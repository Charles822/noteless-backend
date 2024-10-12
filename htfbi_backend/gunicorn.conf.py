import multiprocessing

workers = 3
worker_class = 'gevent'  # or 'sync' if async is not needed
timeout = 30
# bind = "0.0.0.0:8000"
accesslog = '-'
errorlog = '-'
loglevel = 'info'