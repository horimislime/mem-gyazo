__author__ = 'horimislime'

from flask import (Flask, request, render_template, redirect, url_for, make_response, abort)
from werkzeug.routing import BaseConverter
import memcache
import hashlib

client = memcache.Client(['127.0.0.1:11211'])
app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


class Image(object):
    def __init__(self, raw_data, mime_type):
        self.raw_data = raw_data
        self.mime_type = mime_type

    def raw_data(self):
        return self.raw_data

    def mime_type(self):
        return self.mime_type


@app.route('/<regex("[a-z0-9]+"):key>.png')
def get_image(key):
    response = make_response()
    image = client.get(str(key))
    if image is None:
        abort(404)

    response.data = image.raw_data
    response.headers['Content-Type'] = image.mime_type

    return response

@app.route('/drop', methods=['GET'])
def drop():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def post():
    uploaded_image = request.files['imagedata']
    image = Image(uploaded_image.stream.read(), uploaded_image.content_type)

    md5 = hashlib.md5()
    md5.update(str(image.raw_data))
    key = md5.hexdigest()
    client.set(key, image)
    
    return 'http://%s/%s.png' % (request.host, key)


def make_app(global_conf={}):
    app.debug = False
    return app

if __name__ == '__main__':
    app.debug=True
    app.run()
