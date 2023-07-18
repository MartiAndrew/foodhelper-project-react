include infra/.env

run_gunicorn:
	source infra/.env && gunicorn --bind 0.0.0.0:$${GUNICORN_PORT} foodhelper.wsgi