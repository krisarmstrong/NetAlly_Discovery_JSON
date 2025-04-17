#!/usr/bin/env python3
"""
Project Title: NetworkDiscoveryParser

Parses a NetAlly discovery.json file to extract host data and count valid IPv4 addresses.

Designed for network administrators, it extracts host ID, MAC address, IPv4 address, IPv4 subnet, IPv6 address, MDNS name, and user name from the NetAlly-specific JSON structure.

Author: Kris Armstrong
"""
__version__ = "2.0.1"

import argparse
import json
import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
import ipaddress
from typing import List, Dict, Any, Optional

class Config:
    """Global configuration constants for NetworkDiscoveryParser."""
    LOG_FILE: str = "network_discovery_parser.log"
    ENCODING: str = "utf-8"
    DEFAULT_INPUT: str = "discovery.json"

def setup_logging(verbose: bool, logfile: Optional[str] = None) -> None:
    """Configure logging with console and rotating file handler.

    Args:
        verbose: Enable DEBUG level logging to console if True.
        logfile: Path to log file, defaults to Config.LOG_FILE if unspecified.

    Returns:
        None
    """
    logger = logging.getLogger()
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(console_handler)
    logfile = logfile or Config.LOG_FILE
    file_handler = RotatingFileHandler(logfile, maxBytes=10_000_000, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(file_handler)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.

    Raises:
        SystemExit: If arguments are invalid.
    """
    parser = argparse.ArgumentParser(
        description="Parse a NetAlly discovery.json file to extract host data and count valid IPv4 addresses.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--input_file",
        default=Config.DEFAULT_INPUT,
        help=f"Path to input JSON file (default: {Config.DEFAULT_INPUT})"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose console output"
    )
    parser.add_argument(
        "--logfile",
        help="Path to log file"
    )

    args = parser.parse_args()
    input_path = Path(args.input_file)
    if not input_path.is_file():
        parser.error(f"Input file does not exist: {args.input_file}")
    if input_path.suffix.lower() != ".json":
        parser.error(f"Input file must be a JSON file: {args.input_file}")

    return args

def check_sensitive_data(input_path: Path) -> bool:
    """Check for sensitive data in the JSON file before processing.

    Args:
        input_path: Path to the JSON file.

    Returns:
        True if no sensitive data found, False otherwise.
    """
    sensitive_patterns = [r'api_key\s*=\s*["\'].+["\']', r'password\s*=\s*["\'].+["\']']
    try:
        with input_path.open("r", encoding=Config.ENCODING) as file:
            content = file.read()
        for pattern in sensitive_patterns:
            if re.search(pattern, content):
                logging.warning(f"Potential sensitive data found in {input_path}")
                return False
    except IOError as err:
        logging.error("Failed to read %s for sensitive data check: %s", input_path, err)
        return False
    return True

def count_valid_ips(host_list: List[Dict[str, Any]]) -> int:
    """Count valid IPv4 addresses in the host list.

    Args:
        host_list: List of host dictionaries.

    Returns:
        Number of valid IPv4 addresses.
    """
    ip_count = 0
    for host in host_list:
        host_data = host.get("host", {})
        ip_v4_address = host_data.get("ip_v4_address")
        if ip_v4_address:
            try:
                ipaddress.IPv4Address(ip_v4_address)
                ip_count += 1
                logging.debug("Valid IPv4 address: %s", ip_v4_address)
            except ValueError:
                logging.warning("Invalid IPv4 address: %s", ip_v4_address)
    return ip_count

def extract_host_data(host_list: List[Dict[str, Any]]) -> None:
    """Extract and print host data in a formatted manner.

    Args:
        host_list: List of host dictionaries.

    Returns:
        None
    """
    for index, host in enumerate(host_list, 1):
        host_data = host.get("host", {})
        host_id = host_data.get("host_id", "N/A")
        mac_address = host_data.get("mac_address", "N/A")
        ip_v4_address = host_data.get("ip_v4_address", "N/A")
        ip_v4_subnet = host_data.get("ip_v4_subnet", "N/A")
        ip_v6_address = host_data.get("ip_v6_address", "N/A")
        mdns_name = host_data.get("mdns_name", "N/A")
        user_name = host_data.get("user_name", "N/A")

        print(f"\nHost {index}:")
        print(f"  Host ID: {host_id}")
        print(f"  MAC Address: {mac_address}")
        print(f"  IPv4 Address: {ip_v4_address}")
        print(f"  IPv4 Subnet: {ip_v4_subnet}")
        print(f"  IPv6 Address: {ip_v6_address}")
        print(f"  MDNS Name: {mdns_name}")
        print(f"  User Name: {user_name}")
        logging.debug("Processed host %d: host_id=%s, ip_v4=%s", index, host_id, ip_v4_address)

def main() -> None:
    """Parse NetAlly discovery.json and process host data."""
    try:
        args = parse_arguments()
        setup_logging(args.verbose, args.logfile)
        input_path = Path(args.input_file)
        logging.info("Starting parsing of JSON file: %s", input_path)

        if not check_sensitive_data(input_path):
            logging.error("Aborted due to potential sensitive data")
            print("Error: Potential sensitive data detected in input file")
            sys.exit(1)

        with input_path.open("r", encoding=Config.ENCODING) as json_file:
            json_data = json.load(json_file)
        logging.info("Successfully read JSON file: %s", input_path)

        if "Detail" not in json_data or "host_list" not in json_data["Detail"]:
            logging.error("Invalid JSON structure: missing 'Detail' or 'host_list'")
            print("Error: JSON file must contain 'Detail' and 'host_list' keys")
            sys.exit(1)

        host_list = json_data["Detail"]["host_list"]
        if not isinstance(host_list, list):
            logging.error("Invalid JSON structure: 'host_list' is not a list")
            print("Error: 'host_list' must be a list")
            sys.exit(1)

        valid_ip_count = count_valid_ips(host_list)
        extract_host_data(host_list)
        print(f"\nTotal Valid IPv4 Address(es): {valid_ip_count}")
        logging.info("Parsing completed: %d valid IPv4 addresses found", valid_ip_count)

    except json.JSONDecodeError as err:
        print(f"Error: Invalid JSON in {input_path}: {err}")
        logging.error("Invalid JSON: %s", err)
        sys.exit(1)
    except IOError as err:
        print(f"Error: File operation failed: {err}")
        logging.error("File operation failed: %s", err)
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Cancelled by user")
        sys.exit(0)
    except Exception as err:
        print(f"Unexpected error: {err}")
        logging.error("Unexpected error: %s", err)
        sys.exit(1)

if __name__ == "__main__":
    main()