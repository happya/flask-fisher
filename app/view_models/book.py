"""
book view model
"""

"""
single book
"""


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.author = ','.join(book['author'])
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.isbn = book['isbn']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


"""
a collection of books
"""


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, fisher_book, keyword):
        self.total = fisher_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in fisher_book.books]

