import traceback

import flask
import gevent.pywsgi

class Request:
    def __init__(self, method, ip, data, path, cookies):
        self.method = method
        self.ip = ip
        self.data = data
        self.path = path
        self.cookies = cookies

class Application:
    def __init__(self, name):
        self.app = flask.Flask(name, root_path = 'static/', template_folder = '.')
        self.events = {}
        self.error_handlers = {}

    def register_event(self, path, handler, index = 1):
        self.events[index] = {'path': path, 'class': handler}

    def register_error_handler(self, handler, index = 1):
        self.error_handlers[index] = {'class': handler}

    def register_routes(self):
        @self.app.route('/', methods = ['GET', 'POST'])
        @self.app.route('/<path:path>', methods = ['GET', 'POST'])
        def _handler(path = ''):
            try:
                for key, value in dict(sorted(self.events.items())).items():
                    if '/' + path == value['path'] or path == value['path'] or value['path'] == '*':
                        response = value['class'].call(Request(flask.request.method, flask.request.remote_addr, flask.request.form.to_dict() if flask.request.method == 'POST' else flask.request.args.to_dict(), path, flask.request.cookies))
                        if response:
                            return response
            except:
                for key, value in dict(sorted(self.error_handlers.items())).items():
                    response = value['class'].call(message = str(traceback.format_exc()))
                    if response:
                        return response

    def run(self, host = '0.0.0.0', port = 80, server_key = '', server_crt = ''):
        if not server_crt:
            gevent.pywsgi.WSGIServer((host, port), self.app).serve_forever()
        else:
            gevent.pywsgi.WSGIServer((host, port), self.app, keyfile = server_key, certfile = server_crt).serve_forever()