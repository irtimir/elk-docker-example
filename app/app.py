import logging
import random

import logstash
import sentry_sdk
from flask import Flask, request
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(integrations=[FlaskIntegration()])
app = Flask(__name__)
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)

logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')


@app.route('/')
def index():
    result = random.randint(1, 50)
    app.logger.info(f'Пользователю досталось число {result}')
    return f"Ваше число {result}!"
