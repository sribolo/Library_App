class BorrowedItems:
    def __init__(self, borrower_account_number, item_borrowed, date_borrowed):
        self.borrower_account_number = borrower_account_number
        self.item_borrowed = item_borrowed
        self.date_borrowed = date_borrowed
        self.return_date = None

    def return_item(self, return_date):
        self.return_date = return_date

    def __str__(self):
        return f"BorrowedItem: {self.item_borrowed.title} by Account: {self.borrower_account_number} on {self.date_borrowed} (Returned: {self.return_date})"
