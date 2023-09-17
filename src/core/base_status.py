import enum


class BaseStatus(enum.Enum):
    NEW = 'NEW'
    DELIVERY = 'DELIVERY'
    CLOSE = 'CLOSE'
    REFUND = 'REFUND'
    FAILED = 'FAILED'


class DeliveryStatus(enum.Enum):
    NEW = 'NEW'
    DELIVERY = 'DELIVERY'
    CLOSE = 'CLOSE'
    REFUND = 'REFUND'
    FAILED = 'FAILED'


class TransactionStatus(enum.Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'
    FAILED = 'FAILED'
