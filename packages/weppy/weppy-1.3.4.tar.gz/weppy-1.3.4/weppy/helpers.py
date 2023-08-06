# -*- coding: utf-8 -*-
"""
    weppy.helpers
    -------------

    Provides helping methods for applications.

    :copyright: (c) 2014-2018 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

import os
import re
from ._compat import string_types
from .libs.contenttype import contenttype

_REGEX_DBSTREAM = re.compile('(?P<table>.*?)\.(?P<field>.*?)\..*')


def abort(code, body=''):
    from .http import HTTP
    from .globals import current
    current.response.status = code
    raise HTTP(code, body)


def stream_file(path):
    from .globals import request, response
    from .expose import Expose
    from .stream import streamer
    fullfilename = os.path.join(Expose.application.root_path, path)
    raise streamer(request.environ, fullfilename, headers=response.headers)


def stream_dbfile(db, name):
    items = _REGEX_DBSTREAM.match(name)
    if not items:
        abort(404)
    (t, f) = (items.group('table'), items.group('field'))
    try:
        field = db[t][f]
    except AttributeError:
        abort(404)
    from pydal.exceptions import NotAuthorizedException, NotFoundException
    try:
        (filename, fullfilename) = field.retrieve(name, nameonly=True)
    except NotAuthorizedException:
        abort(403)
    except NotFoundException:
        abort(404)
    except IOError:
        abort(404)
    from .globals import request, response
    if isinstance(fullfilename, string_types):
        #: handle file uploads
        from .stream import streamer
        raise streamer(request.environ, fullfilename, headers=response.headers)
    else:
        #: handle blob fields
        from .http import HTTP
        response.headers['Content-Type'] = contenttype(filename)
        if 'wsgi.file_wrapper' in request.environ:
            data = request.environ['wsgi.file_wrapper'](fullfilename, 10**5)
        else:
            data = iter(lambda: fullfilename.read(10**5), '')
        raise HTTP(200, data, response.headers)


def flash(message, category='message'):
    #: Flashes a message to the next request.
    from .globals import session
    if session._flashes is None:
        session._flashes = []
    session._flashes.append((category, message))


def get_flashed_messages(with_categories=False, category_filter=[]):
    #: Pulls flashed messages from the session and returns them.
    #  By default just the messages are returned, but when `with_categories`
    #  is set to `True`, the return value will be a list of tuples in the
    #  form `(category, message)` instead.
    from .globals import session
    if not isinstance(category_filter, list):
        category_filter = [category_filter]
    try:
        flashes = list(session._flashes or [])
        if category_filter:
            flashes = list(filter(lambda f: f[0] in category_filter, flashes))
        for el in flashes:
            session._flashes.remove(el)
        if not with_categories:
            return [x[1] for x in flashes]
    except Exception:
        flashes = []
    return flashes


def load_component(url, target=None, content='loading...'):
    from .html import tag
    attr = {}
    if target:
        attr['_id'] = target
    attr['_data-wpp_remote'] = url
    return tag.div(content, **attr)
