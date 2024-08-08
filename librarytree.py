
class Node:
    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.left = None
        self.right = None
class LibraryTree:
    def __init__(self):
        self.root = None

    def insert(self, item):
        key = item.title
        if self.root is None:
            self.root = Node(key, item)
        else:
            self._insert_recursive(self.root, key, item)


    def _insert_recursive(self, node, key, item):
        if key < node.key:
            if node.left is None:
                node.left = Node(key, item)
            else:
                self._insert_recursive(node.left, key, item)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, item)
            else:
                self._insert_recursive(node.right, key, item)

    def find(self, title):
        return self._find(self.root, title)

    def _find(self, node, title):
        if node is None:
            return None
        if title == node.item.title:
            return node.item
        elif title < node.item.title:
            return self._find(node.left, title)
        else:
            return self._find(node.right, title)

    def remove(self, title):
        self.root, deleted_node = self._remove(self.root, title)
        return deleted_node

    def _remove(self, node, title):
        if node is None:
            return node, None
        if title < node.item.title:
            node.left, deleted_node = self._remove(node.left, title)
        elif title > node.item.title:
            node.right, deleted_node = self._remove(node.right, title)
        else:
            if node.left is None:
                return node.right, node
            elif node.right is None:
                return node.left, node
            temp_val = self._min_value_node(node.right)
            node.item = temp_val.item
            node.right, _ = self._remove(node.right, temp_val.item.title)
            deleted_node = node
        return node, deleted_node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search_by_title(self, title):
        return self._search(self.root, lambda item: title.lower() in item.title.lower())

    def search_by_category(self, category):
        return self._search(self.root, lambda item: category.lower() in item.category.lower())

    def search_by_language(self, language):
        return self._search(self.root, lambda item: language.lower() in item.language.lower())

    def search_by_year_published(self, year_published):
        return self._search(self.root, lambda item: item.year_published == year_published)

    def search_by_author(self, author):
        return self._search(self.root, lambda item: author.lower() in (auth.lower() for auth in item.authors))


    def _search(self, node, criteria):
        results = []
        self._search_recursive(node, criteria, results)
        return results

    def search_items(self, attribute, value):
        found_items = []
        print(f"Searching for {attribute} = {value}")
        for item in self.library_tree:
            print(f"Checking item: {item.title}")
            if attribute == "title":
                if item.title.lower() == value.lower():
                    print(f"Found match for title: {item.title}")
                    found_items.append(item)
            elif attribute == "category":
                if item.category.lower() == value.lower():
                    print(f"Found match for category: {item.category}")
                    found_items.append(item)
            elif attribute == "language":
                if item.language.lower() == value.lower():
                    print(f"Found match for language: {item.language}")
                    found_items.append(item)
            elif attribute == "year_published":
                if item.year_published == value:
                    print(f"Found match for year_published: {item.year_published}")
                    found_items.append(item)
            elif attribute == "authors":
                if value.lower() in [author.lower() for author in item.authors]:
                    print(f"Found match for authors: {item.authors}")
                    found_items.append(item)
        print(f"Found {len(found_items)} items")
        return found_items

    def _search_recursive(self, node, criteria, results):
        if node is not None:
            if criteria(node.item):
                results.append(node.item)
            self._search_recursive(node.left, criteria, results)
            self._search_recursive(node.right, criteria, results)



    def display_paginated(self, page, items_per_page):
        all_items = []
        self._inorder_traversal(self.root, all_items)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        return all_items[start:end]

    def _inorder_traversal(self, node, items):
        if node is not None:
            self._inorder_traversal(node.left, items)
            items.append(node.item)
            self._inorder_traversal(node.right, items)

    def __str__(self):
        items = []
        self._inorder_traversal(self.root, items)
        return "LibraryTree: " + ", ".join(str(item) for item in items)
