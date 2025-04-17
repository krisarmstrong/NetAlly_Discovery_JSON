#!/usr/bin/env python3
"""
Project Title: NetworkDiscoveryParserTests

Pytest smoke tests for network_discovery_parser.py functionality.

Author: Kris Armstrong
"""
__version__ = "1.0.0"

import pytest
import subprocess
from pathlib import Path
import network_discovery_parser

@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for testing.

    Args:
        tmp_path: Pytest-provided temporary path.

    Returns:
        Path to temporary directory.
    """
    return tmp_path

def test_count_valid_ips(temp_dir: Path) -> None:
    """Test counting valid IPv4 addresses."""
    host_list = [
        {"host": {"ip_v4_address": "192.168.1.100"}},
        {"host": {"ip_v4_address": "invalid_ip"}},
    ]
    count = network_discovery_parser.count_valid_ips(host_list)
    assert count == 1

def test_keyboard_interrupt(temp_dir: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test KeyboardInterrupt handling.

    Args:
        temp_dir: Temporary directory for testing.
        caplog: Pytest fixture to capture log output.
    """
    with pytest.raises(SystemExit) as exc:
        network_discovery_parser.setup_logging(False)
        raise KeyboardInterrupt
    assert exc.value.code == 0
    assert "Cancelled by user" in caplog.text

def test_version_bumper_generation(temp_dir: Path) -> None:
    """Test version_bumper.py generation."""
    from git_setup import VERSION_BUMPER_TEMPLATE, create_file
    create_file(temp_dir / 'version_bumper.py', VERSION_BUMPER_TEMPLATE)
    assert (temp_dir / 'version_bumper.py').exists()
    result = subprocess.run(['python', 'version_bumper.py', '--help'], cwd=temp_dir, capture_output=True, text=True)
    assert result.returncode == 0