#!/usr/bin/python3

from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(filename='users.log', 
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route("/")
def index():
    app.logger.info("Processing default request")
    return """
        Welcome to our website!<br /><br />
        <a href="/hello">Go to hello world</a>
    """

@app.route("/hello")
def hello():
    return """
        Hello World!<br /><br />
        <a href="/">Back to index</a>
    """

if __name__ == '__main__':
    # Will make the server available externally as well
    app.run(host='0.0.0.0')
