from Item_class import Item
from datetime import datetime, timedelta
class Audiobook(Item):
    def __init__(self, title, category, language, authors, format, year_published):
        super().__init__(title, category, language, authors, year_published)
        self.format = format
        self.due_date = datetime.now() + timedelta(days=14)


    def __str__(self):
        return f"Audiobook: {super().__str__()}, Format: {self.format}"
