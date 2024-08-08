from password_function import hash_password, verify_password
from BorrowerList import BorrowerList

class Administrator:
    def __init__(self, username, password, first_name, last_name, library_tree, borrower_list):
        self.username = username
        self.password = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.library_tree = library_tree
        self.borrower_list = borrower_list

    def check_password(self, password):
        return verify_password(self.password, password)

    def search_items(self, attribute, value):
        if attribute == "year_published":
            return self.library_tree.search_by_year_published(value)
        elif attribute == "title":
            return self.library_tree.search_by_title(value)
        elif attribute == "category":
            return self.library_tree.search_by_category(value)
        elif attribute == "language":
            return self.library_tree.search_by_language(value)
        elif attribute == "authors":
            return self.library_tree.search_by_author(value)
    def display_item_details(self, item):
        authors = ', '.join(item.authors) if isinstance(item.authors, list) else item.authors
        return f"Title: {item.title}, Authors: {authors}, Year: {item.year_published}"

    def add_item(self, item):
        self.library_tree.insert(item)

    def remove_item(self, title):
        self.library_tree.remove(title.lower())

    def locate_borrowers_with_unpaid_fines(self):
        return self.borrower_list.find_borrowers_with_unpaid_fines()

    def list_borrowed_items(self, account_number):
        borrower = self.borrower_list.find_borrower_by_account_number(account_number)
        return borrower.borrowed_items if borrower else []
