import roger.api as api
from flask import Flask
from flask import render_template
from flask import send_from_directory

app = Flask(__name__, static_url_path='')


@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/components/<path:path>')
@app.route('/index_files/<path:path>')
@app.route('/static/<path:path>')
def send_css(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run()
