import socketio
from config.settings import RABBITMQ_URL

fastapi_mgr = socketio.AsyncAioPikaManager(RABBITMQ_URL, write_only=True)