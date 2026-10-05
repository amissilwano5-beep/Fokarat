import hashlib
from modules.obfuscators.spek_cipher import speck_encrypt


def _normalize_key(key: bytes) -> bytes:
    if len(key) == 16:
        return key
    digest = hashlib.sha256(key).digest()
    return digest[:16]


def _rol(x, n):
    return ((x << n) | (x >> (16 - n))) & 0xFFFF


def _ror(x, n):
    return ((x >> n) | (x << (16 - n))) & 0xFFFF


def speck_encrypt(data: bytes, key: bytes) -> bytes:
    key = _normalize_key(key)
    if not data:
        return b""

    key_words = [int.from_bytes(key[i:i+2], 'little') for i in range(0, 16, 2)]
    if len(key_words) != 8:
        raise ValueError("Clé Speck invalide.")

    ciphertext = bytearray()
    block_size = 16
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block = block + b'\x00' * (block_size - len(block))
        x = int.from_bytes(block[:8], 'little')
        y = int.from_bytes(block[8:], 'little')

        for round_idx in range(22):
            x = (_ror(x, 8) + y) & 0xFFFFFFFFFFFFFFFF
            x ^= key_words[round_idx % 8]
            y = (_rol(y, 3) ^ x) & 0xFFFFFFFFFFFFFFFF

        ciphertext.extend(x.to_bytes(8, 'little'))
        ciphertext.extend(y.to_bytes(8, 'little'))

    return bytes(ciphertext)


__all__ = ["speck_encrypt"]
