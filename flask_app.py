
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect, session, escape, request, g
from User import *

import json
import os
import time
import locale


app = Flask(__name__)
app.secret_key = os.urandom(24)

def convert_money(money):
        locale.setlocale( locale.LC_ALL, '' )
        return locale.currency(money)


###############
#session stuff#
###############


@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if g.user != None:
        g.user = None

    if request.method == 'POST':

        db = Database_Mediator()
        username = request.form['username']
        password = request.form['password']

        if db.is_user(username, password):

            user_id = db.get_user_id(username, password)
            session['user_id'] = user_id

            return redirect(url_for('main_menu'))
        else:
            error = "Invalid username/password"

    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    if g.user != None:
        session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template("about_page.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    username = None
    password = None

    if request.method == 'POST':
        db = Database_Mediator()
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']

        if db.is_username(username):
            error = "Username already taken"
            return render_template("register.html", error=error)
        else:
            db.create_user(fname, lname, username, password)
            return redirect(url_for('login'))

    return render_template("register.html", error=error)


@app.route('/main_menu')
def main_menu():
    if g.user is None:
        return redirect(url_for('main'))

    user = User()
    user.init(g.user)

    if user.accounts == []:
        return redirect(url_for('create_account'))

    credit = 0.00
    for account in user.accounts:
        credit += account.credit

    debit = 0.00
    for account in user.accounts:
        debit += account.debit

    net = credit + debit
    credit = convert_money(credit)
    debit = convert_money(debit)
    net = convert_money(net)

    user.push()
    return render_template("main_menu.html", credit=credit, debit=debit, net=net, fname=user.fname, Account_data = user.accounts)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if g.user is None:
        return redirect(url_for('main'))

    user = User()
    user.init(g.user)

    if request.method == 'POST':
        user_id = user.user_id
        account_type = int(request.form['type'])
        balance = float(request.form['balance'])
        tag = str(request.form['tag'])

        user.create_account(user_id, account_type, balance, tag)
        user.push()
        return redirect(url_for('account_menu', account_num = 0))

    return render_template("create_account.html")

@app.route('/account_menu/<account_num>', methods=['GET', 'POST'])
def account_menu(account_num):
    account_num = int(account_num)
    if g.user is None:
        return redirect(url_for('main'))

    user = User()
    user.init(g.user)
    if user.accounts == []:
        return redirect(url_for('create_account'))

    if request.method == 'POST':
        user_id = user.user_id
        account = int(request.form['account'])
        trans_type = int(request.form['type'])
        amount = float(request.form['amount'])
        date = int(time.strftime("%Y%m%d%H%M%S"))
        datetime = time.strftime("%m/%d/%Y, %H:%M:%S")

        user.create_transaction(user_id, account, trans_type, amount,
                                date, datetime)
        user.push()
        return redirect(url_for('account_menu', account_num = account_num))


    user.push()
    account_data = None
    if account_num == 0:
        account_data = user.accounts
    else:
        for account in user.accounts:
            if account.account == account_num:
                account_data = account
                break

    return render_template("account_menu.html", Account_data=account_data, Account_num = account_num)

@app.route('/delete_account/<account_num>', methods=['Get', 'POST'])
def delete_account(account_num):
    db = Database_Mediator()
    db.delete_account(int(account_num))
    return redirect(url_for('account_menu', account_num = 0))

@app.route('/income_menu', methods=['GET', 'POST'])
def income_menu():
    if g.user is None:
        return redirect(url_for('main'))

    user = User()
    user.init(g.user)
    if user.accounts == []:
        return redirect(url_for('create_account'))


    if request.method == 'POST':
        user_id = user.user_id
        account = int(request.form['account'])
        amount = float(request.form['amount'])
        date = int(time.strftime("%Y%m%d%H%M%S"))
        datetime = time.strftime("%m/%d/%Y, %H:%M:%S")

        user.create_transaction(user_id, account, 1, amount,
                                date, datetime)

    user.push()
    return render_template("income_menu.html", Account_data=user.accounts)


@app.route('/expense_menu', methods=['GET', 'POST'])
def expense_menu():
    if g.user is None:
        return redirect(url_for('main'))

    user = User()
    user.init(g.user)
    if user.accounts == []:
        return redirect(url_for('create_account'))

    if request.method == 'POST':
        user_id = user.user_id
        account = int(request.form['account'])
        amount = float(request.form['amount'])
        date = int(time.strftime("%Y%m%d%H%M%S"))
        datetime = time.strftime("%m/%d/%Y, %H:%M:%S")

        user.create_transaction(user_id, account, 0, amount,
                                date, datetime)
        user.push()


    user.push()
    return render_template("expense_menu.html", Account_data=user.accounts)



@app.route('/delete_trans/<trans_amount>/<trans_date>', methods=['Get', 'POST'])
def remove_trans(trans_amount, trans_date):
    db = Database_Mediator()
    db.delete_transaction(float(trans_amount), int(trans_date))
    return redirect(url_for('income_menu'))

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = session['user_id']


if __name__ == '__main__':
    app.run(debug = True)