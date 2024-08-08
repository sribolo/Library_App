from Item_class import Item
from datetime import datetime, timedelta

class Periodical(Item):
    def __init__(self, title, category,language, authors, year_published):
        super().__init__(title, category, language, authors, year_published)
        self.due_date = datetime.now() + timedelta(days=14)

    def __str__(self):
        return super().__str__()