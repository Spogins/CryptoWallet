fastapi:

	uvicorn config_fastapi.app:app --reload --port 8000


socketio:

	uvicorn config_socketio.socket_app:socket_app --reload --port 8001


worker:

	celery -A config_celery.celery_app worker --loglevel=info


migration:

	alembic revision --autogenerate -m "migration"


migrate:

	alembic upgrade head


alembic:

	alembic init -t async migrations


celery_clear:

	celery purge


init_scripts:

	python init_scripts.py


asyncapi_docs:
	python src/chat/asyncapi/generator.py
	sudo ag asyncapi_docs.yaml @asyncapi/html-template -o static/async_api --force-write
	sudo mv static/async_api/index.html templates/asyncapi
	sudo chmod 746 templates/asyncapi/index.html







