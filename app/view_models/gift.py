"""
gift view model
"""
from collections import namedtuple

from app.view_models.book import BookViewModel


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        # gifts is a list of MyGift instance
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        tmp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            tmp_gifts.append(my_gift)
        return tmp_gifts

    def __matching(self, gift):
        """
        For a given gift, find the wish count of that gift
        :param gift: a Gift instance
        :return: a dict
        """
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'id': gift.id,
            'book': BookViewModel(gift.book),
            'wishes_count': count
        }
        return r
