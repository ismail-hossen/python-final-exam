from abc import ABC, abstractmethod
from datetime import datetime


class Bank(ABC):
    __accounts = []
    __totalBalance = 0
    __totalLoan = 0
    isBankrupt = False

    def __init__(self, name, email, address, accountNumber, password, type, userType):
        self.name = name
        self.email = email
        self.address = address
        self.__accountNo = accountNumber
        self.__passW = password
        self.__balance = 0
        self.type = type
        self.transactions = []
        self.__takeLoan = 0
        self.__loanAmount = 0
        self.userType = userType
        Bank.__accounts.append(self)
        Bank.__totalBalance += self.__balance

    def deposit(self, amount):
        if amount >= 0:
            self.__balance += amount
            Bank.__totalBalance += amount
            transaction = f"Deposit amount {amount}, Time: {datetime.now()}, Account no {self.__accountNo}"
            self.transactions.append(transaction)
            print(f"\nDeposited {amount}. New balance is: ${self.__balance}")
        else:
            print("\nInvalid deposit amount")

    def withdraw(self, amount):
        if not Bank.isBankrupt and amount >= 0 and amount <= self.__balance:
            self.__balance -= amount
            Bank.__totalBalance -= amount
            transaction = f"Withdrawal amount {amount}, Time: {datetime.now()}, Account no {self.__accountNo}"
            self.transactions.append(transaction)
            print(f"\nWithdraw ${amount}. New balance is: ${self.__balance}")
        else:
            print("\nWithdrawal amount exceeded or Bankrupt!")

    def checkBalance(self):
        print(f"Your current Balance is: {self.__balance}")

    def transferMoney(self, amount, accNo):
        if not self.isBankrupt and amount >= 0 and amount <= self.balance:
            flag = False
            for i in range(len(Bank.__accounts)):
                if Bank.__accounts[i].__accountNo == accNo:
                    Bank.__accounts[i].__balance += amount
                    self.__balance -= amount
                    flag = True
                    transaction = f"Transfer amount {amount}, Time: {datetime.now()}, From account no {accNo}, To {self.__accountNo}, Balance {self.__balance}"
                    self.transactions.append(transaction)
                    print(
                        f"\nYour transfer amount: {amount} from {self.name} to {Bank.accounts[i].name} is success.\n")
                    break
            if flag == False:
                print("Account does not exist")
        else:
            print("\nThe bank is bankrupt or your amount is invalid!")

    def getLoan(self, amount):
        if Bank.isBankrupt == False and Bank.__totalBalance != 0:
            if self.__takeLoan <= 2 and amount <= Bank.__totalBalance:
                self.__takeLoan += 1
                self.__loanAmount += amount
                Bank.__totalLoan += amount
                self.__balance += amount
                print(f"\nYou got {amount} amount of Loan")
            else:
                print("You exceeded loan take limits.")
        else:
            print("The Bank is bankrupt for now!")

    def getTrnHistory(self):
        if len(self.transactions) == 0:
            print("\nDon't have any transactions\n")
            return
        for trn in self.transactions:
            print(trn)

    def deleteAccount(self, accNo):
        if self.userType == "Admin":
            flag = False
            for i in range(len(Bank.__accounts)):
                if Bank.__accounts[i].__accountNo == accNo:
                    Bank.__totalBalance -= Bank.__accounts[i].__balance
                    flag = True
                    Bank.__accounts.pop(i)
                    print(
                        f"Account {accNo} is deleted successfully.\n")
                    break
            if not flag:
                print("Account does not exist")
        else:
            print("You are unable to delete any account.")

    def seeAllAccOfTheBank(self):
        for acc in Bank.__accounts:
            print(acc.name, acc.__accountNo)

    def login(accNo, password):
        flag = False
        for acc in Bank.__accounts:
            if acc.__accountNo == accNo and acc.__passW == password:
                flag = True
                return acc
        if flag == False:
            print("Account does not exit")

    def showTotalBankBalance(self):
        if self.userType == "Admin":
            print(f"\nTotal balance in the bank is {Bank.__totalBalance}\n")
        else:
            print("You are unable to see of the bank balance")

    def showTotalLoanOfTheBank(self):
        if self.userType == "Admin":
            print(f"\nTotal Loan in the bank is {Bank.__totalLoan}\n")
        else:
            print("You are unable to see of the bank loan")

    def onOrOff(self, status):
        if status == "ON":
            Bank.isBankrupt = True
        else:
            Bank.isBankrupt = False

    @abstractmethod
    def showInfo(self):
        pass


class SavingsAccount(Bank):
    def __init__(self, name, email, address, accountNumber, password, userType):
        super().__init__(name, email, address, accountNumber, password, "savings", userType)
        self.accNo = accountNumber

    def showInfo(self):
        print(f"Infos of {self.type} account of {self.name}:\n")
        print(f"User Type: {self.userType}")
        print(f"Name: {self.name}")
        print(f"Account No: {self.accNo}\n")


class CurrentAccount(Bank):
    def __init__(self, name, email, address, accountNumber, password, userType):
        super().__init__(name, email, address, accountNumber, password, "current", userType)
        self.accNo = accountNumber

    def showInfo(self):
        print(f"Infos of {self.type} account of {self.name}:\n")
        print(f"User Type: {self.userType}")
        print(f"Name: {self.name}")
        print(f"Account No: {self.accNo}\n")


currentUser = None
while True:
    if currentUser == None:
        print("No user logged in!")
        op = input("Register as User/Admin? ( ur / ar ) or Login( l )?: ")
        if op == "ur":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            pa = input("Password: ")
            accType = input("Savings Account or Current Account (sv/cu): ")
            accNo = f"{email[:3]+name[:3]}"
            if accType == "sv":
                currentUser = SavingsAccount(
                    name, email, address, accNo, pa, "User")
            elif accType == "cu":
                currentUser = CurrentAccount(
                    name, email, address, accNo, pa, "User")

        elif op == "ar":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            pa = input("Password: ")
            accType = input("Savings Account or Current Account (sv/cu):")
            accNo = f"{email[:3]+name[:3]}"
            if accType == "sv":
                currentUser = SavingsAccount(
                    name, email, address, accNo, pa, "Admin")
            elif accType == "cu":
                currentUser = CurrentAccount(
                    name, email, address, accNo, pa, "Admin")
        else:
            accNo = input("Account Number: ")
            password = input("Enter Password: ")
            acc = Bank.login(accNo=accNo, password=password)
            if acc:
                currentUser = acc

    else:
        print(f"\nWelcome {currentUser.name}!\n")

        if currentUser.userType == "User":
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Show Info")
            print("4. Check Balance")
            print("5. Transfer Money")
            print("6. Take Loan")
            print("7. Transaction History")
            print("8. Logout\n")

            op = int(input("Choose Option: "))

            if op == 1:
                amount = int(input("Enter withdraw amount: "))
                currentUser.withdraw(amount)

            elif op == 2:
                amount = int(input("Enter deposit amount: "))
                currentUser.deposit(amount)

            elif op == 3:
                currentUser.showInfo()

            elif op == 4:
                currentUser.checkBalance()

            elif op == 5:
                amount = int(input("Enter transfer amount: "))
                accNo = input("Enter the ac no to transfer money: ")
                currentUser.transferMoney(amount, accNo)

            elif op == 6:
                amount = int(input("Enter loan amount: "))
                currentUser.getLoan(amount)

            elif op == 7:
                currentUser.getTrnHistory()

            elif op == 8:
                currentUser = None

            else:
                print("Invalid Option")

        elif currentUser.userType == "Admin":
            print("1. Delete an user account")
            print("2. See all user accounts")
            print("3. Show total balance of the bank")
            print("4. Show total loan amount of the bank")
            print("5. On or Off the bank")
            print("6. Logout\n")

            op = int(input("Choose Option: "))

            if op == 1:
                accNo = input("Enter acc no to delete: ")
                currentUser.deleteAccount(accNo)

            elif op == 2:
                print("All accounts of the bank.\n")
                currentUser.seeAllAccOfTheBank()

            elif op == 3:
                currentUser.showTotalBankBalance()

            elif op == 4:
                currentUser.showTotalLoanOfTheBank()

            elif op == 5:
                onOrOff = input("Need to Bank On or Off Type( on / Off )?: ")
                if onOrOff == "on":
                    currentUser.onOrOff("ON")
                else:
                    currentUser.onOrOff("OFF")

            elif op == 6:
                currentUser = None

            else:
                print("Invalid Option")
