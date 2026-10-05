import struct

def speck_encrypt(plaintext: bytes, key: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("La clé doit faire 16 octets")
    if len(plaintext) % 8 != 0:
        plaintext = plaintext.ljust((len(plaintext) + 7) // 8 * 8, b'\x00')
    rounds = 32
    alpha = 8
    beta = 3
    k = [0] * (rounds + 1)
    k[0] = struct.unpack('<Q', key[0:8])[0]
    l = [struct.unpack('<Q', key[i*8:(i+1)*8])[0] for i in range(1, 2)]
    for i in range(rounds - 1):
        l_i = (k[i] >> alpha) | ((k[i] & ((1 << alpha) - 1)) << (64 - alpha))
        k[i+1] = l_i ^ l[0] ^ i
        l[0] = (l[0] >> beta) | ((l[0] & ((1 << beta) - 1)) << (64 - beta))
        l[0] ^= k[i+1]
    ciphertext = b''
    for i in range(0, len(plaintext), 8):
        x = struct.unpack('<Q', plaintext[i:i+8])[0]
        y = struct.unpack('<Q', plaintext[i+8:i+16])[0] if i+8 < len(plaintext) else 0
        for i in range(rounds):
            x = ( (x >> alpha) | ((x & ((1 << alpha) - 1)) << (64 - alpha)) ) ^ y ^ k[i]
            y = ( (y >> beta) | ((y & ((1 << beta) - 1)) << (64 - beta)) ) ^ x
        ciphertext += struct.pack('<Q', x) + struct.pack('<Q', y)
    return ciphertext[:len(plaintext)]