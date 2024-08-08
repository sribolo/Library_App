from Borrower_class import Borrower

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return
            current = current.next

    def find(self, criteria):
        current = self.head
        while current is not None:
            if criteria(current.data):
                return current.data
            current = current.next
        return None

    def find_all(self, criteria):
        current = self.head
        results = []
        while current is not None:
            if criteria(current.data):
                results.append(current.data)
            current = current.next
        return results

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

class BorrowerList:
    def __init__(self):
        self.borrowers = DoublyLinkedList()

    def add_borrower(self, borrower):
        self.borrowers.append(borrower)

    def remove_borrower(self, account_number):
        borrower_to_remove = self.find_borrower_by_account_number(account_number)
        if borrower_to_remove:
            self.borrowers.remove(borrower_to_remove)
            return f"Borrower '{account_number}' removed successfully."
        return f"Borrower '{account_number}' not found."

    def find_borrower_by_username(self, username):
        for borrower in self.borrowers:
            if borrower.username == username:
                return borrower
        return None

    def find_borrower_by_account_number(self, account_number):
        for borrower in self.borrowers:
            if borrower.account_number == account_number:
                return borrower
        return None


    def find_borrowers_with_unpaid_fines(self):
        return self.borrowers.find_all(lambda borrower: borrower.has_fine())
