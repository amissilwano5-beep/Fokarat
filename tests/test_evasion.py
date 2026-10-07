"""Tests pour les modules d'évasion"""
import os
import base64
import zlib

from modules.evasion.payload_padding import PaddingGenerator
from modules.evasion.python_obfuscator import PythonObfuscator


class TestPythonObfuscator:
    def test_obfuscate_returns_string(self, sample_python_code):
        obf = PythonObfuscator().obfuscate(sample_python_code)
        assert isinstance(obf, str)
        assert len(obf) > 0

    def test_obfuscate_contains_no_original_code(self, sample_python_code):
        obf = PythonObfuscator().obfuscate(sample_python_code)
        # Le code original ne doit PAS apparaître en clair
        assert "def hello():" not in obf
        assert "print(" not in obf

    def test_obfuscate_contains_base64(self, sample_python_code):
        obf = PythonObfuscator().obfuscate(sample_python_code)
        assert "base64" in obf
        assert "zlib" in obf

    def test_obfuscate_is_different_each_time(self, sample_python_code):
        obf1 = PythonObfuscator().obfuscate(sample_python_code)
        obf2 = PythonObfuscator().obfuscate(sample_python_code)
        # La clé XOR est aléatoire, donc les 2 doivent être différents
        assert obf1 != obf2


class TestPaddingGenerator:
    def test_generate_padding_block_returns_string(self):
        gen = PaddingGenerator()
        block = gen.generate_padding_block(size_kb=1)
        assert isinstance(block, str)
        assert "unsigned char" in block

    def test_generate_fake_functions(self):
        gen = PaddingGenerator()
        funcs = gen.generate_fake_functions(count=5)
        assert isinstance(funcs, str)
        assert "int " in funcs
        assert "(void)" in funcs

    def test_wrap_payload_contains_original(self, sample_c_code):
        gen = PaddingGenerator()
        wrapped = gen.wrap_payload(sample_c_code, size_kb=1, fake_funcs=3)
        # Le code original doit être présent
        assert "Hello, FOKARAT" in wrapped
        # Du padding doit être présent
        assert "unsigned char" in wrapped

    def test_wrap_payload_is_random(self, sample_c_code):
        gen = PaddingGenerator()
        w1 = gen.wrap_payload(sample_c_code, size_kb=1, fake_funcs=3)
        w2 = gen.wrap_payload(sample_c_code, size_kb=1, fake_funcs=3)
        # Chaque wrap doit être différent (noms aléatoires)
        assert w1 != w2