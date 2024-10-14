import multiprocessing

workers = 2
worker_class = 'gevent'  # or 'sync' if async is not needed
# timeout = 60
# bind = "0.0.0.0:8000"
accesslog = '-'
errorlog = '-'
loglevel = 'debug'