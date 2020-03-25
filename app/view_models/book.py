"""
book view model
"""

"""
single book
"""


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.author =  ','.join(book['author'])
        self.publisher =  book['publisher']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']


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


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total':  0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            # returned['books'] = [cls.__cur_book_data(data)]
            returned['books'] = [cls.__cur_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            # returned['books'] = [cls.__cur_book_data(book) for book in data['books']]
            returned['books'] = [cls.__cur_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cur_book_data(cls, book):
        """
        tailor original data to get the desired information
        :param data:
        :return:
        """
        result = {
            'title': book['title'],
            'author': ','.join(book['author']),
            'publisher': book['publisher'],
            'pages': book['pages'] or '',
            'price': book['price'],
            'summary': book['summary'] or '',
            'image': book['image']
        }
        return result
