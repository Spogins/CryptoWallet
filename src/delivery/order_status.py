import enum


class StatusOrder(enum.Enum):
    NEW = 'NEW'
    DELIVERY = 'DELIVERY'
    CLOSE = 'CLOSE'
    REFUND = 'REFUND'
    FAILED = 'FAILED'
