from flask import Flask
import os

import threading
event = threading.Event()

import logging
logging.basicConfig(format='[%(levelname)s]\t[%(asctime)s]\t%(message)s', level=20)

#from flask_cors import CORS 

environment = os.environ.get('FLASK_ENV')

if environment == 'development':
    from configuration.config import load_env_variables
    load_env_variables()

import routes
from utils.ibm import generate_iam_token
from utils.ibm import ThreadJob

set_interval = ThreadJob(generate_iam_token, event, 3000)
set_interval.start()

def create_app():
    app = Flask(__name__)
#    CORS(app)
#    app.config['CORS_HEADERS'] = 'Content-Type'
    # Init blueprints
    routes.init_app(app)
    return app

def init(app):
    logging.info('[INIT] Iniciando aplicación')
    generate_iam_token()

    port = int(os.getenv("PORT", 8080))

    if environment == 'development':
        app.run(host='0.0.0.0', port=port)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    # app.run()

if (__name__) == '__main__':
    init(create_app())