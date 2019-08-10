release: cd backend && python manage.py migrate --noinput
web: cd backend && gunicorn weatherwarner.wsgi --log-file -
