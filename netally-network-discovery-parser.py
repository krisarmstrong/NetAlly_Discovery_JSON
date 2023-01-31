#!/usr/bin python3

"""
Script Name: Netally-network-discovery-parser.py
Author: Kris Armstrong
Date: 1.17.2023
Version: 1.0

This script takes a discovery.json file as input and extracts the host data from it.
It then counts the number of valid IPv4 addresses and prints the host data and the total number of valid IPs.

Usage: python discovery.py discovery.json
"""

import json
import sys
import socket

def count_valid_ips(host_list):
    """
    Count the number of valid IPv4 addresses in the host_list
    Args:
        host_list (list): List of hosts
    Returns:
        int: The number of valid IPv4 addresses
    """
    ip_count = 0
    for host in host_list:
        host_data = host["host"]
        ip_v4_address = host_data.get("ip_v4_address", None)
        if ip_v4_address != None:
            try:
                socket.inet_aton(ip_v4_address)
                ip_count += 1
            except socket.error:
                pass
    return ip_count


def extract_host_data(host_list):
    """
    Extract and print the host data
    Args:
        host_list (list): List of hosts
    """
    for host in host_list:
        host_data = host["host"]
        host_id = host_data.get("host_id", None)
        mac_address = host_data.get("mac_address", None)
        ip_v4_address = host_data.get("ip_v4_address", None)
        ip_v4_subnet = host_data.get("ip_v4_subnet", None)
        ip_v6_address = host_data.get("ip_v6_address", None)
        mdns_name = host_data.get("mdns_name", None)
        user_name = host_data.get("user_name", None)
        print("Host ID:", host_id)
        print("MAC Address:", mac_address)
        print("IPv4 Address:", ip_v4_address)
        print("IPv4 Subnet:", ip_v4_subnet)
        print("IPv6 Address:", ip_v6_address)
        print("MDNS Name:", mdns_name)
        print("User Name:", user_name)
        print()


def main():
    """
    Main function to run the script
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py discovery.json")
        sys.exit()

    json_file = sys.argv[1]

    # Open the JSON file and parse its contents
    try:
        with open(json_file, "r") as json_file:
            json_data = json.load(json_file)
    except:
        print("Error: Unable to open JSON file")
        sys.exit()

    # Extract the host_list from the JSON data
    host_list = json_data["Detail"]["host_list"]

    # Count the valid IP addresses
    valid_ip_count = count_valid_ips(host_list)

    # Extract and print the host data
    extract_host_data(host_list)

    # Print the total number of valid IP addresses
    print("Total Valid IP(s):", valid_ip_count)


if __name__ == "__main__":
    main()