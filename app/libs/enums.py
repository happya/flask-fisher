"""
author: yyi
"""

from enum import Enum


class PendingStatus(Enum):
    """
    trading status
    """
    Waiting = 1
    Success = 2
    Reject = 3
    Withdraw = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting: {
                'requester': 'Waiting the gifter to send',
                'gifter': 'Waiting you to send'
            },
            cls.Reject: {
                'requester': 'Your request was rejected',
                'gifter': 'You have rejected the request'
            },
            cls.Withdraw: {
                'requester': 'You have withdrew the request',
                'gifter': 'The request has been withdrawn'
            },
            cls.Success: {
                'requester': 'The book is on delivery to you',
                'gifter': 'Your gift is on delivery, transaction succeeds'
            }
        }
        return key_map[status][key]
