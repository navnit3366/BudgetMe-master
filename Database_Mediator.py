from exception import *

import MySQLdb
import time

class DBException:
    def invalid_user(self, x):
        assert(x is not 0), "Invalid User_id, recieved {}".format(x)

    def invalid_account(self, x):
        assert(x is not 0), "Invalid account, recieved {}".format(x)

class Database_Mediator:
    def __init__(self):
        self.exception = TypeException()
        self.dbexception = DBException()

    def dosql(self, sql):
        self.exception.str_type_exception(sql)

             #connects to Users Database
        db = MySQLdb.connect(
            host='mefisher2.mysql.pythonanywhere-services.com',
            user='mefisher2',
            passwd='cc1851cc',
            db='mefisher2$Transactions')

        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)

        ret = cursor.fetchall()
        cursor.close()

        db.commit()
        db.close()

        return ret

    ############################################################################
    ## User Database Methods
    ############################################################################
    def is_user(self, username, password): #returns a bool
        username = username.lower()
        sql = "select * from Users where username = '%s' and password = '%s'" % (username, password)

        try:
            ret = self.dosql(sql)
        except:
            return False

        return (ret != ())

    def is_username(self, username):
        self.exception.str_type_exception(username)
        username = username.lower()
        sql = "select * from Users where username = '%s'" % (username)

        try:
            ret = self.dosql(sql)
        except:
            return False

        return (ret != ())

    def is_user_id(self, user_id):
        self.excepton.int_type_exception(user_id)
        sql = "select * from Users where user_id = '%s'" % (user_id)

        try:
            ret = self.dosql(sql)
        except:
            return False

        return (ret != ())

    def get_user_id(self, username, password):
        self.exception.str_type_exception(username)
        self.exception.str_type_exception(password)

        sql = "select user_id from Users where username = '%s' and password ='%s'" % (username, password)
        ret = self.dosql(sql)
        ret = ret[0]['user_id']
        return ret

    def get_user_data(self, user_id):
        self.exception.int_type_exception(user_id)
        self.dbexception.invalid_user(user_id)

        sql = "select * from Users where user_id = '%s'" % (user_id)
        return self.dosql(sql)[0]

    def create_user(self, fname, lname, username, password):
        self.exception.str_type_exception(fname)
        self.exception.str_type_exception(lname)
        self.exception.str_type_exception(username)
        self.exception.str_type_exception(password)

        sql = """
                insert Users (fname, lname, username, password)
                values ('%s', '%s', '%s', '%s')
              """ % (fname, lname, username.lower(), password)
        self.dosql(sql)
        return self.get_user_id(username, password)

    def delete_user(self, user_id):
        self.exception.int_type_exception(user_id)

        sql = "delete from Goals where user_id = '%s'" % user_id
        self.dosql(sql)
        sql = "delete from Transaction where user_id = '%s'" % user_id
        self.dosql(sql)
        sql = "delete from Account where user_id = '%s'" % user_id
        self.dosql(sql)
        sql = "delete from Users where user_id = '%s'" % user_id
        self.dosql(sql)

    ############################################################################
    ## Account Database Methods
    ############################################################################

    def get_account_data(self, user_id):
        self.exception.int_type_exception(user_id)
        self.dbexception.invalid_user(user_id)

        sql = "select * from Account where user_id = '%s'" % (user_id)
        return self.dosql(sql)

    def set_account_data(self, user_id, account, account_type, balance, tag):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(balance)
        self.exception.str_type_exception(tag)

        sql = """ update Account set user_id = '%s', type = '%s',
                  balance = '%s', tag = '%s' where account = '%s'
              """ % (user_id, account_type, balance, tag, account)
        self.dosql(sql)

    def create_account(self, user_id, account_type, balance, tag):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(balance)
        self.exception.str_type_exception(tag)

        sql = "insert Account (user_id, type, balance, tag) values ('%s','%s','%s','%s')" % (user_id, account_type, balance, tag)
        self.dosql(sql)
        sql = "select account from Account where user_id = '%s' and type = '%s' and tag = '%s'" % (user_id, account_type, tag)
        account_num = self.dosql(sql)[0]['account']
        date = int(time.strftime("%Y%m%d%H%M%S"))
        datetime = time.strftime("%m/%d/%Y, %H:%M:%S")
        self.set_transaction_data(user_id, account_num, account_type, balance,
                                  date, datetime)

    def delete_account(self, account):
        self.exception.int_type_exception(account)
        self.dbexception.invalid_account(account)

        self.delete_transactions(account)
        sql = "delete from Account where account = '%s'" % account
        self.dosql(sql)

    ############################################################################
    ## Goals Database Methods
    ############################################################################

    def get_goals_data(self, user_id):
        self.exception.int_type_exception(user_id)

        sql = "select * from Goals where user_id = '%s'" % (user_id)
        return self.dosql(sql)

    def set_goals_data(self, user_id, account, account_type, goal_amount,
                       saved_amount, tag, deadline):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(goal_amount)
        self.exception.float_type_exception(saved_amount)
        self.exception.str_type_exception(tag)
        self.exception.int_type_exception(deadline)

        sql = """ update Goals set user_id = '%s', type = '%s',
                  goal_amount = '%s', saved_amount = '%s', tag = '%s',
                  deadline = '%s' where account = '%s'
              """ % (user_id, account_type, goal_amount, saved_amount,
                     tag, deadline, account)
        self.dosql(sql)

    def create_goal(self, user_id, account_type, goal_amount, tag, deadline):
        self.excepiton.int_type_exception(user_id)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(goal_amount)
        self.exception.str_type_exception(tag)
        self.exception.int_type_exception(deadline)

        sql = """
                insert Goals (user_id, type, goal_amount, tag, deadline)
                values ('%s', '%s', '%s', '%s', '%s')
              """ % (user_id, account_type, goal_amount, tag, deadline)
        self.dosql(sql)

    def delete_goal(self, account):
        self.exception.int_type_exception(account)

        sql = "delete from Goals where account = '%s'" % account
        self.dosql(sql)

    ############################################################################
    ## Transaction Database Methods
    ############################################################################

    def get_transaction_data(self, account):
        self.exception.int_type_exception(account)
        self.dbexception.invalid_account(account)

        sql = "select * from Transaction where account = '%s'" % (account)
        return self.dosql(sql)

    def set_transaction_data(self, user_id, account, account_type, amount, date, datetime):
        self.exception.int_type_exception(user_id)
        self.exception.int_type_exception(account)
        self.exception.int_type_exception(account_type)
        self.exception.float_type_exception(amount)
        self.exception.int_type_exception(date)
        self.exception.str_type_exception(datetime)

        sql = """
                insert Transaction (user_id, account, type, amount, date, datetime)
                values ('%s', '%s', '%s', '%s', '%s', '%s')
              """ % (user_id, account, account_type, amount, date, datetime)
        self.dosql(sql)

    def delete_transactions(self, account):
        self.exception.int_type_exception(account)
        self.dbexception.invalid_account(account)

        sql = "delete from Transaction where account = '%s'" % account
        self.dosql(sql)

    def delete_transaction(self, amount, date):
        self.exception.float_type_exception(amount)
        self.exception.int_type_exception(date)

        sql = "delete from Transaction where amount = '%s' and date = '%s'" % (amount, date)
        self.dosql(sql)

