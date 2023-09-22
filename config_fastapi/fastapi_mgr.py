import socketio
from starlette.templating import Jinja2Templates
from config.settings import RABBITMQ_URL

fastapi_mgr = socketio.AsyncAioPikaManager(RABBITMQ_URL, write_only=True)
templates = Jinja2Templates(directory='templates')