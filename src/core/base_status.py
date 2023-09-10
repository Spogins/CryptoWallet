import enum


class BaseStatus(enum.Enum):
    NEW = 'NEW'
    DELIVERY = 'DELIVERY'
    CLOSE = 'CLOSE'
    REFUND = 'REFUND'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'
    test = 'TEST'
