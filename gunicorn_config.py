import os



workers = int(os.environ.get('GUNICORN_PROCESSES', '5'))

threads = int(os.environ.get('GUNICORN_THREADS', '10'))

timeout = int(os.environ.get('GUNICORN_TIMEOUT', '1200'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8081')



forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }