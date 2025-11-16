# Promo ICT 113 Project

## Online Baking System

A comprehensive banking system application developed as part of the ICT 113 course project.

**Student Number:** 2025557938

### Project Structure

```
promo Ict 113 project/
├── Online Baking System/
│   ├── onlinebaking_gui.py    # Python GUI application (Tkinter)
│   ├── onlinebaking.c          # C language implementation
│   ├── onlinebaking.exe        # Compiled executable
│   ├── onlinebaking.spec      # PyInstaller specification
│   └── README.md               # Detailed documentation
└── README.md                   # This file
```

### Features

- **Account Management**
  - User registration with account number, password, and phone number
  - Secure login system
  - Account details viewing

- **Financial Operations**
  - Deposit funds
  - Withdraw funds
  - Transfer funds between accounts
  - Transaction history tracking

- **Security**
  - Password protection
  - Password change functionality
  - Account authentication

- **Transaction History**
  - View all transactions for your account
  - Detailed transaction information with timestamps
  - Color-coded transaction types (deposits/withdrawals/transfers)

### Technologies Used

- **Python** - GUI application using Tkinter
- **C** - Console-based implementation
- **File I/O** - Persistent data storage

### Getting Started

#### Python GUI Version
1. Ensure Python 3.9+ is installed
2. Navigate to the `Online Baking System` directory
3. Run: `python onlinebaking_gui.py`

#### C Console Version
1. Compile the C file: `gcc onlinebaking.c -o onlinebaking`
2. Run the executable: `./onlinebaking` (Linux/Mac) or `onlinebaking.exe` (Windows)

### Data Storage

- Account data is stored in: `~/.online_banking/bank_data.txt`
- Transaction history is stored in: `~/.online_banking/transactions.txt`
- Data persists between application sessions

### Requirements

- Python 3.9+ (for GUI version)
- Tkinter (usually bundled with Python)
- GCC compiler (for C version)

### Author

Student Number: 2025557938

### License

This project is part of an academic course assignment.

