import roger.api as api
from flask import Flask
from flask import render_template
from flask import send_from_directory
import socketio
import eventlet
import eventlet.wsgi
import threading
from web.util import capitalize_first_letter

sio = socketio.Server()
app = Flask(__name__, static_url_path='')


def send_poet_lines(sid, seed_words):
    print('sending poet lines, %s, %s' % (sid, seed_words))
    sio.emit('line feed', 'line from thread... <br/>', room=sid)
    for line in api.generate('../roger/MODEL.db', seed_words):
        print('Sending line: %s to room %s' % (line, sid))
        sio.emit('line feed', line, room=sid)
    print("Leaving function send poet lines...")


@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/static/<path:path>')
def send_css(path):
    return send_from_directory('static', path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@sio.on('connect', namespace='/')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('poet request', namespace='/')
def message(sid, seed_words):
    print("poet request: %s " % seed_words)
    # threading.Thread(target=send_poet_lines, args=(sid, data)).start()
    for line in api.generate('../roger/MODEL.db', seed_words):
        line = capitalize_first_letter(line)
        sio.emit('line feed', line + '<br/>', room=sid)
        print('emitted line: %s' % line)



@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)