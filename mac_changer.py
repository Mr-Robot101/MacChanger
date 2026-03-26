#!/usr/bin/env python3
"""
mac_changer.py - A command-line tool to spoof MAC addresses on Linux systems.

Usage:
    sudo python3 mac_changer.py -i <interface> -m <new_mac>

Example:
    sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55

Requirements:
    - Linux OS
    - Root/sudo privileges
    - net-tools (ifconfig) installed
"""

import subprocess
import optparse
import re
import sys


# ---------------------------------------------------------------------------
# Argument Parsing
# ---------------------------------------------------------------------------

def get_arguments():
    """
    Parse and validate command-line arguments.

    Returns:
        optparse.Values: Parsed options containing 'interface' and 'mac_address'.

    Exits:
        Prints an error and exits if required arguments are missing or invalid.
    """
    parser = optparse.OptionParser(
        usage="usage: %prog -i <interface> -m <mac_address>",
        description="A tool to change/spoof the MAC address of a network interface."
    )

    parser.add_option(
        "-i", "--interface",
        dest="interface",
        help="Network interface to change (e.g. eth0, wlan0)"
    )
    parser.add_option(
        "-m", "--mac",
        dest="mac_address",
        help="New MAC address in the format XX:XX:XX:XX:XX:XX"
    )

    (options, arguments) = parser.parse_args()

    # Validate that both required arguments are provided
    if not options.interface:
        parser.error("[-] Please specify a network interface. Use --help for more info.")
    if not options.mac_address:
        parser.error("[-] Please specify a MAC address. Use --help for more info.")

    # Validate the MAC address format before proceeding
    if not is_valid_mac(options.mac_address):
        parser.error(
            f"[-] '{options.mac_address}' is not a valid MAC address.\n"
            "    Expected format: XX:XX:XX:XX:XX:XX (e.g. 00:11:22:33:44:55)"
        )

    return options


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def is_valid_mac(mac_address):
    """
    Check whether a string is a valid MAC address.

    A valid MAC address matches the pattern: XX:XX:XX:XX:XX:XX
    where each X is a hexadecimal digit (0-9, a-f, A-F).

    Args:
        mac_address (str): The MAC address string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    return bool(mac_pattern.match(mac_address))


# ---------------------------------------------------------------------------
# Core Functionality
# ---------------------------------------------------------------------------

def get_current_mac(interface):
    """
    Retrieve the current MAC address of a network interface.

    Runs 'ifconfig <interface>' and parses the output for a MAC address.

    Args:
        interface (str): The network interface name (e.g. 'eth0').

    Returns:
        str | None: The MAC address string if found, otherwise None.
    """
    try:
        ifconfig_output = subprocess.check_output(
            ["ifconfig", interface],
            stderr=subprocess.STDOUT  # Capture stderr so errors don't leak to terminal
        )
        # Decode bytes to string for regex matching
        ifconfig_str = ifconfig_output.decode("utf-8")

    except subprocess.CalledProcessError as e:
        print(f"[-] Error reading interface '{interface}': {e.output.decode().strip()}")
        return None

    # Search for a MAC address pattern in the ifconfig output
    mac_search = re.search(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", ifconfig_str)
    if mac_search:
        return mac_search.group(0)

    print(f"[-] Could not read MAC address for interface '{interface}'.")
    return None


def change_mac(interface, new_mac):
    """
    Change the MAC address of a network interface using ifconfig.

    Steps:
        1. Bring the interface down.
        2. Set the new hardware (MAC) address.
        3. Bring the interface back up.

    Args:
        interface (str): The network interface to modify (e.g. 'eth0').
        new_mac   (str): The new MAC address to assign (e.g. '00:11:22:33:44:55').
    """
    print(f"[*] Changing MAC address for '{interface}' to '{new_mac}'...")

    # Bring the interface down before modifying its hardware address
    subprocess.call(["ifconfig", interface, "down"])

    # Assign the new MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

    # Bring the interface back up
    subprocess.call(["ifconfig", interface, "up"])


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main():
    """
    Main entry point for the MAC changer tool.

    Workflow:
        1. Parse arguments.
        2. Display the current MAC address.
        3. Attempt to change the MAC address.
        4. Verify and report whether the change succeeded.
    """
    # Parse CLI arguments (exits on invalid input)
    options = get_arguments()

    # Read and display the MAC address before any changes
    original_mac = get_current_mac(options.interface)
    if original_mac is None:
        print(f"[-] Could not find interface '{options.interface}'. Exiting.")
        sys.exit(1)

    print(f"[*] Current MAC address : {original_mac}")

    # Perform the MAC address change
    change_mac(options.interface, options.mac_address)

    # Verify the change was applied successfully
    updated_mac = get_current_mac(options.interface)
    if updated_mac and updated_mac.lower() == options.mac_address.lower():
        print(f"[+] MAC address successfully changed to: {updated_mac}")
    else:
        print(f"[-] MAC address change failed. Current MAC: {updated_mac}")
        sys.exit(1)


if __name__ == "__main__":
    main()
