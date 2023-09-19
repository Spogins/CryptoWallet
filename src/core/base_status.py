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


class DeliveryStatus(enum.Enum):
    NEW = 'NEW'
    DELIVERY = 'DELIVERY'
    CLOSE = 'CLOSE'
    REFUND = 'REFUND'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'


class TransactionStatus(enum.Enum):
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'
    FAILED = 'FAILED'
