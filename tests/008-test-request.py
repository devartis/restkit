# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license.
# See the NOTICE for more information.

import os
import uuid
from restkit import request
from restkit.forms import multipart_form_encode
from restkit.py3compat import StringIO

from . import t
from ._server_test import HOST, PORT

LONG_BODY_PART = """This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client...
This is a relatively long body, that we send to the client..."""

def test_001():
    u = "http://%s:%s" % (HOST, PORT)
    r = request(u)
    t.eq(r.status_int, 200)
    t.eq(r.body_string(), "welcome")

def test_002():
    u = "http://%s:%s" % (HOST, PORT)
    r = request(u, 'POST', body=LONG_BODY_PART)
    t.eq(r.status_int, 200)
    body = r.body_string()
    t.eq(len(body), len(LONG_BODY_PART))
    t.eq(body, LONG_BODY_PART)

def test_003():
     u = "http://test:test@%s:%s/auth" % (HOST, PORT)
     r = request(u)
     t.eq(r.status_int, 200)
     u = "http://test:test2@%s:%s/auth" % (HOST, PORT)
     r = request(u)
     t.eq(r.status_int, 403)

def test_004():
    u = "http://%s:%s/multipart2" % (HOST, PORT)
    fn = os.path.join(os.path.dirname(__file__), "1M")
    f = open(fn, 'rb')
    l = int(os.fstat(f.fileno())[6])
    b = {'a':'aa','b':['bb','éàù@'], 'f':f}
    h = {'content-type':"multipart/form-data"}
    body, headers = multipart_form_encode(b, h, uuid.uuid4().hex)
    r = request(u, method='POST', body=body, headers=headers)
    t.eq(r.status_int, 200)
    t.eq(int(r.body_string()), l)

def test_005():
    u = "http://%s:%s/multipart3" % (HOST, PORT)
    fn = os.path.join(os.path.dirname(__file__), "1M")
    f = open(fn, 'rb')
    l = int(os.fstat(f.fileno())[6])
    b = {'a':'aa','b':'éàù@', 'f':f}
    h = {'content-type':"multipart/form-data"}
    body, headers = multipart_form_encode(b, h, uuid.uuid4().hex)
    r = request(u, method='POST', body=body, headers=headers)
    t.eq(r.status_int, 200)
    t.eq(int(r.body_string()), l)

def test_006():
    u = "http://%s:%s/multipart4" % (HOST, PORT)
    fn = os.path.join(os.path.dirname(__file__), "1M")
    f = open(fn, 'rb')
    content = f.read()
    f.seek(0)
    b = {'a':'aa','b':'éàù@', 'f':f}
    h = {'content-type':"multipart/form-data"}
    body, headers = multipart_form_encode(b, h, uuid.uuid4().hex)
    r = request(u, method='POST', body=body, headers=headers)
    t.eq(r.status_int, 200)
    t.eq(r.body_string(), content)

def test_007():
    u = "http://%s:%s/multipart4" % (HOST, PORT)
    content = 'éàù@'
    f = StringIO('éàù@')
    f.name = 'test.txt'
    b = {'a':'aa','b':'éàù@', 'f':f}
    h = {'content-type':"multipart/form-data"}
    body, headers = multipart_form_encode(b, h, uuid.uuid4().hex)
    r = request(u, method='POST', body=body, headers=headers)
    t.eq(r.status_int, 200)
    t.eq(r.body_string(), content)
