# -*- coding: utf-8 -*-
"""
    weppy.wsgi
    ----------

    Provide error, static and dynamic handlers for wsgi.

    :copyright: (c) 2014-2018 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

import os
import re
from datetime import datetime
from .globals import current
from .http import HTTP
from .stream import stream_file_handler

REGEX_STATIC = re.compile(
    '^/static/(?P<v>_\d+\.\d+\.\d+/)?(?P<f>.*?)$')
REGEX_STATIC_LANG = re.compile(
    '^/(?P<l>\w+/)?static/(?P<v>_\d+\.\d+\.\d+/)?(?P<f>.*?)$')


def dynamic_handler(app, environ, start_response):
    try:
        #: init current
        environ['wpp.application'] = app.name
        current.initialize(environ)
        #: dispatch request
        response = current.response
        app.route.dispatch()
        #: build HTTP response
        http = HTTP(
            response.status, response.output, response.headers,
            response.cookies)
    except HTTP as httpe:
        http = httpe
        #: render error with handlers if in app
        error_handler = app.error_handlers.get(http.status_code)
        if error_handler:
            output = error_handler()
            http = HTTP(http.status_code, output, response.headers)
        #: always set cookies
        http.set_cookies(response.cookies)
    return http.to(environ, start_response)


def static_handler(app, environ, start_response):
    path_info = environ['wpp.path_info']
    #: handle weppy assets (helpers)
    if path_info.startswith('/__weppy__'):
        filename = path_info[11:]
        static_file = os.path.join(
            os.path.dirname(__file__), 'assets', filename)
        #: avoid exposing html files
        if os.path.splitext(static_file)[1] == 'html':
            return HTTP(404).to(environ, start_response)
        return stream_file_handler(
            environ, start_response, static_file)
    #: handle app assets
    static_file, version = app.static_handler(app, path_info)
    if static_file:
        return stream_file_handler(
            environ, start_response, static_file, version)
    return dynamic_handler(app, environ, start_response)


def _lang_static_handler(app, path_info):
    static_match = REGEX_STATIC_LANG.match(path_info)
    if static_match:
        lang, version, filename = static_match.group('l', 'v', 'f')
        static_file = os.path.join(app.static_path, filename)
        if lang:
            lang_file = os.path.join(app.static_path, lang, filename)
            if os.path.exists(lang_file):
                static_file = lang_file
        return static_file, version
    return None, None


def _nolang_static_handler(app, path_info):
    if path_info.startswith('/static'):
        version, filename = REGEX_STATIC.match(path_info).group('v', 'f')
        static_file = os.path.join(app.static_path, filename)
        return static_file, version
    return None, None


def _pre_handler(app, environ, start_response):
    environ['wpp.path_info'] = environ['PATH_INFO'] or '/'
    return app.common_static_handler(app, environ, start_response)


def _pre_handler_prefix(app, environ, start_response):
    path_info = environ['PATH_INFO'] or ''
    if not path_info.startswith(app.route._prefix_main):
        return HTTP(404).to(environ, start_response)
    environ['wpp.path_info'] = path_info[app.route._prefix_main_len:] or '/'
    return app.common_static_handler(app, environ, start_response)


def error_handler(app, environ, start_response):
    environ['wpp.now'] = datetime.utcnow()
    try:
        return app._wsgi_pre_handler(app, environ, start_response)
    except Exception:
        if app.debug:
            from .debug import smart_traceback, debug_handler
            tb = smart_traceback(app)
            body = debug_handler(tb)
        else:
            body = None
            custom_handler = app.error_handlers.get(500, lambda: None)
            try:
                body = custom_handler()
            except Exception:
                pass
            if not body:
                body = '<html><body>Internal error</body></html>'
        app.log.exception('Application exception:')
        return HTTP(500, body).to(environ, start_response)
