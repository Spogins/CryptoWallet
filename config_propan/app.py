from propan import RabbitBroker, PropanApp
from src.parser.consumers import parser_router

broker = RabbitBroker("amqp://guest:guest@localhost:5672")
broker.include_router(parser_router)
app = PropanApp(broker)