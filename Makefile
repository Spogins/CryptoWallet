fast_api:

	uvicorn config_fastapi.app:app --reload --port 8000


socketio:

	uvicorn config_socketio.app:socket_app --reload --port 8001


socket_connect:

	python3 config_socketio/connect.py


worker:

	celery -A config_celery.celery worker --loglevel=info




