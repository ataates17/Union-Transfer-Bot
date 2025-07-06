#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
from web3 import Web3
from eth_account import Account
from datetime import datetime

# Ethereum RPC URL (Infura, Alchemy, etc.)
RPC_URL = "https://ethereum-holesky-rpc.publicnode.com"  # Add your own API key
# For testnet: "https://sepolia.infura.io/v3/YOUR_API_KEY"

# Contract address
CONTRACT_ADDRESS = "0x5FbE74A283f7954f10AA04C2eDf55578811aeb03"

# Gas settings
GAS_LIMIT = 500000
GAS_PRICE = None  # Auto-calculate if None

def load_wallets():
    """
    Reads wallet information from wallet.txt file
    Format: address,private_key
    """
    wallets = []
    try:
        with open("wallet.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(",")
                    if len(parts) >= 2:
                        address = parts[0].strip()
                        private_key = parts[1].strip()
                        wallets.append({
                            "address": address,
                            "private_key": private_key
                        })
    except FileNotFoundError:
        print("wallet.txt file not found!")
        return []
    return wallets

def get_gas_price(w3):
    """
    Gets gas price
    """
    try:
        gas_price = w3.eth.gas_price
        return gas_price
    except Exception as e:
        print(f"Gas price could not be retrieved, using default: {e}")
        return 20000000000  # 20 Gwei

def get_nonce(w3, address):
    """
    Gets wallet nonce value
    """
    try:
        nonce = w3.eth.get_transaction_count(address)
        return nonce
    except Exception as e:
        print(f"Nonce could not be retrieved: {e}")
        return 0

def create_transaction(w3, wallet, tx_data):
    """
    Creates transaction
    """
    try:
        # Get gas price
        gas_price = GAS_PRICE or get_gas_price(w3)
        
        # Get nonce
        nonce = get_nonce(w3, wallet["address"])
        
        # Create transaction
        transaction = {
            'to': CONTRACT_ADDRESS,
            'value': 10913304046004750,  # In Wei
            'gas': GAS_LIMIT,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data,
            'chainId': 17000  # Mainnet, for testnet use 11155111 (Sepolia)
        }
        
        return transaction, nonce
        
    except Exception as e:
        print(f"Transaction could not be created: {e}")
        return None, None

def send_transaction(w3, wallet, transaction):
    """
    Sends transaction
    """
    try:
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, wallet["private_key"])
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"Transaction could not be sent: {e}")
        return None

def wait_for_transaction(w3, tx_hash, max_wait=300):
    """
    Waits for transaction confirmation
    """
    print(f"Waiting for transaction: {tx_hash}")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                if receipt['status'] == 1:
                    print(f"Transaction successful! Block: {receipt['blockNumber']}")
                    return True
                else:
                    print(f"Transaction failed!")
                    return False
        except:
            pass
        
        time.sleep(5)
    
    print(f"Timeout! Transaction status could not be verified.")
    return False

def main():
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            print("Web3 connection could not be established!")
            return
    except Exception as e:
        print(f"Web3 connection error: {e}")
        return
    wallets = load_wallets()
    if not wallets:
        print("No wallets found!")
        return
    for wallet in wallets:
        try:
            current_time = int(time.time())
            deadline = current_time + (72 * 3600)
            wallet_address = wallet["address"]
            formatted_signature = "0" * 64
            tx_data = (
                "0xff0d7c2f"
                + "0000000000000000000000000000000000000000000000000000000000000002"
                + "0000000000000000000000000000000000000000000000000000000000000000"
                + f"{deadline:064x}"
                + formatted_signature
                + "00000000000000000000000000000000000000000000000000000000000000a0"
                + "0000000000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000002"
                + "0000000000000000000000000000000000000000000000000000000000000060"
                + "0000000000000000000000000000000000000000000000000000000000000700"
                + "0000000000000000000000000000000000000000000000000000000000000020"
                + "0000000000000000000000000000000000000000000000000000000000000002"
                + "0000000000000000000000000000000000000000000000000000000000000040"
                + "0000000000000000000000000000000000000000000000000000000000000380"
                + "0000000000000000000000000000000000000000000000000000000000000001"
                + "0000000000000000000000000000000000000000000000000000000000000003"
                + "0000000000000000000000000000000000000000000000000000000000000060"
                + "00000000000000000000000000000000000000000000000000000000000002c0"
                + "0000000000000000000000000000000000000000000000000000000000000140"
                + "0000000000000000000000000000000000000000000000000000000000000180"
                + "00000000000000000000000000000000000000000000000000000000000001c0"
                + "00000000000000000000000000000000000000000000000000038d7ea4c68000"
                + "0000000000000000000000000000000000000000000000000000000000000200"
                + "0000000000000000000000000000000000000000000000000000000000000240"
                + "0000000000000000000000000000000000000000000000000000000000000012"
                + "0000000000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000280"
                + "00000000000000000000000000000000000000000000000000038d7ea4c68000"
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + wallet_address[2:].zfill(64)
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + wallet_address[2:].zfill(64)
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000003"
                + "4554480000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000005"
                + "4574686572000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + "f6E7E2725b40EC8226036906cAb0f5dC3722b8E7000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000001"
                + "0000000000000000000000000000000000000000000000000000000000000003"
                + "0000000000000000000000000000000000000000000000000000000000000060"
                + "00000000000000000000000000000000000000000000000000000000000002c0"
                + "0000000000000000000000000000000000000000000000000000000000000140"
                + "0000000000000000000000000000000000000000000000000000000000000180"
                + "00000000000000000000000000000000000000000000000000000000000001c0"
                + "000000000000000000000000000000000000000000000000000002e406abe040"
                + "0000000000000000000000000000000000000000000000000000000000000200"
                + "0000000000000000000000000000000000000000000000000000000000000240"
                + "0000000000000000000000000000000000000000000000000000000000000012"
                + "0000000000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000280"
                + "0000000000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + wallet_address[2:].zfill(64)
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + wallet_address[2:].zfill(64)
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000003"
                + "4554480000000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000005"
                + "4574686572000000000000000000000000000000000000000000000000000000"
                + "0000000000000000000000000000000000000000000000000000000000000014"
                + "f6E7E2725b40EC8226036906cAb0f5dC3722b8E7000000000000000000000000"
            )
            print("Sending transaction...")
            transaction, nonce = create_transaction(w3, wallet, tx_data)
            if not transaction:
                print("Transaction could not be created.")
                continue
            tx_hash = send_transaction(w3, wallet, transaction)
            if not tx_hash:
                print("Transaction could not be sent.")
                continue
            print("Transaction sent, waiting for confirmation...")
            result = wait_for_transaction(w3, tx_hash)
            if result:
                print("Transaction confirmed.")
            else:
                print("Transaction not confirmed.")
        except Exception as e:
            print(f"Error in transaction: {e}")

if __name__ == "__main__":
    main()
