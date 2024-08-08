from datetime import datetime, timedelta
class Item:
    def __init__(self, title, category, language, authors, year_published):
        self.title = title
        self.category = category
        self.language = language
        self.authors = authors
        self.year_published = year_published
        self.due_date = datetime.now() + timedelta(days=14)

    def __str__(self):
        authors = ', '.join(self.authors) if self.authors else 'Unknown'
        return (f"{self.title} by {authors}, Category: {self.category},"
                f" Language: {self.language}, Year: {self.year_published}, Due Date: {self.due_date.strftime('%Y-%m-%d')}")