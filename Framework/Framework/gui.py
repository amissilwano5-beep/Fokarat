import os
import shutil
import subprocess
import threading
from tkinter import filedialog, messagebox, scrolledtext

import customtkinter as ctk

from ai.Assistant import Assistant
from ai.Agent import AutonomousAgent
from core.config import Config
from core.logger import Logger
from mobile.android_gen import AndroidPayloadGenerator
from mobile.ios_gen import IosZeroClickGenerator
from modules.injectors.badusb_gen import BadUSBGenerator
from modules.listeners.listener_manager import ListenerManager
from modules.obfuscators.sandbox_detector import SandboxDetector
from modules.obfuscators.speck_cipher import speck_encrypt
from modules.payload_generators.cpp_gen import CppPayloadGenerator
from modules.payload_generators.python_gen import PythonPayloadGenerator
from modules.persistence.wmi_persist import WMIPersistence
from ai.polymorph_llm import PolymorphLLM

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FrameworkGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Thèse Framework - Cybersécurité Offensive v2.0")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.config = Config()
        self.logger = Logger()
        self.listener_manager = ListenerManager()
        self.source_file = None
        self.payload_path = None

        self.kali_ip = ctk.StringVar(value=self.config.get("kali_ip", self.config.get_local_network_ip()))
        self.kali_port = ctk.StringVar(value=str(self.config.get("kali_port", 4444)))
        self.llm_model_path = ctk.StringVar(value=self.config.get("llm_model_path", "models/mistral-7b.gguf"))
        self.android_keystore = ctk.StringVar(value=self.config.get("android_keystore", "my.keystore"))
        self.android_apk = ctk.StringVar(value="")
        self.payload_file = ctk.StringVar()
        self.ssl_cert = ctk.StringVar()
        self.http_port = ctk.StringVar(value=str(self.config.get("http_server_port", 8080)))
        self.network_mode = ctk.StringVar(value=self.config.get("network_mode", "tcp"))
        self.network_protocol = ctk.StringVar(value=self.config.get("network_protocol", "tcp"))

        self._setup_ui()
        self._setup_tabs()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.listener_manager.stop_all()
        self.destroy()

    def _setup_ui(self):
        top_frame = ctk.CTkFrame(self, height=50)
        top_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(top_frame, text="Framework Doctoral - Cybersécurité Offensive v2.0", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="Sauvegarder config", command=self.save_config).pack(side="right", padx=5)
        ctk.CTkButton(top_frame, text="À propos", command=self.show_about).pack(side="right", padx=5)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

    def _setup_tabs(self):
        self.tabview.add("Payloads")
        self.tabview.add("Mobile")
        self.tabview.add("Injection & Persistance")
        self.tabview.add("Évitement & IA")
        self.tabview.add("Listeners")
        self.tabview.add("Assistant IA")
        self.tabview.add("Logs & Configuration")

        self._setup_payloads_tab()
        self._setup_mobile_tab()
        self._setup_injection_tab()
        self._setup_evasion_tab()
        self._setup_listeners_tab()
        self._setup_ai_tab()
        self._setup_logs_tab()

    def _setup_payloads_tab(self):
        tab = self.tabview.tab("Payloads")
        frame_params = ctk.CTkFrame(tab)
        frame_params.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_params, text="LHOST (Kali IP):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(frame_params, textvariable=self.kali_ip, width=150).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame_params, text="LPORT:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(frame_params, textvariable=self.kali_port, width=80).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkLabel(frame_params, text="Protocole réseau:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ctk.CTkOptionMenu(frame_params, values=["tcp", "http", "https"], variable=self.network_mode).grid(row=0, column=5, padx=5, pady=5)

        frame_buttons = ctk.CTkFrame(tab)
        frame_buttons.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(frame_buttons, text="Générer Python (reverse SSL)", command=self.gen_python, width=250).pack(side="left", padx=5)
        ctk.CTkButton(frame_buttons, text="Générer C++ (syscalls)", command=self.gen_cpp, width=250).pack(side="left", padx=5)
        self.payload_output = scrolledtext.ScrolledText(tab, height=10, bg="black", fg="white")
        self.payload_output.pack(fill="both", expand=True, padx=10, pady=10)

    def _setup_mobile_tab(self):
        tab = self.tabview.tab("Mobile")
        frame_android = ctk.CTkFrame(tab)
        frame_android.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_android, text="Android", font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
        ctk.CTkLabel(frame_android, text="APK original:").pack(anchor="w", padx=5)
        ctk.CTkEntry(frame_android, textvariable=self.android_apk, placeholder_text="Chemin APK").pack(fill="x", padx=5, pady=2)
        ctk.CTkButton(frame_android, text="Sélectionner APK", command=self.select_apk).pack(pady=2)
        ctk.CTkButton(frame_android, text="Générer APK backdooré", command=self.gen_android, fg_color="orange").pack(pady=5)
        self.mobile_output = scrolledtext.ScrolledText(tab, height=10, bg="black", fg="white")
        self.mobile_output.pack(fill="both", expand=True, padx=10, pady=10)

    def _setup_injection_tab(self):
        tab = self.tabview.tab("Injection & Persistance")
        frame_badusb = ctk.CTkFrame(tab)
        frame_badusb.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_badusb, text="BadUSB (DuckyScript)", font=("Arial", 12, "bold")).pack(anchor="w")
        ctk.CTkButton(frame_badusb, text="Générer script Ducky (mode lab sûr)", command=self.gen_badusb).pack(pady=5)
        self.injection_output = scrolledtext.ScrolledText(tab, height=10, bg="black", fg="white")
        self.injection_output.pack(fill="both", expand=True, padx=10, pady=10)

    def _setup_evasion_tab(self):
        tab = self.tabview.tab("Évitement & IA")
        frame_sandbox = ctk.CTkFrame(tab)
        frame_sandbox.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_sandbox, text="Détection de sandbox", font=("Arial", 12, "bold")).pack(anchor="w")
        ctk.CTkButton(frame_sandbox, text="Tester si en sandbox", command=self.check_sandbox).pack(pady=5)
        self.evasion_output = scrolledtext.ScrolledText(tab, height=10, bg="black", fg="white")
        self.evasion_output.pack(fill="both", expand=True, padx=10, pady=10)

    def _setup_listeners_tab(self):
        tab = self.tabview.tab("Listeners")
        frame_listener = ctk.CTkFrame(tab)
        frame_listener.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_listener, text="Port du listener:").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkEntry(frame_listener, textvariable=self.kali_port, width=80).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(frame_listener, text="Démarrer listener ncat SSL", command=self.start_ncat_listener).grid(row=3, column=0, pady=5)
        ctk.CTkButton(frame_listener, text="Démarrer listener Metasploit", command=self.start_msf_listener).grid(row=3, column=1, pady=5)
        ctk.CTkButton(frame_listener, text="Arrêter tous les listeners", command=self.stop_listeners, fg_color="red").grid(row=5, column=0, columnspan=2, pady=10)
        self.listener_output = scrolledtext.ScrolledText(tab, height=10, bg="black", fg="white")
        self.listener_output.pack(fill="both", expand=True, padx=10, pady=10)

    def _setup_ai_tab(self):
        tab = self.tabview.tab("Assistant IA")
        frame_chat = ctk.CTkFrame(tab)
        frame_chat.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_display = scrolledtext.ScrolledText(frame_chat, height=15, bg="black", fg="white")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        frame_input = ctk.CTkFrame(tab)
        frame_input.pack(fill="x", padx=10, pady=5)
        self.chat_entry = ctk.CTkEntry(frame_input, placeholder_text="Posez une question à l'assistant...")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(frame_input, text="Envoyer", command=self.send_chat).pack(side="right", padx=5)

    def _setup_logs_tab(self):
        tab = self.tabview.tab("Logs & Configuration")
        self.log_text = scrolledtext.ScrolledText(tab, height=15, bg="black", fg="white")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, msg):
        self.after(0, lambda: self.log_text.insert("end", msg + "\n"))
        self.after(0, lambda: self.log_text.see("end"))
        self.logger.info(msg)

    def save_config(self):
        self.config.set("kali_ip", self.kali_ip.get())
        self.config.set("kali_port", int(self.kali_port.get()))
        self.config.set("network_mode", self.network_mode.get())
        self.config.set("network_protocol", self.network_mode.get())
        self.config.set("llm_model_path", self.llm_model_path.get())
        self.config.set("android_keystore", self.android_keystore.get())
        self.config.set("http_server_port", int(self.http_port.get()))
        self.config.save()
        messagebox.showinfo("Configuration", "Configuration sauvegardée")

    def show_about(self):
        messagebox.showinfo("À propos", "Framework Doctoral - Cybersécurité Offensive v2.0\n" "Dépasse TheFatRat avec IA, Syscalls, Mobile zero-click, etc.\n" "© Thèse 2026 - Usage réservé aux tests autorisés.")

    def _run_threaded(self, target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        thread.start()

    def gen_python(self):
        self._run_threaded(self._gen_python)

    def _gen_python(self):
        self.log("[*] Génération payload Python...")
        self.config.set("kali_ip", self.kali_ip.get())
        self.config.set("kali_port", int(self.kali_port.get()))
        result = PythonPayloadGenerator().run(self.config)
        self.after(0, lambda: self.payload_output.insert("end", str(result) + "\n"))
        self.log(f"[+] {result}")

    def gen_cpp(self):
        self._run_threaded(self._gen_cpp)

    def _gen_cpp(self):
        self.log("[*] Génération payload C++...")
        self.config.set("kali_ip", self.kali_ip.get())
        self.config.set("kali_port", int(self.kali_port.get()))
        result = CppPayloadGenerator().run(self.config)
        self.after(0, lambda: self.payload_output.insert("end", str(result) + "\n"))
        self.log(f"[+] {result}")

    def select_apk(self):
        path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if path:
            self.android_apk.set(path)
            self.log(f"[+] APK sélectionné : {path}")

    def gen_android(self):
        self._run_threaded(self._gen_android)

    def _gen_android(self):
        self.log("[*] Génération APK Android...")
        self.config.set("kali_ip", self.kali_ip.get())
        self.config.set("kali_port", int(self.kali_port.get()))
        self.config.set("android_apk_input", self.android_apk.get())
        result = AndroidPayloadGenerator().run(self.config)
        self.after(0, lambda: self.mobile_output.insert("end", str(result) + "\n"))
        self.log(f"[+] {result}")

    def gen_badusb(self):
        self._run_threaded(self._gen_badusb)

    def _gen_badusb(self):
        self.log("[*] Génération script BadUSB...")
        result = BadUSBGenerator().run(self.config)
        self.after(0, lambda: self.injection_output.insert("end", str(result) + "\n"))
        self.log(f"[+] {result}")

    def check_sandbox(self):
        self._run_threaded(self._check_sandbox)

    def _check_sandbox(self):
        self.log("[*] Détection de sandbox...")
        is_sb = SandboxDetector.is_sandbox()
        self.after(0, lambda: self.evasion_output.insert("end", f"SANDBOX DETECTED: {is_sb}\n"))
        self.log(f"[+] Résultat : {'SANDBOX DÉTECTÉE' if is_sb else 'ENVIRONNEMENT NORMAL'}")

    def start_ncat_listener(self):
        self._run_threaded(self._start_ncat)

    def _start_ncat(self):
        port = int(self.kali_port.get())
        self.log(f"[*] Démarrage listener ncat sur port {port}...")
        proc = self.listener_manager.start_ncat(port)
        if proc:
            self.after(0, lambda: self.listener_output.insert("end", f"ncat listening on {port}\n"))
            self.log("[+] Listener ncat actif.")
        else:
            self.log("[!] Échec du démarrage de ncat")

    def start_msf_listener(self):
        self._run_threaded(self._start_msf)

    def _start_msf(self):
        lhost = self.kali_ip.get()
        lport = int(self.kali_port.get())
        self.log(f"[*] Démarrage listener Metasploit sur {lhost}:{lport}...")
        proc = self.listener_manager.start_msf(lhost, lport)
        if proc:
            self.after(0, lambda: self.listener_output.insert("end", f"MSF listener started on {lhost}:{lport}\n"))
            self.log("[+] Metasploit handler démarré.")
        else:
            self.log("[!] Échec du démarrage de Metasploit")

    def stop_listeners(self):
        self.listener_manager.stop_all()
        self.log("[!] Tous les listeners arrêtés.")
        self.after(0, lambda: self.listener_output.insert("end", "Listeners stopped.\n"))

    def send_chat(self):
        msg = self.chat_entry.get()
        if not msg:
            return
        self.chat_display.insert("end", f"Vous: {msg}\n")
        self.chat_entry.delete(0, "end")
        self._run_threaded(self._get_ai_response, msg)

    def _get_ai_response(self, msg):
        assistant = Assistant(self.llm_model_path.get())
        reply = assistant.chat(msg)
        self.after(0, lambda: self.chat_display.insert("end", f"Assistant: {reply}\n\n"))


if __name__ == "__main__":
    app = FrameworkGUI()
    app.mainloop()