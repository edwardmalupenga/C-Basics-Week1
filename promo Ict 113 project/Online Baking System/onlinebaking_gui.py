import tkinter as tk
from tkinter import messagebox, ttk
import os
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from datetime import datetime


MAX_ACCOUNTS = 100
MAX_NAME_LEN = 100
MAX_PASS_LEN = 20
MAX_PHONE_LEN = 15
DEFAULT_DATA_DIR = Path.home() / ".online_banking"
DATA_DIR_ENV = os.environ.get("ONLINE_BANKING_DATA_DIR")
DATA_DIR = Path(DATA_DIR_ENV).expanduser() if DATA_DIR_ENV else DEFAULT_DATA_DIR
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILENAME = DATA_DIR / "bank_data.txt"
TRANSACTION_FILENAME = DATA_DIR / "transactions.txt"


@dataclass
class Account:
    full_name: str
    account_number: int
    password: str
    balance: float
    phone_number: str


@dataclass
class Transaction:
    account_number: int
    transaction_type: str  # "Deposit", "Withdrawal", "Transfer"
    amount: float
    balance_after: float
    timestamp: str
    recipient_account: Optional[int] = None  # For transfers


class OnlineBankingApp:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Online Baking System - Student Number: 2025557938")
        self.master.geometry("1080x720")
        self.master.state("zoomed")
        self.master.resizable(True, True)
        self.master.configure(bg="#0e1a2b")

        self.accounts: List[Account] = []
        self.logged_in_account: Optional[Account] = None
        self.transactions: List[Transaction] = []

        self._load_accounts()
        self._load_transactions()
        self._build_widgets()
        self._show_frame("welcome")

    # ---------------- Data Layer ---------------- #
    def _load_accounts(self) -> None:
        if not FILENAME.exists():
            self.accounts = []
            return

        loaded_accounts: List[Account] = []
        with FILENAME.open("r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                full_name, account_num, password, balance, phone = parts
                try:
                    account = Account(
                        full_name=full_name[:MAX_NAME_LEN],
                        account_number=int(account_num),
                        password=password[:MAX_PASS_LEN],
                        balance=float(balance),
                        phone_number=phone[:MAX_PHONE_LEN],
                    )
                except ValueError:
                    continue
                loaded_accounts.append(account)
        self.accounts = loaded_accounts[:MAX_ACCOUNTS]

    def _save_accounts(self) -> None:
        with FILENAME.open("w", encoding="utf-8") as file:
            for account in self.accounts:
                file.write(
                    f"{account.full_name} {account.account_number} "
                    f"{account.password} {account.balance:.2f} {account.phone_number}\n"
                )

    def _find_account(self, account_number: int) -> Optional[Account]:
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def _load_transactions(self) -> None:
        if not TRANSACTION_FILENAME.exists():
            self.transactions = []
            return

        loaded_transactions: List[Transaction] = []
        with TRANSACTION_FILENAME.open("r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 5:
                    try:
                        recipient = int(parts[5]) if len(parts) > 5 and parts[5].strip() else None
                        transaction = Transaction(
                            account_number=int(parts[0]),
                            transaction_type=parts[1],
                            amount=float(parts[2]),
                            balance_after=float(parts[3]),
                            timestamp=parts[4],
                            recipient_account=recipient
                        )
                        loaded_transactions.append(transaction)
                    except (ValueError, IndexError):
                        continue
        self.transactions = loaded_transactions

    def _save_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        with TRANSACTION_FILENAME.open("a", encoding="utf-8") as file:
            recipient = str(transaction.recipient_account) if transaction.recipient_account else ""
            file.write(
                f"{transaction.account_number}|{transaction.transaction_type}|"
                f"{transaction.amount}|{transaction.balance_after}|"
                f"{transaction.timestamp}|{recipient}\n"
            )

    # ---------------- UI Construction ---------------- #
    def _build_widgets(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0e1a2b")
        style.configure("TLabel", background="#0e1a2b", foreground="white", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 20))
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#1f3d5c")])
        style.configure("Card.TFrame", background="#13263c", relief="ridge", borderwidth=2)

        container = ttk.Frame(self.master)
        container.pack(expand=True, fill="both", padx=40, pady=40)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for frame_id in ("welcome", "register", "login", "dashboard"):
            frame = ttk.Frame(container, style="Card.TFrame", padding=30)
            self.frames[frame_id] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self._build_welcome_frame()
        self._build_register_frame()
        self._build_login_frame()
        self._build_dashboard_frame()

    def _build_welcome_frame(self) -> None:
        frame = self.frames["welcome"]

        ttk.Label(frame, text="Online Baking System\nStudent Number: 2025557938", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(
            frame,
            text="Securely manage your finances with confidence.",
            wraplength=420,
            justify="center",
        ).pack(pady=(0, 20))

        ttk.Button(frame, text="Login to Account", command=lambda: self._show_frame("login")).pack(
            fill="x", pady=10
        )
        ttk.Button(
            frame, text="Register New Account", command=lambda: self._show_frame("register")
        ).pack(fill="x", pady=10)

    def _build_register_frame(self) -> None:
        frame = self.frames["register"]
        ttk.Label(frame, text="Open a New Account", style="Header.TLabel").pack(pady=(0, 20))

        self.reg_full_name = tk.StringVar()
        self.reg_account_number = tk.StringVar()
        self.reg_phone = tk.StringVar()
        self.reg_password = tk.StringVar()
        self.reg_deposit = tk.StringVar()

        self._build_entry(frame, "Full Name (no spaces)", self.reg_full_name)
        self._build_entry(frame, "6-digit Account Number", self.reg_account_number)
        self._build_entry(frame, "Phone Number", self.reg_phone)
        self._build_entry(frame, "Password", self.reg_password, show="*")
        self._build_entry(frame, "Initial Deposit (min ZMW 10.00)", self.reg_deposit)

        ttk.Button(frame, text="Create Account", command=self._handle_register).pack(fill="x", pady=12)
        ttk.Button(frame, text="Back", command=lambda: self._show_frame("welcome")).pack(fill="x")

    def _build_login_frame(self) -> None:
        frame = self.frames["login"]
        ttk.Label(frame, text="Account Login", style="Header.TLabel").pack(pady=(0, 20))

        self.login_account_number = tk.StringVar()
        self.login_password = tk.StringVar()

        self._build_entry(frame, "Account Number", self.login_account_number)
        self._build_entry(frame, "Password", self.login_password, show="*")

        ttk.Button(frame, text="Login", command=self._handle_login).pack(fill="x", pady=12)
        ttk.Button(frame, text="Back", command=lambda: self._show_frame("welcome")).pack(fill="x")

    def _build_dashboard_frame(self) -> None:
        frame = self.frames["dashboard"]

        self.dashboard_header = ttk.Label(frame, text="", style="Header.TLabel")
        self.dashboard_header.pack(pady=(0, 10))

        self.dashboard_info = ttk.Label(frame, text="", justify="center")
        self.dashboard_info.pack(pady=(0, 20))

        btn_frame = ttk.Frame(frame, style="TFrame")
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(btn_frame, text="Deposit Funds", command=self._open_deposit_dialog).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Withdraw Funds", command=self._open_withdraw_dialog).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Transfer Funds", command=self._open_transfer_dialog).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Change Password", command=self._open_change_password_dialog).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Transaction History", command=self._show_transaction_history).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Show Account Details", command=self._show_account_details).pack(
            fill="x", pady=4
        )
        ttk.Button(btn_frame, text="Logout", command=self._logout).pack(fill="x", pady=(20, 0))

    def _build_entry(
        self, parent: ttk.Frame, label_text: str, variable: tk.StringVar, show: str = ""
    ) -> None:
        container = ttk.Frame(parent, style="TFrame")
        container.pack(fill="x", pady=6)
        ttk.Label(container, text=label_text).pack(anchor="w", pady=(0, 4))
        entry = ttk.Entry(container, textvariable=variable, show=show)
        entry.pack(fill="x")

    def _show_frame(self, frame_id: str) -> None:
        frame = self.frames[frame_id]
        frame.tkraise()
        if frame_id == "dashboard" and self.logged_in_account:
            account = self.logged_in_account
            self.dashboard_header.config(text=f"Welcome back, {account.full_name}")
            self.dashboard_info.config(
                text=(
            f"Account Number: {account.account_number}\n"
            f"Phone Number: {account.phone_number}\n"
            f"Current Balance: ZMW {account.balance:,.2f}"
                )
            )

    # ---------------- Event Handlers ---------------- #
    def _handle_register(self) -> None:
        if len(self.accounts) >= MAX_ACCOUNTS:
            messagebox.showerror("Registration", "The bank has reached its account capacity.")
            return

        full_name = self.reg_full_name.get().strip()
        account_number = self.reg_account_number.get().strip()
        phone = self.reg_phone.get().strip()
        password = self.reg_password.get().strip()
        deposit = self.reg_deposit.get().strip()

        if not all([full_name, account_number, phone, password, deposit]):
            messagebox.showwarning("Validation", "Please complete all fields.")
            return

        if " " in full_name or len(full_name) > MAX_NAME_LEN:
            messagebox.showwarning(
                "Validation", f"Full name must be a single word up to {MAX_NAME_LEN} characters."
            )
            return

        if not account_number.isdigit() or len(account_number) != 6:
            messagebox.showwarning("Validation", "Account number must be a 6-digit number.")
            return

        account_num_int = int(account_number)
        if self._find_account(account_num_int):
            messagebox.showwarning("Validation", "That account number already exists.")
            return

        if len(phone) > MAX_PHONE_LEN or " " in phone:
            messagebox.showwarning(
                "Validation", f"Phone number must be up to {MAX_PHONE_LEN} characters with no spaces."
            )
            return

        try:
            deposit_amount = float(deposit)
        except ValueError:
            messagebox.showwarning("Validation", "Deposit must be a valid number.")
            return

        if deposit_amount < 10.0:
            messagebox.showwarning("Validation", "Initial deposit must be at least ZMW 10.00.")
            return

        if len(password) > MAX_PASS_LEN:
            messagebox.showwarning(
                "Validation", f"Password must be up to {MAX_PASS_LEN} characters."
            )
            return

        new_account = Account(
            full_name=full_name,
            account_number=account_num_int,
            password=password,
            balance=deposit_amount,
            phone_number=phone,
        )
        self.accounts.append(new_account)
        self._save_accounts()

        # Record initial deposit as a transaction
        transaction = Transaction(
            account_number=account_num_int,
            transaction_type="Initial Deposit",
            amount=deposit_amount,
            balance_after=deposit_amount,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self._save_transaction(transaction)

        messagebox.showinfo(
            "Success",
            f"Welcome, {full_name}! Your account {account_number} is active.\nPhone: {phone}",
        )
        self._clear_registration_fields()
        self._show_frame("welcome")

    def _clear_registration_fields(self) -> None:
        self.reg_full_name.set("")
        self.reg_account_number.set("")
        self.reg_phone.set("")
        self.reg_password.set("")
        self.reg_deposit.set("")

    def _handle_login(self) -> None:
        account_number = self.login_account_number.get().strip()
        password = self.login_password.get().strip()

        if not (account_number and password):
            messagebox.showwarning("Login", "Please enter account number and password.")
            return

        if not account_number.isdigit():
            messagebox.showerror("Login", "Account number must be numeric.")
            return

        account = self._find_account(int(account_number))
        if account and account.password == password:
            self.logged_in_account = account
            messagebox.showinfo("Login Successful", f"Welcome, {account.full_name}.")
            self._show_frame("dashboard")
            self.login_account_number.set("")
            self.login_password.set("")
        else:
            messagebox.showerror("Login Failed", "Invalid account number or password.")

    def _require_login(self) -> bool:
        if not self.logged_in_account:
            messagebox.showerror("Authentication", "You must be logged in to perform this action.")
            return False
        return True

    def _open_deposit_dialog(self) -> None:
        if not self._require_login():
            return
        self._open_amount_dialog(
            title="Deposit Funds",
            action_label="Deposit",
            callback=self._deposit_funds,
        )

    def _open_withdraw_dialog(self) -> None:
        if not self._require_login():
            return
        self._open_amount_dialog(
            title="Withdraw Funds",
            action_label="Withdraw",
            callback=self._withdraw_funds,
        )

    def _open_transfer_dialog(self) -> None:
        if not self._require_login():
            return

        dialog = tk.Toplevel(self.master)
        dialog.title("Transfer Funds")
        dialog.geometry("360x260")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Recipient Account Number").pack(anchor="w", padx=20, pady=(20, 4))
        to_account_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=to_account_var).pack(fill="x", padx=20)

        ttk.Label(dialog, text="Amount").pack(anchor="w", padx=20, pady=(16, 4))
        amount_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=amount_var).pack(fill="x", padx=20)

        ttk.Button(
            dialog,
            text="Transfer",
            command=lambda: self._transfer_funds(dialog, to_account_var.get(), amount_var.get()),
        ).pack(fill="x", padx=20, pady=(24, 10))

    def _open_change_password_dialog(self) -> None:
        if not self._require_login():
            return

        dialog = tk.Toplevel(self.master)
        dialog.title("Change Password")
        dialog.geometry("360x260")
        dialog.resizable(False, False)

        old_pass_var = tk.StringVar()
        new_pass_var = tk.StringVar()
        confirm_pass_var = tk.StringVar()

        self._password_entry(dialog, "Current Password", old_pass_var)
        self._password_entry(dialog, "New Password", new_pass_var)
        self._password_entry(dialog, "Confirm New Password", confirm_pass_var)

        ttk.Button(
            dialog,
            text="Update Password",
            command=lambda: self._change_password(
                dialog, old_pass_var.get(), new_pass_var.get(), confirm_pass_var.get()
            ),
        ).pack(fill="x", padx=20, pady=(24, 10))

    def _password_entry(self, parent: tk.Toplevel, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=label).pack(anchor="w", padx=20, pady=(16, 4))
        ttk.Entry(parent, textvariable=variable, show="*").pack(fill="x", padx=20)

    def _open_amount_dialog(self, title: str, action_label: str, callback) -> None:
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("320x200")
        dialog.resizable(False, False)

        amount_var = tk.StringVar()

        ttk.Label(dialog, text="Amount").pack(anchor="w", padx=20, pady=(20, 4))
        ttk.Entry(dialog, textvariable=amount_var).pack(fill="x", padx=20)

        ttk.Button(
            dialog,
            text=action_label,
            command=lambda: callback(dialog, amount_var.get()),
        ).pack(fill="x", padx=20, pady=(24, 10))

    def _deposit_funds(self, dialog: tk.Toplevel, amount_text: str) -> None:
        if not self.logged_in_account:
            return
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showwarning("Deposit", "Please enter a valid amount.")
            return

        if amount <= 0:
            messagebox.showwarning("Deposit", "Amount must be positive.")
            return

        self.logged_in_account.balance += amount
        self._save_accounts()
        
        # Record transaction
        transaction = Transaction(
            account_number=self.logged_in_account.account_number,
            transaction_type="Deposit",
            amount=amount,
            balance_after=self.logged_in_account.balance,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self._save_transaction(transaction)
        
        messagebox.showinfo("Deposit", f"ZMW {amount:,.2f} added to your account.")
        dialog.destroy()
        self._show_frame("dashboard")

    def _withdraw_funds(self, dialog: tk.Toplevel, amount_text: str) -> None:
        if not self.logged_in_account:
            return
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showwarning("Withdrawal", "Please enter a valid amount.")
            return

        if amount <= 0:
            messagebox.showwarning("Withdrawal", "Amount must be positive.")
            return

        if self.logged_in_account.balance < amount:
            messagebox.showerror(
                "Withdrawal",
                f"Insufficient funds. Available balance is ZMW {self.logged_in_account.balance:,.2f}.",
            )
            return

        self.logged_in_account.balance -= amount
        self._save_accounts()
        
        # Record transaction
        transaction = Transaction(
            account_number=self.logged_in_account.account_number,
            transaction_type="Withdrawal",
            amount=amount,
            balance_after=self.logged_in_account.balance,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self._save_transaction(transaction)
        
        messagebox.showinfo("Withdrawal", f"ZMW {amount:,.2f} withdrawn successfully.")
        dialog.destroy()
        self._show_frame("dashboard")

    def _transfer_funds(
        self, dialog: tk.Toplevel, recipient_text: str, amount_text: str
    ) -> None:
        if not self.logged_in_account:
            return

        if not recipient_text.isdigit():
            messagebox.showwarning("Transfer", "Recipient account number must be numeric.")
            return

        recipient_account = self._find_account(int(recipient_text))
        if not recipient_account:
            messagebox.showerror("Transfer", "Recipient account not found.")
            return

        if recipient_account.account_number == self.logged_in_account.account_number:
            messagebox.showwarning("Transfer", "Please use Deposit/Withdrawal for self-account.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showwarning("Transfer", "Please enter a valid amount.")
            return

        if amount <= 0:
            messagebox.showwarning("Transfer", "Amount must be positive.")
            return

        if self.logged_in_account.balance < amount:
            messagebox.showerror("Transfer", "Insufficient funds for this transfer.")
            return

        self.logged_in_account.balance -= amount
        recipient_account.balance += amount
        self._save_accounts()
        
        # Record transaction for sender
        sender_transaction = Transaction(
            account_number=self.logged_in_account.account_number,
            transaction_type="Transfer",
            amount=amount,
            balance_after=self.logged_in_account.balance,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            recipient_account=recipient_account.account_number
        )
        self._save_transaction(sender_transaction)
        
        # Record transaction for recipient
        recipient_transaction = Transaction(
            account_number=recipient_account.account_number,
            transaction_type="Transfer Received",
            amount=amount,
            balance_after=recipient_account.balance,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            recipient_account=self.logged_in_account.account_number
        )
        self._save_transaction(recipient_transaction)
        
        messagebox.showinfo(
            "Transfer",
            f"ZMW {amount:,.2f} transferred to {recipient_account.full_name} "
            f"(Acc: {recipient_account.account_number}).",
        )
        dialog.destroy()
        self._show_frame("dashboard")

    def _change_password(
        self, dialog: tk.Toplevel, old_password: str, new_password: str, confirm_password: str
    ) -> None:
        if not self.logged_in_account:
            return

        if not all([old_password, new_password, confirm_password]):
            messagebox.showwarning("Password", "All fields are required.")
            return

        if self.logged_in_account.password != old_password:
            messagebox.showerror("Password", "Current password is incorrect.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Password", "New passwords did not match.")
            return

        if len(new_password) > MAX_PASS_LEN:
            messagebox.showwarning(
                "Password", f"Password must be up to {MAX_PASS_LEN} characters."
            )
            return

        self.logged_in_account.password = new_password
        self._save_accounts()
        messagebox.showinfo("Password", "Password updated successfully.")
        dialog.destroy()

    def _show_account_details(self) -> None:
        if not self._require_login():
            return

        account = self.logged_in_account
        messagebox.showinfo(
            "Account Details",
            f"Holder: {account.full_name}\n"
            f"Account Number: {account.account_number}\n"
            f"Phone Number: {account.phone_number}\n"
            f"Current Balance: ZMW {account.balance:,.2f}\n"
            f"Security: Password hash is hidden from view.",
        )

    def _show_transaction_history(self) -> None:
        if not self._require_login():
            return

        # Filter transactions for the logged-in account
        account_transactions = [
            t for t in self.transactions
            if t.account_number == self.logged_in_account.account_number
        ]

        if not account_transactions:
            messagebox.showinfo("Transaction History", "No transactions found for this account.")
            return

        # Create a new window to display transaction history
        history_window = tk.Toplevel(self.master)
        history_window.title("Transaction History")
        history_window.geometry("800x500")
        history_window.configure(bg="#0e1a2b")

        # Create a frame with scrollbar
        main_frame = ttk.Frame(history_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_label = ttk.Label(
            main_frame,
            text=f"Transaction History - Account: {self.logged_in_account.account_number}",
            font=("Segoe UI Semibold", 14)
        )
        header_label.pack(pady=(0, 10))

        # Create a canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg="#13263c", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display transactions (most recent first)
        account_transactions.sort(key=lambda x: x.timestamp, reverse=True)

        for transaction in account_transactions:
            transaction_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
            transaction_frame.pack(fill="x", pady=5, padx=5)

            # Transaction type and amount
            type_color = "#4CAF50" if transaction.transaction_type in ["Deposit", "Transfer Received", "Initial Deposit"] else "#F44336"
            type_label = ttk.Label(
                transaction_frame,
                text=f"{transaction.transaction_type}",
                font=("Segoe UI", 11, "bold"),
                foreground=type_color
            )
            type_label.pack(anchor="w", padx=10, pady=(5, 0))

            # Amount
            amount_label = ttk.Label(
                transaction_frame,
                text=f"Amount: ZMW {transaction.amount:,.2f}",
                font=("Segoe UI", 10)
            )
            amount_label.pack(anchor="w", padx=10)

            # Balance after
            balance_label = ttk.Label(
                transaction_frame,
                text=f"Balance After: ZMW {transaction.balance_after:,.2f}",
                font=("Segoe UI", 10)
            )
            balance_label.pack(anchor="w", padx=10)

            # Recipient (for transfers)
            if transaction.recipient_account:
                recipient_text = "To" if transaction.transaction_type == "Transfer" else "From"
                recipient_label = ttk.Label(
                    transaction_frame,
                    text=f"{recipient_text} Account: {transaction.recipient_account}",
                    font=("Segoe UI", 9),
                    foreground="#888888"
                )
                recipient_label.pack(anchor="w", padx=10)

            # Timestamp
            timestamp_label = ttk.Label(
                transaction_frame,
                text=f"Date: {transaction.timestamp}",
                font=("Segoe UI", 9),
                foreground="#888888"
            )
            timestamp_label.pack(anchor="w", padx=10, pady=(0, 5))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Close button
        close_button = ttk.Button(
            history_window,
            text="Close",
            command=history_window.destroy
        )
        close_button.pack(pady=10)

    def _logout(self) -> None:
        if self.logged_in_account:
            name = self.logged_in_account.full_name
            self.logged_in_account = None
            messagebox.showinfo("Logout", f"{name}, you have been logged out.")
            self._show_frame("welcome")


def main() -> None:
    root = tk.Tk()
    OnlineBankingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

