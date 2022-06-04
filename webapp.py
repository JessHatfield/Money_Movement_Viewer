from app import create_app

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s/%(funcName)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }, 'debug_rotating_file_handler': {
        'level': 'DEBUG',
        'formatter': 'default',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': 'debug.log',
        'mode': 'a',
        'maxBytes': 1048576,
        'backupCount': 10
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi','debug_rotating_file_handler']
    }
})

app = create_app()
