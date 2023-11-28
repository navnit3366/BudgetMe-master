from decimal import *
from exception import *
from Database_Mediator import *
from Account import *
from Goal import *

import locale

class User:
    def __init__(self,user_id = 0,fname='fname',lname='lname',username='username',password='password'):
        self.user_id  = user_id
        self.fname    = fname
        self.lname    = lname
        self.username = username
        self.password = password

        self.accounts = []
        self.num_of_accounts = 0

        self.goals = []
        self.num_of_goals = 0

        self.db = Database_Mediator()
        self.exception = TypeException()

    def init(self, user_id):
        self.user_id  = user_id
        self.fname = self.db.get_user_data(user_id)['fname']
        self.lname = self.db.get_user_data(user_id)['lname']
        self.username = self.db.get_user_data(user_id)['username']
        self.password = self.db.get_user_data(user_id)['password']

        self.exception.int_type_exception(user_id)
        self.exception.str_type_exception(self.fname)
        self.exception.str_type_exception(self.lname)
        self.exception.str_type_exception(self.username)
        self.exception.str_type_exception(self.password)

        self.pull_accounts()
        self.pull_goals()

    def push(self):
        self.push_accounts()
        self.push_goals()

    def create_user(self, fname, lname, username, password):
        self.exception.str_type_exception(fname)
        self.exception.str_type_exception(lname)
        self.exception.str_type_exception(username)
        self.exception.str_type_exception(password)
        return self.db.create_user(fname, lname, username, password)

    def delete_user(self):
        self.db.delete_user(self.user_id)

    def pull_accounts(self):
        exception = DBException()

        exception.invalid_user(self.user_id)
        accounts = self.db.get_account_data(self.user_id)

        for account in accounts:
            new_account = Account(account['user_id'], account['account'],
                                  account['type'], account['balance'],
                                  account['tag'])
            new_account.pull_transaction_data()
            self.accounts.append(new_account)
            self.num_of_accounts += 1

    def push_accounts(self):
        exception = DBException()
        exception.invalid_user(self.user_id)

        for account in self.accounts:
            account.push_transaction_data()
            self.db.set_account_data(account.user_id, account.account,
                                     account.account_type, account.balance,
                                     account.tag)

    def create_account(self, user_id, account_type, balance, tag):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(balance)
        self.exception.str_type_exception(tag)

        self.push_accounts()
        self.db.create_account(user_id, account_type, balance, tag)
        self.pull_accounts()

    def delete_account(self, account):
        self.exception.int_type_exception(account)

        self.push_accounts()
        self.db.delete_account(account)

    def create_transaction(self, user_id, account, trans_type, amount, date, datetime):
        for Account in self.accounts:
            if Account.account == account:
                Account.create_transaction(user_id, account, trans_type,
                                           amount, date, datetime)
                self.push_accounts()
                return

    def pull_goals(self):
        exception = DBException()

        goals = self.db.get_goals_data(self.user_id)

        for goal in goals:
            new_goal = Goal(goal['user_id'], goal['account'], goal['type'],
                            goal['goal_amount'], goal['saved_amount'],
                            goal['tag'], goal['deadline'])

            self.goals.append(new_goal)
            self.num_of_goals += 1

    def push_goals(self):
        for goal in self.goals:
            self.db.set_goal_data(goal.user_id, goal.account, goal.account_type,
                                  goal.goal_amount, goal.saved_amount,
                                  goal.tag, goal.deadline)

    def create_goal(self, user_id, account_type, goal_amount, tag, deadline):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(goal_amount)
        self.exception.str_type_exception(tag)

        self.push_goals()
        self.db.create_goal(user_id, account_type, goal_amount, tag, deadline)
        self.pull_goals()

    def delete_goal(self, account):
        self.push_goals()
        self.db.delete_goal(account)
