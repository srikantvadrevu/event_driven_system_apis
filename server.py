# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask import render_template
import flask_restful as restful

import os
import time
from datetime import datetime


app = Flask(__name__)
api = restful.Api(app)

# Long polling Example HTML
@app.route('/')
def index():
    return render_template('long_polling.html')

# Server Sent Events HTML Example
@app.route('/sse')
def test():
    return render_template('server_sent_events.html')

# Long polling Example API
class DataUpdate(restful.Resource):

    def _is_updated(self, request_time):
        """
        Returns if resource is updated or it's the first
        time it has been requested.
        args:
            request_time: last request timestamp
        """
        return os.stat('data.txt').st_mtime > request_time

    def get(self):
        """
        Returns 'data.txt' content when the resource has
        changed after the request time
        """
        request_time = time.time()
        while not self._is_updated(request_time):
            time.sleep(0.5)
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content,
                'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')}

# Server Sent Events API Example
@app.route('/stream')
def stream():
    def event_stream():
        while True:
            time.sleep(1)
            if True:
                yield "data:{}\n\n".format('hello! server time is ' + datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    return Response(event_stream(), mimetype="text/event-stream")

class Data(restful.Resource):

    def get(self):
        """
        Returns the current data content
        """
        content = ''
        with open('data.txt') as data:
            content = data.read()
        return {'content': content}

api.add_resource(DataUpdate, '/data-update')
api.add_resource(Data, '/data')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
