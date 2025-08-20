import tkinter as tk
from tkinter import simpledialog, messagebox

# ------------------------
# Base BankAccount Class (Encapsulation + Abstraction)
# ------------------------
class BankAccount:
    def __init__(self, acc_num, holder_name, balance=0):
        self._acc_num = acc_num
        self._holder_name = holder_name
        self._balance = balance

    @property
    def acc_num(self): return self._acc_num

    @property
    def holder_name(self): return self._holder_name

    @property
    def balance(self): return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def display(self):
        return f"{self._acc_num}: {self._holder_name} - ₹{self._balance}"

# ------------------------
# SavingsAccount (Inheritance + Polymorphism)
# ------------------------
class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= 500:
            self._balance -= amount
            return True
        return False

# ------------------------
# BankingSystem Class (Manages All Accounts)
# ------------------------
class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self._next_acc = 1001

    def generate_account_number(self):
        acc = f"ACC{self._next_acc}"
        self._next_acc += 1
        return acc

    def create_account(self, name, acc_type):
        acc_num = self.generate_account_number()
        account = SavingsAccount(acc_num, name) if acc_type == "savings" else BankAccount(acc_num, name)
        self.accounts[acc_num] = account
        return acc_num

    def get_account(self, acc_num):
        return self.accounts.get(acc_num)

# ------------------------
# BankingApp Class (GUI)
# ------------------------
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.bank = BankingSystem()
        self.root.title("🏦 Banking System")
        self.root.geometry("750x550")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        self.output = tk.Text(frame, width=85, height=20, bg="#f2f2f2")
        self.output.pack(pady=10)

        button_frame = tk.Frame(frame)
        button_frame.pack()

        buttons = [
            ("➕ Open Account", self.create_account_ui),
            ("💰 Deposit", self.deposit_ui),
            ("💸 Withdraw", self.withdraw_ui),
            ("📄 Show Accounts", self.show_accounts),
            ("🔍 Check Balance", self.check_balance_ui)
        ]

        for label, command in buttons:
            tk.Button(button_frame, text=label, width=30, bg="#e2f0cb", command=command).pack(pady=5)

    def create_account_ui(self):
        name = simpledialog.askstring("Account Holder", "Enter holder name:")
        acc_type = simpledialog.askstring("Account Type", "Type (savings/current):").lower()
        if acc_type not in ['savings', 'current']:
            messagebox.showerror("Error", "Invalid account type!")
            return
        acc_num = self.bank.create_account(name, acc_type)
        self.output.insert(tk.END, f"✅ Account created: {acc_num} ({acc_type})\n")

    def deposit_ui(self):
        acc_num = simpledialog.askstring("Deposit", "Enter Account Number:")
        account = self.bank.get_account(acc_num)
        if not account:
            messagebox.showerror("Error", "Account not found.")
            return
        amount = simpledialog.askfloat("Amount", "Enter amount to deposit:")
        if account.deposit(amount):
            self.output.insert(tk.END, f"💰 Deposited ₹{amount} to {acc_num}\n")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def withdraw_ui(self):
        acc_num = simpledialog.askstring("Withdraw", "Enter Account Number:")
        account = self.bank.get_account(acc_num)
        if not account:
            messagebox.showerror("Error", "Account not found.")
            return
        amount = simpledialog.askfloat("Amount", "Enter amount to withdraw:")
        if account.withdraw(amount):
            self.output.insert(tk.END, f"💸 Withdrawn ₹{amount} from {acc_num}\n")
        else:
            messagebox.showerror("Error", "Insufficient balance or rules violated.")

    def show_accounts(self):
        self.output.insert(tk.END, "\n📋 --- All Accounts ---\n")
        for acc in self.bank.accounts.values():
            self.output.insert(tk.END, acc.display() + "\n")

    def check_balance_ui(self):
        acc_num = simpledialog.askstring("Balance Check", "Enter Account Number:")
        account = self.bank.get_account(acc_num)
        if account:
            self.output.insert(tk.END, f"💼 {acc_num} Balance: ₹{account.balance}\n")
        else:
            messagebox.showerror("Error", "Account not found.")

# ------------------------
# Main Entry Point
# ------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()