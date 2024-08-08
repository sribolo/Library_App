from password_function import hash_password, verify_password
from datetime import datetime, timedelta

class Borrower:
    def __init__(self, username, password, first_name, last_name, account_number):
        self.username = username
        self.password = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.account_number = account_number
        self.borrowed_items = []
        self.fine_amount = 0

    def check_password(self, password):
        return verify_password(self.password, password)

    def has_fine(self):
        return self.fine_amount > 0

    def get_fine_amount(self):
        return self.fine_amount

    def pay_fine(self, amount):
        if amount >= self.fine_amount:
            self.fine_amount = 0
        else:
            self.fine_amount -= amount

    def borrow_item(self, item):
        if len(self.borrowed_items) >= 8:
            print("You cannot borrow more than 8 items.")
            return
        if item in self.borrowed_items:
            print("You have already borrowed this item.")
            return
        due_date = self.calculate_due_date()
        self.borrowed_items.append(item)
        item.due_date = due_date

    def return_item(self, item):
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)
        else:
            print("You have not borrowed this item.")

    def calculate_due_date(self):
        from datetime import datetime, timedelta
        return datetime.now() + timedelta(days=14)

    def get_due_dates(self):
        return {item.title: item.due_date for item in self.borrowed_items}
