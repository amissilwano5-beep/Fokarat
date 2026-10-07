"""
FOKARAT - Anti-Debug
Détecte les debuggers et empêche l'analyse dynamique.
"""
from core.logger import Logger

logger = Logger()


class AntiDebugGenerator:

    C_CODE = r'''
#include <windows.h>
#include <stdio.h>

typedef struct _MY_PEB {
    BYTE Reserved1[2];
    BYTE BeingDebugged;
    BYTE Reserved2[1];
    PVOID Reserved3[2];
    PVOID Ldr;
    PVOID ProcessParameters;
} MY_PEB, *PMY_PEB;

BOOL is_debugged() {
    // 1. IsDebuggerPresent
    if (IsDebuggerPresent()) return TRUE;

    // 2. CheckRemoteDebuggerPresent
    BOOL dbg = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &dbg);
    if (dbg) return TRUE;

    // 3. PEB->BeingDebugged
    #ifdef _WIN64
        PMY_PEB peb = (PMY_PEB)__readgsqword(0x60);
    #else
        PMY_PEB peb = (PMY_PEB)__readfsdword(0x30);
    #endif
    if (peb && peb->BeingDebugged) return TRUE;

    // 4. Timing check (les debuggers ralentissent)
    DWORD t1 = GetTickCount();
    Sleep(100);
    DWORD t2 = GetTickCount();
    if ((t2 - t1) > 200) return TRUE;

    // 5. Hardware breakpoints (Dr0-Dr3)
    CONTEXT ctx = {0};
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    if (GetThreadContext(GetCurrentThread(), &ctx)) {
        if (ctx.Dr0 || ctx.Dr1 || ctx.Dr2 || ctx.Dr3) return TRUE;
    }

    return FALSE;
}
'''

    def wrap(self, code):
        wrapped = self.C_CODE + "\n\n" + code.replace(
            "int main() {",
            "int main() {\n    if (is_debugged()) return 1;"
        )
        logger.success("Protection Anti-Debug ajoutée")
        return wrapped