fastapi:

	uvicorn config_fastapi.app:app --reload --port 8000


socketio:

	uvicorn config_socketio.socket_app:socket_app --reload --port 8001


socket_connect:

	python3 config_socketio/connect.py


connect_to_chat:

	python3 config_socketio/connect_to_chat.py


worker:

	celery -A config_celery.celery_app worker --loglevel=info


migration:

	alembic revision --autogenerate -m "migration"


migrate:

	alembic upgrade head






