from datetime import datetime, timedelta
import random
import os


FILENAME = "accounts.txt"

class BankAccount:
    tot_acct = 5
    def __init__(self, usnm, id, bal, card_number=None, cvv2=None, expiry=None, pin=None, transactions=None, username=None, password=None):
        self.name = usnm
        self.id = id
        self.balance = bal
        self.card_number = card_number
        self.cvv2 = cvv2            # عدد سه یا چهار رقمی
        self.expiry = expiry        # رشته MM/YY
        self.pin = pin              # رمز کارت (4 یا 6 رقمی)
        self.transactions = transactions if transactions else []
        self.username = username    # ?
        self.password = password    # ?

    def add_transaction(self, sign, amount, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {sign}${amount} - {description}"
        self.transactions.append(entry)
        if len(self.transactions) > 10:
            self.transactions.pop(0)

    def transfer(self, to, amt):
        if amt > self.balance:
            raise RuntimeError("Amount greater than available balance.")
        self.balance -= amt
        to.balance += amt
        print("Transfer done.")
        self.add_transaction("-", amt, f"Transferred to {to.name}")
        to.add_transaction("+", amt, f"Received from {self.name}")
        save_accounts()

    def deposit(self, amt):
        self.balance += amt
        print("Deposit done.")
        self.add_transaction("+", amt, "Deposited")
        save_accounts()

    def withdraw(self, amt):
        if amt > self.balance:
            raise RuntimeError("Amount greater than available balance.")
        self.balance -= amt
        print("Withdraw done.")
        self.add_transaction("-", amt, "Withdrawn")
        save_accounts()

    def show_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
        else:
            print("Last 10 Transactions:")
            for i, t in enumerate(reversed(self.transactions), 1):
                print(f"{i}. {t}")

    def request_card(self, all_accounts):
        if self.card_number:
            print("\n--- Your Card Information ---")
            print(f"Card Number: {self.card_number}")
            print(f"Expiry Date: {self.expiry}")
            print(f"CVV2: {self.cvv2}")
            print(f"PIN: {self.pin}")
            print("\nDo you want to update your card PIN or get a new card?")
            print("1. Update PIN")
            print("2. Get new card (replace old card)")
            print("3. Cancel")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.update_pin()
            elif choice == "2":
                self.issue_new_card(all_accounts)
            else:
                print("Canceled.")
            return

    # اگر کارت نداشت، کارت جدید صادر می‌کند
        self.issue_new_card(all_accounts)

        # اگر کارت نداشت، کارت جدید صادر می‌کند
        self.issue_new_card(all_accounts)

    def update_pin(self):
        print("\n--- Update Card PIN ---")
        while True:
            new_pin = input("Enter new PIN (4-6 digits): ").strip()
            if not new_pin.isdigit() or not (4 <= len(new_pin) <= 6):
                print("Invalid PIN format.")
            else:
                confirm_pin = input("Confirm new PIN: ").strip()
                if new_pin != confirm_pin:
                    print("PINs do not match.")
                else:
                    break
        self.pin = new_pin
        print("PIN updated successfully.")
        save_accounts()

    def issue_new_card(self, all_accounts):
        print("\n--- Issuing New Card ---")
        existing_cards = [acc.card_number for acc in all_accounts if acc.card_number]
        self.card_number = generate_random_card(existing_cards)
        self.cvv2 = generate_cvv2()
        self.expiry = generate_expiry_date()
        self.update_pin()
        print("\nNew card issued successfully!")
        print(f"Card Number: {self.card_number}")
        print(f"Expiry Date: {self.expiry}")
        print(f"CVV2: {self.cvv2}")
        save_accounts()





def generate_random_card(existing_cards):
    bin_code = "627412"  # کد ثابت بانک یا سیستم
    while True:
        random_part = ''.join(str(random.randint(0, 9)) for _ in range(10))
        card_number = bin_code + random_part
        if card_number not in existing_cards:
            return card_number

def generate_cvv2():
    return ''.join(str(random.randint(0, 9)) for _ in range(3))

def generate_expiry_date():
    today = datetime.today()
    future_date = today + timedelta(days=365*4)  # 4 سال آینده
    return future_date.strftime("%m/%y")



def save_accounts():
    with open(FILENAME, "w", encoding="utf-8") as f:
        for acc in accounts:
            f.write("---ACCOUNT START---\n")
            f.write(f"name: {acc.name}\n")
            f.write(f"id: {acc.id}\n")
            f.write(f"balance: {acc.balance}\n")
            f.write(f"card_number: {acc.card_number if acc.card_number else ''}\n")
            f.write(f"cvv2: {acc.cvv2 if acc.cvv2 else ''}\n")
            f.write(f"expiry: {acc.expiry if acc.expiry else ''}\n")
            f.write(f"pin: {acc.pin if acc.pin else ''}\n")
            f.write(f"username: {acc.username if acc.username else ''}\n")
            f.write(f"password: {acc.password if acc.password else ''}\n")
            f.write("transactions:\n")
            for t in acc.transactions:
                f.write(t + "\n")
            f.write("---ACCOUNT END---\n")


def load_accounts():
    if not os.path.exists(FILENAME):
        return []

    loaded_accounts = []
    with open(FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_acc = {}
    transactions = []
    inside_account = False

    for line in lines:
        line = line.strip()
        if line == "---ACCOUNT START---":
            inside_account = True
            current_acc = {}
            transactions = []
        elif line == "---ACCOUNT END---":
            inside_account = False
            acc = BankAccount(
                usnm=current_acc.get("name", ""),
                id=int(current_acc.get("id", 0)),
                bal=float(current_acc.get("balance", 0)),
                card_number=current_acc.get("card_number") if current_acc.get("card_number") else None,
                cvv2=current_acc.get("cvv2"),
                expiry=current_acc.get("expiry"),
                pin=current_acc.get("pin"),
                transactions=transactions,
                username=current_acc.get("username"),
                password=current_acc.get("password")
            )
            loaded_accounts.append(acc)
        elif inside_account:
            if line.startswith("name:"):
                current_acc["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("id:"):
                current_acc["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("balance:"):
                current_acc["balance"] = line.split(":", 1)[1].strip()
            elif line.startswith("card_number:"):
                current_acc["card_number"] = line.split(":", 1)[1].strip()
            elif line.startswith("cvv2:"):
                current_acc["cvv2"] = line.split(":", 1)[1].strip()
            elif line.startswith("expiry:"):
                current_acc["expiry"] = line.split(":", 1)[1].strip()
            elif line.startswith("pin:"):
                current_acc["pin"] = line.split(":", 1)[1].strip()
            elif line.startswith("username:"):
                current_acc["username"] = line.split(":", 1)[1].strip()
            elif line.startswith("password:"):
                current_acc["password"] = line.split(":", 1)[1].strip()
            elif line == "transactions:":
                transactions = []
            else:
                if line:
                    transactions.append(line)

    return loaded_accounts

def login():
    print("\n--- Login ---")
    username_try = input("Username: ").strip()
    password_try = input("Password: ").strip()

    acc = next((a for a in accounts if a.username == username_try and a.password == password_try), None)
    if acc:
        print(f"Login successful. Welcome, {acc.name}!")
        return acc
    else:
        print("Wrong username or password.")
        return None


def create_account():
    print("\n--- Create New Account ---")
    name = input("Enter your name: ")

    try:
        user_id = int(input("Choose an ID: "))
    except ValueError:
        print("Invalid ID.")
        return None

    if any(acc.id == user_id for acc in accounts):
        print("ID already taken.")
        return None

    while True:
        username = input("Choose a username: ").strip()
        if any(acc.username == username for acc in accounts):
            print("Username already taken, try another.")
        else:
            break

    while True:
        password = input("Choose a password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        if password != confirm_password:
            print("Passwords do not match, try again.")
        elif len(password) < 4:
            print("Password too short, min 4 characters.")
        else:
            break

    try:
        initial_balance = float(input("Enter initial deposit: "))
    except ValueError:
        print("Invalid amount.")
        return None

    new_acc = BankAccount(name, user_id, initial_balance, username=username, password=password)
    accounts.append(new_acc)
    save_accounts()
    print(f"Account created successfully for {name}!")
    return new_acc


def menu(account):
    while True:
        print("\n--- Main Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Last 10 Transactions")
        print("6. Request or Manage Card")
        print("7. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print(f"Your balance: ${account.balance}")
            if account.card_number:
                print(f"Your card: {account.card_number}")
                print(f"Expiry: {account.expiry}")
                print(f"CVV2: {account.cvv2}")
        elif choice == "2":
            try:
                amt = float(input("Enter amount to deposit: "))
                account.deposit(amt)
            except ValueError:
                print("Invalid amount.")
        elif choice == "3":
            try:
                amt = float(input("Enter amount to withdraw: "))
                account.withdraw(amt)
            except ValueError:
                print("Invalid amount.")
            except RuntimeError as e:
                print(e)
        elif choice == "4":
            recipient_card = input("Enter recipient's card number: ").strip()
            recipient = next((acc for acc in accounts if acc.card_number == recipient_card), None)
            if recipient:
                try:
                    amt = float(input("Enter amount to transfer: "))
                    account.transfer(recipient, amt)
                except ValueError:
                    print("Invalid amount.")
                except RuntimeError as e:
                    print(e)
            else:
                print("Recipient with this card number not found.")
        elif choice == "5":
            account.show_transactions()
        elif choice == "6":
            account.request_card(accounts)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


# ---------- Main Program ----------
accounts = load_accounts()

if not accounts:
    accounts = [
        BankAccount("John", 1, 500),
        BankAccount("Ali", 2, 500),
        BankAccount("Javid", 3, 500)
    ]
    save_accounts()

while True:
    print("\n====== Welcome to the Bank System ======")
    print("1. Login")
    print("2. Create New Account")
    print("3. Exit")

    option = input("Choose an option: ")

    if option == "1":
        user = login()
        if user:
            menu(user)
    elif option == "2":
        user = create_account()
        if user:
            menu(user)
    elif option == "3":
        print("Goodbye.")
        break
    else:
        print("Invalid choice.")
