"""Tests pour core/logger.py"""
import os
import json

from core.logger import Logger


class TestLogger:
    def test_logger_creates_file(self, temp_dir):
        log_file = os.path.join(temp_dir, "test.log")
        Logger(log_file=log_file)
        assert os.path.exists(log_file)

    def test_log_info_writes_to_file(self, temp_dir, capsys):
        log_file = os.path.join(temp_dir, "test.log")
        logger = Logger(log_file=log_file)

        logger.info("Test message")

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "Test message" in content
        assert "INFO" in content

    def test_log_success_writes_level(self, temp_dir):
        log_file = os.path.join(temp_dir, "test.log")
        logger = Logger(log_file=log_file)

        logger.success("Success message")

        with open(log_file, "r", encoding="utf-8") as f:
            line = f.readline()
            entry = json.loads(line)

        assert entry["level"] == "SUCCESS"
        assert entry["message"] == "Success message"

    def test_log_error_writes_level(self, temp_dir):
        log_file = os.path.join(temp_dir, "test.log")
        logger = Logger(log_file=log_file)

        logger.error("Error message")

        with open(log_file, "r", encoding="utf-8") as f:
            line = f.readline()
            entry = json.loads(line)

        assert entry["level"] == "ERROR"

    def test_log_has_timestamp(self, temp_dir):
        log_file = os.path.join(temp_dir, "test.log")
        logger = Logger(log_file=log_file)

        logger.info("Test")

        with open(log_file, "r", encoding="utf-8") as f:
            line = f.readline()
            entry = json.loads(line)

        assert "timestamp" in entry
        assert entry["timestamp"].endswith("Z")