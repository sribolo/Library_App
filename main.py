from password_function import hash_password, verify_password
from Book_class import Book
from Periodical_class import Periodical
from AudioBook_class import Audiobook
from Borrower_class import Borrower
from Administrator_class import Administrator
from librarytree import LibraryTree
from BorrowerList import BorrowerList
import csv

def load_borrowers_from_file(borrowers):
    borrower_list = BorrowerList()
    with open(borrowers, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            username, password, first_name, last_name, account_number, fine_amount = row
            borrower = Borrower(username, password, first_name, last_name, account_number)
            borrower.fine_amount = float(fine_amount)
            borrower_list.add_borrower(borrower)
    return borrower_list

def load_library_items_from_file(library_items):
    library_tree = LibraryTree()
    with open(library_items, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            item_type, title, category, language, authors, isbn_or_format, year_published = row
            try:
                authors_list = [author.strip() for author in authors.split(',')] if authors else []
                year_published = int(year_published)
                if item_type == "Book":
                    item = Book(title, category, language, authors_list, isbn_or_format, year_published)
                elif item_type == "AudioBook":
                    item = Audiobook(title, category, language, authors_list, isbn_or_format, year_published)
                elif item_type == "Periodical":
                    item = Periodical(title, category, language, authors_list, year_published)
                library_tree.insert(item)
            except ValueError as e:
                print(f"Error processing row: {row}. Error: {e}")
    return library_tree

def main():
    # Load the library tree and borrower list from files
    library_tree = load_library_items_from_file('library_items.csv')
    borrower_list = load_borrowers_from_file('borrowers.csv')

    # Create an administrator
    admin = Administrator("admin", "adminpass", "Admin", "User", library_tree, borrower_list)

    # User authentication
    while True:
        print("\nWelcome to SG Online Library App (SOLA)")
        user_type = input("Are you a (1) Borrower or (2) Administrator? (Enter 1 or 2): ")

        if user_type == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            borrower = borrower_list.find_borrower_by_username(username)

            if borrower and borrower.check_password(password):
                print(f"Welcome {borrower.first_name} {borrower.last_name}!")
                borrower_menu(borrower, library_tree, admin)
            else:
                print("Invalid username or password. Please try again.")

        elif user_type == '2':
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")

            if admin.username == username and admin.check_password(password):
                print(f"Welcome {admin.first_name} {admin.last_name}!")
                admin_menu(admin)
            else:
                print("Invalid username or password. Please try again.")

        else:
            print("Invalid selection. Please enter 1 or 2.")

def borrower_menu(borrower, library_tree, admin):
    while True:
        print("\nBorrower Menu")
        print("1. Borrow Item")
        print("2. Return Item")
        print("3. Search Item by Title")
        print("4. Search Item by Category")
        print("5. Search Item by Language")
        print("6. Search Item by Year Published")
        print("7. Search Item by Author")
        print("8. Check Due Date of Borrowed Items")
        print("9. Pay Fine")
        print("10. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            if len(borrower.borrowed_items) >= 8:
                print("You cannot borrow more than 8 items.")
            else:
                title = input("Enter title of the item to borrow: ")
                items = admin.search_items("title", title)
                if items:
                    item = items[0]
                    if borrower.has_fine():
                        print("You have an unpaid fine. Please pay it before borrowing new items.")
                    else:
                        borrower.borrow_item(item)
                        print(f"You have borrowed '{item.title}'.")

        elif choice == '2':
            title = input("Enter title of the item to return: ")
            items = admin.search_items("title", title)
            if items:
                item = items[0]
                if item in borrower.borrowed_items:
                    borrower.return_item(item)
                    print(f"You have returned '{item.title}'.")
                else:
                    print("You have not borrowed this item.")

        elif choice in {'3', '4', '5', '6', '7'}:
            if choice == '3':
                attribute = "title"
                value = input("Enter title: ")
            elif choice == '4':
                attribute = "category"
                value = input("Enter category: ")
            elif choice == '5':
                attribute = "language"
                value = input("Enter language: ")
            elif choice == '6':
                attribute = "year_published"
                value = int(input("Enter year published: "))
            elif choice == '7':
                attribute = "authors"
                value = input("Enter author: ")

            items = admin.search_items(attribute, value)
            print(f"Found {len(items)} item(s):")
            for item in items:
                authors = [str(author)for author in item.authors] if isinstance(item.authors, list) else [str(item.authors)]
                print(f" - {item.title} by {', '.join(authors)}")

        elif choice == '8':
            due_dates = borrower.get_due_dates()
            print("Due dates for borrowed items:")
            for title, due_date in due_dates.items():
                print(f" - {title}: {due_date.strftime('%Y-%m-%d')}")

        elif choice == '9':
            if borrower.has_fine():
                amount = borrower.get_fine_amount()
                print(f"Your fine amount is: ${amount}")
                pay = input("Do you want to pay the fine? (yes/no): ")
                if pay.lower() == 'yes':
                    borrower.pay_fine(amount)
                    print("Fine paid successfully.")
                else:
                    print("Fine not paid.")
            else:
                print("You have no fines.")

        elif choice == '10':
            print("Logging out.")
            break

        else:
            print("Invalid choice. Please try again.")

def admin_menu(admin):

    while True:
        print("\nAdministrator Menu")
        print("1. Search Item by Title")
        print("2. Search Item by Category")
        print("3. Search Item by Language")
        print("4. Search Item by Year Published")
        print("5. Search Item by Author")
        print("6. Display Item Details")
        print("7. Add New Item")
        print("8. Remove Item")
        print("9. Locate Borrowers with Unpaid Fines")
        print("10. List Items Borrowed by Borrower")
        print("11. Logout")
        choice = input("Enter your choice: ")

        if choice in {'1', '2', '3', '4', '5'}:
            if choice == '1':
                attribute = "title"
                value = input("Enter title: ")
            elif choice == '2':
                attribute = "category"
                value = input("Enter category: ")
            elif choice == '3':
                attribute = "language"
                value = input("Enter language: ")
            elif choice == '4':
                attribute = "year_published"
                value = int(input("Enter year published: "))
            elif choice == '5':
                attribute = "authors"
                value = input("Enter author: ")

            items = admin.search_items(attribute, value)
            print(f"Found {len(items)} item(s):")
            for item in items:
                authors = [str(author) for author in item.authors] if isinstance(item.authors, list) else [
                    str(item.authors)]
                print(f" - {item.title} by {', '.join(authors)}")

        elif choice == '6':
            title = input("Enter item title to display details: ").strip().lower()
            items = admin.search_items("title", title)
            if items:
                print(admin.display_item_details(items[0]))
            else:
                print(f"Item '{title}' not found.")


        elif choice == '7':
            title = input("Enter title: ")
            category = input("Enter category: ")
            language = input("Enter language: ")
            authors = input("Enter authors (comma-separated): ").split(', ')
            format = input("Enter format: ")
            year_published = int(input("Enter year published: "))
            new_item = Audiobook(title, category, language, authors, format, year_published)
            admin.add_item(new_item)
            print(f"AudioBook '{title}' added successfully.")


        elif choice == '8':
            title = input("Enter title of the item to remove: ")
            admin.remove_item(title)
            print(f"Item '{title}' removed successfully.")

        elif choice == '9':
            borrowers_with_fines = admin.locate_borrowers_with_unpaid_fines()
            print(f"Found {len(borrowers_with_fines)} borrower(s) with unpaid fines:")
            for borrower in borrowers_with_fines:
                print(f" - {borrower.first_name} {borrower.last_name} (Account: {borrower.account_number})")

        elif choice == '10':
            account_number = input("Enter borrower account number: ")
            items = admin.list_borrowed_items(account_number)
            if items:
                print(f"Borrower '{account_number}' has borrowed {len(items)} item(s):")
                for item in items:
                    print(f" - {item.title} by {', '.join(item.authors)}")
            else:
                print(f"No borrowed items found for account number '{account_number}'.")

        elif choice == '11':
            print("Logging out.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
