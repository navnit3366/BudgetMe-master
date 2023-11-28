from decimal import *
from exception import *
from Database_Mediator import *

import locale

class Account:
    def __init__(self, user_id, account, account_type, balance, tag):
        self.db = Database_Mediator()
        self.exception = TypeException()

        self.user_id = user_id
        self.account = account
        self.account_type = account_type

        self.trans_credits = []
        self.trans_debits = []
        self.trans_total = []

        self.credit = 0.00
        self.debit = 0.00
        self.balance = balance

        self.credit_str = self.convert_money(self.credit)
        self.debit_str = self.convert_money(self.debit)
        self.balance_str = self.convert_money(self.balance)
        self.tag = tag

    def convert_money(self, money):
        locale.setlocale( locale.LC_ALL, '' )
        return locale.currency(money)

    def pull_transaction_data(self):
        transacitons = self.db.get_transaction_data(self.account)
        amount = 0.00
        credit = 0.00
        debit = 0.00


        for trans in transacitons:
            self.exception.int_type_exception(trans['type'])
            self.exception.float_type_exception(float(trans['amount']))

            new_trans = Transaction(trans['user_id'], trans['account'],
                                    trans['type'], float(trans['amount']),
                                    trans['date'], trans['datetime'])
            print("inside pull_trans_data: ", trans['type'], new_trans.trans_type)

            if new_trans.trans_type is 0:
                self.trans_total.append(new_trans)
                self.trans_debits.append(new_trans)
                amount -= new_trans.amount
                debit -= new_trans.amount

            if new_trans.trans_type is 1:
                self.trans_total.append(new_trans)
                self.trans_credits.append(new_trans)
                amount += new_trans.amount
                credit += new_trans.amount

        self.credit = credit
        self.debit = debit
        self.balance = amount
        self.balance_str = self.convert_money(self.balance)

    def push_transaction_data(self):
        self.db.delete_transactions(self.account)
        for trans in self.trans_total:
            self.db.set_transaction_data(trans.user_id, trans.account,
            trans.trans_type, float(trans.amount), trans.date, trans.datetime)

    def create_transaction(self, user_id, account, trans_type, amount, date, datetime):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account)
        self.exception.int_type_exception(trans_type)
        self.exception.float_type_exception(amount)
        self.exception.int_type_exception(date)
        self.exception.str_type_exception(datetime)

        new_trans = Transaction(user_id, account, trans_type, amount, date, datetime)
        self.db.set_transaction_data(user_id, account, trans_type, amount, date, datetime)
        amount = 0.00
        credit = 0.00
        debit = 0.00

        if new_trans.trans_type is 0:
            self.trans_total.append(new_trans)
            self.trans_debits.append(new_trans)
            amount -= float(amount)
            debit -= float(amount)

        if new_trans.trans_type is 1:
            self.trans_total.append(new_trans)
            self.trans_credits.append(new_trans)
            amount += float(amount)
            credit += float(amount)

        self.credit += credit
        self.debit += debit
        self.balance += amount
        self.balance_str = self.convert_money(self.balance)


class Transaction:
    def __init__(self, user_id, account, trans_type, amount, date, datetime):
        self.user_id = user_id
        self.account = account
        self.trans_type = trans_type
        self.amount = amount
        self.date = date
        self.datetime = datetime
