"""Tests pour core/config.py"""
import os

from core.config import Config


class TestConfig:
    def test_default_values(self, temp_dir):
        config_path = os.path.join(temp_dir, "test_config.yaml")
        config = Config(config_file=config_path)

        assert config.get("lhost") == ""
        assert config.get("lport") == 4444
        assert config.get("http_server_port") == 8080

    def test_set_and_get(self, temp_config):
        temp_config.set("lhost", "192.168.1.50")
        temp_config.set("lport", 5555)

        assert temp_config.get("lhost") == "192.168.1.50"
        assert temp_config.get("lport") == 5555

    def test_save_and_load(self, temp_dir):
        config_path = os.path.join(temp_dir, "test_save.yaml")

        config1 = Config(config_file=config_path)
        config1.set("lhost", "10.0.0.1")
        config1.set("lport", 9999)
        assert config1.save() is True

        config2 = Config(config_file=config_path)
        assert config2.get("lhost") == "10.0.0.1"
        assert config2.get("lport") == 9999

    def test_get_local_network_ip(self, temp_config):
        ip = temp_config.get_local_network_ip()
        assert isinstance(ip, str)
        assert len(ip) > 0

    def test_get_default_value(self, temp_config):
        assert temp_config.get("inexistant", "default_value") == "default_value"