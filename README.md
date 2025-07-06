# 🚀 Union Transaction Bot

An automated Union transaction bot that sends transactions with customizable intervals and transaction counts.

## ⚠️ Warning

**This bot performs real Ethereum transactions with real wallets and real funds. Use at your own risk!**

- Always test with small amounts first
- Use test wallets initially
- Keep your private keys secure
- This bot is for educational purposes

## 📋 Features

- 🔄 **Automated Transactions**: Send multiple transactions automatically
- ⏱️ **Customizable Intervals**: Set wait time between transactions (10-60 seconds)
- 📊 **Transaction Tracking**: Monitor successful and failed transactions
- 🛡️ **Safety Checks**: File validation and user confirmation
- 📈 **Progress Monitoring**: Real-time transaction status updates

## 🛠️ Requirements

### System Requirements
- Python 3.7 or higher
- Windows/Linux/macOS
- Internet connection for Ethereum RPC

### Python Packages
```
web3>=6.0.0
eth-account>=0.8.0
```

## 📦 Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd ethereum-transaction-bot
```

### 2. Install Python Dependencies
```bash
pip install web3 eth-account
```

### 3. Create Required Files

#### wallet.txt
Create a `wallet.txt` file with your wallet information:
```
0x1234567890abcdef1234567890abcdef12345678,abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef

```

**Format**: `address,private_key` (one wallet per line)

#### transfer.py
The `transfer.py` file should already be present in the repository.

## ⚙️ Configuration

### RPC Settings
Edit `transfer.py` to configure your Ethereum RPC endpoint:

```python
# Ethereum RPC URL (Infura, Alchemy, etc.)
RPC_URL = "https://ethereum-holesky-rpc.publicnode.com"  # Testnet
# For mainnet: "https://mainnet.infura.io/v3/YOUR_API_KEY"

# Contract address
CONTRACT_ADDRESS = "0x5FbE74A283f7954f10AA04C2eDf55578811aeb03"

# Gas settings
GAS_LIMIT = 500000
GAS_PRICE = None  # Auto-calculate if None
```

### Network Configuration
- **Testnet (Holesky)**: Chain ID 17000


## 🚀 Usage

### 1. Start the Bot
```bash
python main.py
```

### 2. Main Menu Options
```
📋 MAIN MENU
1. 🚀 Start Transactions
2. 📖 Help
3. ❌ Exit
```

### 3. Transaction Settings
When you select "Start Transactions", you'll be prompted for:

- **Transaction Count**: Number of transactions (1-100)
- **Wait Time**: Seconds between transactions (10-60)

### 4. Confirmation
The bot will show a summary and ask for confirmation:
```
📋 Transaction Summary:
   🔄 Total Transactions: 5
   ⏱️  Transaction Interval: 15 seconds
   ⏰ Estimated Time: 75 seconds (1.3 minutes)

❓ Do you want to start the transactions? (y/n):
```

## 📊 Transaction Flow

1. **File Validation**: Checks for required files
2. **Wallet Loading**: Reads wallet.txt
3. **Transaction Creation**: Generates tx data with dynamic values
4. **Transaction Sending**: Signs and sends to network
5. **Confirmation**: Waits for transaction confirmation
6. **Progress Tracking**: Shows success/failure status

## 🔧 Dynamic Values

The bot automatically sets these values for each transaction:

- **Deadline**: Current time + 72 hours (3 days)
- **Wallet Address**: From wallet.txt (formatted for ABI)
- **Signature**: Empty signature (64 zeros)

## 📁 File Structure

```
ethereum-transaction-bot/
├── main.py              # Main bot interface
├── transfer.py          # Transaction logic
├── wallet.txt           # Wallet configuration
└── README.md            # This file
```

## 🛡️ Security Best Practices

1. **Test First**: Always test with small amounts
2. **Secure Keys**: Never share private keys
3. **Test Networks**: Use testnets before mainnet
4. **Backup**: Keep wallet backups secure
5. **Monitor**: Watch transactions carefully

## ❗ Troubleshooting

### Common Issues

**"Missing files" error**
- Ensure `transfer.py` and `wallet.txt` exist
- Check file permissions

**"Web3 connection failed"**
- Verify RPC URL is correct
- Check internet connection
- Try different RPC endpoint

**"Transaction failed"**
- Check wallet balance
- Verify gas settings
- Ensure contract address is correct

### Error Messages

- `❌ Missing files`: Required files not found
- `❌ Web3 connection failed`: RPC connection issue
- `❌ Transaction failed`: Transaction rejected by network
- `⚠️ Bot stopped by user`: User interrupted with Ctrl+C

## 📝 Transaction Data Format


```
0xff0d7c2f + [deadline] + [signature] + [wallet_address] + [fixed_values]
```

- **Function Selector**: `0xff0d7c2f`
- **Deadline**: Dynamic timestamp
- **Signature**: Empty (64 zeros)
- **Wallet Address**: Formatted for ABI
- **Fixed Values**: Predefined hex values

## 🔄 Supported Networks

- **Ethereum Mainnet** (Chain ID: 1)
- **Holesky Testnet** (Chain ID: 17000)
- **Sepolia Testnet** (Chain ID: 11155111)

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Test with small amounts first
4. Verify all configuration settings

## 📄 License

This project is for educational purposes. Use responsibly and at your own risk.

## ⚠️ Disclaimer

This bot is provided as-is without any guarantees. Users are responsible for:
- Securing their private keys
- Understanding transaction risks
- Complying with local regulations
- Testing thoroughly before use

**Never use this bot with funds you cannot afford to lose!** 
