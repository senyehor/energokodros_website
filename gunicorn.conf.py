import os

bind = f"[::]:{os.getenv('APP_PORT')}"
workers = 3
# Whether to send Django output to the error log
capture_output = True
loglevel = "info"
