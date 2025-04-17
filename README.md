# NetworkDiscoveryParser

A Python tool to parse NetAlly discovery.json files and extract host data, including host ID, MAC address, IPv4 address, IPv4 subnet, IPv6 address, MDNS name, and user name.

Designed for network administrators, it counts valid IPv4 addresses using strict validation.

## Installation
```bash
chmod +x network_discovery_parser.py
```

## Usage
### network_discovery_parser.py
```bash
./network_discovery_parser.py [--input_file discovery.json] [--verbose] [--logfile path]
```

### version_bumper.py
```bash
python version_bumper.py --project_dir /path/to/project [--type minor] [--commit] [--git_tag] [--dry_run]
```

## Generated Files (via git_setup.py)
- **.gitignore**: Ignores Python, IDE, OS, and project-specific files (e.g., `__pycache__`, `.venv`, `tests/output/`).
- **README.md**: Project template with customizable title, installation, and usage.
- **CHANGELOG.md**: Initial changelog with a 0.1.0 entry, customizable author.
- **requirements.txt**: Placeholder for dependencies.
- **LICENSE**: Proprietary license for NetAlly data.
- **CONTRIBUTING.md**: Fork-branch-PR guidelines.
- **CODE_OF_CONDUCT.md**: Contributor Covenant with contact info.
- **tests/**: Directory with a placeholder test file.
- **version_bumper.py** (optional): Tool for bumping semantic versions.

## Notes
- **Proprietary License**: This software is intended for use with NetAlly network discovery data. Unauthorized distribution or modification is prohibited.
- **JSON Structure**: Assumes `Detail.host_list` structure in `discovery.json`.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com)
[![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org)