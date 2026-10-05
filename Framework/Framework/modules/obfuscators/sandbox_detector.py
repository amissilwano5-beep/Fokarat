import os
import sys
import time

import psutil


class SandboxDetector:
    @staticmethod
    def is_sandbox() -> bool:
        suspicious_procs = [
            'cuckoo', 'sandbox', 'vboxservice', 'vboxtray',
            'vmtoolsd', 'vmsrvc', 'xenservice', 'wine', 'qemu'
        ]

        for proc in psutil.process_iter(['name']):
            try:
                name = (proc.info.get('name') or '').lower()
                for sus in suspicious_procs:
                    if sus in name:
                        return True
            except Exception:
                pass

        if sys.platform == 'win32':
            candidates = [
                r'C:\Program Files\Oracle\VirtualBox Guest Additions',
                r'C:\Program Files\VMware\VMware Tools',
                r'C:\Windows\System32\Drivers\VBoxMouse.sys'
            ]
            if any(os.path.exists(path) for path in candidates):
                return True

        start = time.time()
        time.sleep(0.5)
        if time.time() - start < 0.4:
            return True

        try:
            if psutil.cpu_count() is not None and psutil.cpu_count() < 2:
                return True
        except Exception:
            pass

        return False