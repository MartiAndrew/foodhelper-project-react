include ../.env
 
run_gunicorn: 
	source ../.env && gunicorn --bind 0.0.0.0:$${GUNICORN_PORT} foodhelper.wsgi