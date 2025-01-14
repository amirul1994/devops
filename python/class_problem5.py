#  Write a Python class BankAccount with attributes like account_number,
#  balance, date_of_opening and customer_name,
#  and methods like deposit, withdraw, and check_balance.

class BankAccount():
    def __init__(self,account_number, balance,
                 date_of_opening, customer_name ):
        self.account_number = account_number
        self.balance = balance
        self.date_of_opening = date_of_opening
        self.customer_name = customer_name

    def deposit(self):
        depo = 15000
        return depo


    def withdraw(self):
        wd = 5000
        return wd

    def check_balance(self):
        return self.balance + self.deposit() - self.withdraw()


    def acc_dtls(self):
        print('account number is:', self.account_number)
        print('balance is:', self.check_balance())
        print('date of opening:', self.date_of_opening)
        print('customer name:', self.customer_name)



BA = BankAccount(220, 30000,
                 '26/08/2022', 'amirul')

BA.acc_dtls()