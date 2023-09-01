import enum


class StatusOrder(enum.Enum):
    new = 'NEW'
    delivery = 'DELIVERY'
    finish = 'CLOSE'
    turning = 'REFUND'
    failed = 'FAILED'