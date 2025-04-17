# Changelog

## [2.0.1] - 2025-04-18
- network_discovery_parser.py: Added type annotations, rotating log handler, sensitive data checks
- tests/test_network_discovery_parser.py: Added version_bumper.py generation test
- Standardized naming to NetworkDiscoveryParser, renamed netally_discovery_json.py and changelog.txt
- Updated README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md

## [2.0.0] - 2025-04-18
- Refactored for enhanced Python 3 compatibility
- Merged netally-network-discovery-parser.py and net.py into single script
- Replaced sys.argv with argparse
- Added logging to network_discovery_parser.log
- Used pathlib for cross-platform file handling
- Switched to ipaddress.IPv4Address for IPv4 validation
- Added Config class for global constants
- Improved error handling and output formatting
- Ensured PEP 8 compliance with Google-style docstrings
- Set up Git repository with .gitignore, bump_version.py, requirements.txt
- Added README.md and changelog.txt
- Archived original scripts in archive/v1.0.0/
- Incremented to 2.0.0 due to major overhaul

## [1.0] - 2023-01-17
- Released netally-network-discovery-parser.py
- Parsed discovery.json for host data and IPv4 counts
- Used socket.inet_aton for IPv4 validation
- Basic error handling

## [1.0] - 2021-01-01
- Initial release of net.py
- Parsed discovery.json for host data and IPv4 counts
- Used socket.inet_aton for IPv4 validation
- Basic error handling