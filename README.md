# MAC Changer

A lightweight Python command-line tool for spoofing the MAC address of a network interface on Linux systems.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Disclaimer](#disclaimer)

---

## About

MAC Changer lets you temporarily change the hardware (MAC) address of any network interface on a Linux machine. This is useful for privacy, penetration testing labs, and network troubleshooting.

---

## Features

- Change the MAC address of any network interface
- Validates MAC address format before attempting any changes
- Verifies the change was successfully applied
- Clear, descriptive output at every step
- Graceful error handling with informative messages

---

## Requirements

| Requirement | Notes |
|---|---|
| Python 3.6+ | f-strings are used throughout |
| Linux OS | Relies on `ifconfig` (not available on macOS/Windows) |
| `net-tools` | Provides the `ifconfig` command |
| Root privileges | Required to modify network interfaces |

Install `net-tools` if it's not already present:

```bash
sudo apt install net-tools       # Debian / Ubuntu
sudo dnf install net-tools       # Fedora / RHEL
sudo pacman -S net-tools         # Arch Linux
```

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/mac-changer.git
cd mac-changer
```

2. **No additional dependencies required** — the script uses only Python standard library modules.

---

## Usage

```
sudo python3 mac_changer.py -i <interface> -m <new_mac_address>
```

### Options

| Flag | Long form | Description |
|---|---|---|
| `-i` | `--interface` | Network interface to modify (e.g. `eth0`, `wlan0`) |
| `-m` | `--mac` | New MAC address in `XX:XX:XX:XX:XX:XX` format |
| `-h` | `--help` | Show help message and exit |

> **Note:** Root/sudo privileges are required to bring network interfaces up and down.

---

## Examples

**Change the MAC address of `eth0`:**

```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

**Expected output:**

```
[*] Current MAC address : 08:00:27:ab:cd:ef
[*] Changing MAC address for 'eth0' to '00:11:22:33:44:55'...
[+] MAC address successfully changed to: 00:11:22:33:44:55
```

**Display help:**

```bash
python3 mac_changer.py --help
```

---

## How It Works

1. **Argument parsing** — The script uses `optparse` to collect the target interface and desired MAC address from the command line.
2. **Validation** — The MAC address is checked against a regex pattern (`XX:XX:XX:XX:XX:XX`) before any system calls are made.
3. **Current MAC retrieval** — `ifconfig <interface>` is called and its output is parsed with a regex to extract the current MAC address.
4. **MAC change** — The interface is brought down with `ifconfig <interface> down`, the new address is assigned with `ifconfig <interface> hw ether <mac>`, and the interface is brought back up.
5. **Verification** — The MAC address is read again after the change and compared to the requested value to confirm success.

---

## Project Structure

```
mac-changer/
├── mac_changer.py   # Main script
└── README.md        # This file
```

---

## Disclaimer

This tool is intended for **educational purposes and authorized testing only**. Changing a MAC address may violate network policies or local laws depending on context. Always ensure you have permission before using this tool on any network. The author is not responsible for misuse.
