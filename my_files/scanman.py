#!/usr/bin/env python3

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='scanman.log',
    level=logging.DEBUG,  # Log detailed messages
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ASCII Banner
def print_banner():
    print(r"""
  █████████                                ██████   ██████                     
 ███░░░░░███                              ░░██████ ██████                      
░███    ░░░   ██████   ██████   ████████   ░███░█████░███   ██████   ████████  
░░█████████  ███░░███ ░░░░░███ ░░███░░███  ░███░░███ ░███  ░░░░░███ ░░███░░███ 
 ░░░░░░░░███░███ ░░░   ███████  ░███ ░███  ░███ ░░░  ░███   ███████  ░███ ░███ 
 ███    ░███░███  ███ ███░░███  ░███ ░███  ░███      ░███  ███░░███  ░███ ░███ 
░░█████████ ░░██████ ░░████████ ████ █████ █████     █████░░████████ ████ █████
 ░░░░░░░░░   ░░░░░░   ░░░░░░░░ ░░░░ ░░░░░ ░░░░░     ░░░░░  ░░░░░░░░ ░░░░ ░░░░░ 
ScanMan: Your Ultimate Enumeration Toolkit
    """)

# Function to add entries to /etc/hosts
def add_to_hosts(ip_address, hostnames, verbose=False):
    try:
        line_to_add = f"{ip_address} {' '.join(hostnames)}"
        print(f"Adding the following entry to /etc/hosts:\n{line_to_add}")
        logging.info(f"Command: Adding to /etc/hosts: {line_to_add}")
        with open('/etc/hosts', 'a') as hosts_file:
            hosts_file.write(f"{line_to_add}\n")
        print("Successfully added to /etc/hosts.")
    except PermissionError as e:
        error_msg = f"Permission denied: {e}"
        logging.error(error_msg)
        print("Permission denied. Please run the script with sudo.")

# Function to run Rustscan
def run_rustscan(target, verbose=False):
    command = ["rustscan", "-a", target, "--", "-A", "-oN", "nmap.txt"]
    if verbose:
        command.append("-v")
    try:
        logging.info(f"Command: {' '.join(command)}")
        print(f"Running Rustscan on target: {target}")
        subprocess.run(command, check=True)
        print("Rustscan completed successfully. Output saved to nmap.txt.")
        logging.info("Rustscan completed successfully.")
    except FileNotFoundError as e:
        error_msg = f"Rustscan not found: {e}"
        logging.error(error_msg)
        print("Rustscan not found. Please ensure it is installed.")
    except subprocess.CalledProcessError as e:
        error_msg = f"Rustscan execution failed: {e}"
        logging.error(error_msg)
        print("Rustscan failed to execute.")

# Function to run Dirb
def run_dirb(ip_address, port, verbose=False):
    protocol = "http" if port == "80" else "https"
    wordlist = "/usr/share/dirb/wordlists/common.txt"  # Default wordlist
    command = ["dirb", f"{protocol}://{ip_address}:{port}/", wordlist]
    if verbose:
        command.append("-v")
    try:
        logging.info(f"Command: {' '.join(command)}")
        print(f"Running Dirb with the following command:\n{' '.join(command)}")
        subprocess.run(command, check=True)
        print("Dirb completed successfully.")
        logging.info("Dirb completed successfully.")
    except FileNotFoundError as e:
        error_msg = f"Dirb not found: {e}"
        logging.error(error_msg)
        print("Dirb not found. Please ensure it is installed.")
    except subprocess.CalledProcessError as e:
        error_msg = f"Dirb execution failed: {e}"
        logging.error(error_msg)
        print("Dirb failed to execute.")

# Function to parse nmap.txt and extract relevant ports
def parse_nmap():
    ports = []
    try:
        with open("nmap.txt", "r") as file:
            for line in file:
                if "open" in line and ("80/tcp" in line or "443/tcp" in line):
                    if "80/tcp" in line:
                        ports.append(80)
                    elif "443/tcp" in line:
                        ports.append(443)
        logging.info(f"Parsed ports from nmap.txt: {ports}")
        return ports
    except FileNotFoundError as e:
        error_msg = f"nmap.txt not found: {e}"
        logging.error(error_msg)
        print("nmap.txt not found. Ensure Rustscan was executed successfully.")
        return ports

# Function for automation
def automate(ip_address, hostname, verbose=False):
    print("Starting automation process...")
    logging.info(f"Starting automation for IP: {ip_address}, Hostname: {hostname}")
    
    # Add to /etc/hosts
    add_to_hosts(ip_address, [hostname], verbose)

    # Run Rustscan
    run_rustscan(hostname, verbose)

    # Parse Rustscan output
    ports = parse_nmap()
    if not ports:
        print("No relevant ports found in nmap.txt. Automation aborted.")
        logging.warning("Automation aborted: No relevant ports found.")
        return

    # Run Dirb on detected ports
    for port in ports:
        print(f"Running Dirb on port {port}...")
        run_dirb(ip_address, str(port), verbose)

# Main function
def main():
    print_banner()
    if len(sys.argv) < 2:
        print("Usage: script.py [options]")
        print("Options:")
        print("  -a, --add-to-hosts <IP_ADDRESS> <HOSTNAME(S)>  Add an entry to the /etc/hosts file.")
        print("  -r, --rustscan <TARGET>                       Run rustscan on the specified target.")
        print("  -d, --dirb <IP_ADDRESS> <PORT>               Run dirb on the specified IP and port.")
        print("  --automate <IP_ADDRESS> <HOSTNAME>           Automate the entire process.")
        print("  -l, --log                                    Enable logging of commands and outputs.")
        print("  -v, --verbose                                Enable verbose mode for selected command.")
        print("  -h, --help                                   Display this help message.")
        return

    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    if sys.argv[1] in ('-a', '--add-to-hosts'):
        if len(sys.argv) < 4:
            print("Error: Insufficient arguments for -a|--add-to-hosts.")
            print("Usage: script.py -a <IP_ADDRESS> <HOSTNAME(S)>")
            return
        ip_address = sys.argv[2]
        hostnames = sys.argv[3:]
        add_to_hosts(ip_address, hostnames, verbose)

    elif sys.argv[1] in ('-r', '--rustscan'):
        if len(sys.argv) < 3:
            print("Error: Insufficient arguments for -r|--rustscan.")
            print("Usage: script.py -r <TARGET>")
            return
        target = sys.argv[2]
        run_rustscan(target, verbose)

    elif sys.argv[1] in ('-d', '--dirb'):
        if len(sys.argv) < 4:
            print("Error: Insufficient arguments for -d|--dirb.")
            print("Usage: script.py -d <IP_ADDRESS> <PORT>")
            return
        ip_address = sys.argv[2]
        port = sys.argv[3]
        run_dirb(ip_address, port, verbose)

    elif sys.argv[1] in ('--automate'):
        if len(sys.argv) < 4:
            print("Error: Insufficient arguments for --automate.")
            print("Usage: script.py --automate <IP_ADDRESS> <HOSTNAME>")
            return
        ip_address = sys.argv[2]
        hostname = sys.argv[3]
        automate(ip_address, hostname, verbose)

    elif sys.argv[1] in ('-l', '--log'):
        logging.info("Logging enabled.")
        print("Logging is already configured. All commands and outputs will be logged.")

    elif sys.argv[1] in ('-h', '--help'):
        print("Usage: script.py [options]")
        print("Options:")
        print("  -a, --add-to-hosts <IP_ADDRESS> <HOSTNAME(S)>  Add an entry to the /etc/hosts file.")
        print("  -r, --rustscan <TARGET>                       Run rustscan on the specified target.")
        print("  -d, --dirb <IP_ADDRESS> <PORT>               Run dirb on the specified IP and port.")
        print("  --automate <IP_ADDRESS> <HOSTNAME>           Automate the entire process.")
        print("  -l, --log                                    Enable logging of commands and outputs.")
        print("  -v, --verbose                                Enable verbose mode for selected command.")
        print("  -h, --help                                   Display this help message.")
    else:
        print(f"Invalid option: {sys.argv[1]}")
        print

if __name__ == main():
    main()