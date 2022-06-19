web: daphne hssc.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A hssc.celery worker -l info
celerybeat: celery -A hssc beat -l INFO
celeryworker: celery -A hssc.celery worker & celery -A hssc beat -l INFO & wait -n