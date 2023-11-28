import locale

class Goal:
    def __init__(self, user_id, account, account_type, goal_amount, saved_amount,
                 tag, deadline):
        self.user_id = user_id
        self.account = account
        self.account_type = account_type
        self.tag = tag
        self.deadline = deadline

        self.goal_amount = goal_amount
        self.saved_amount = saved_amount

        self.goal_amount_str = self.convert_money(self.goal_amount)
        self.saved_amount_str = self.convert_money(self.saved_amount)


    def convert_money(self, money):
        locale.setlocale( locale.LC_ALL, '' )
        return locale.currency(money)
