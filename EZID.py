#    ! /usr/bin/env python

'''EZID client: Module to make using EZID easier from python.

Can use this as a client command line program or pull the EZIDClient object
into other programs
Following the samples from: https://ezid.cdlib.org/doc/apidoc.html
'''

__author__ = "Mark Redar"
__copyright__ = "Copyright 2011, The Regents of the University of California"
__credits__ = ["Greg Janee", ]
__license__ = "BSD"
__version__ = "0.2"
__maintainer__ = "Mark Redar"
__email__ = "mark.redar@ucop.edu"
__status__ = "Prototype"

import re
import sys
import types
import urllib2

__all__=('EZIDClient', 'formatAnvlFromDict', 'formatAnvlFromList')

SERVER = "https://ezid.cdlib.org"

operations = {
    # operation : number of arguments
    "mint" : lambda l: l%2 == 1,
    "create" : lambda l: l%2 == 1,
    "view" : 1,
    "update" : lambda l: l%2 == 1,
    "delete" : lambda l: l%2 == 1,
    "login" : 0,
    "logout" : 0
}

_usageText = """Usage: client credentials operation...

    credentials
        username:password
        sessionid (as returned by previous login)
        - (none)

    operation
        m[int] shoulder [label value label value ...]
        c[reate] identifier [label value label value ...]
        v[iew] identifier
        u[pdate] identifier [label value label value ...]
        d[elete] identifier
        login
        logout
"""

def _usageError ():
    sys.stderr.write(_usageText)
    sys.exit(1)

class _MyHTTPErrorProcessor (urllib2.HTTPErrorProcessor):
    def http_response (self, request, response):
        # Bizarre that Python leaves this out.
        if response.code == 201:
            return response
        else:
            return urllib2.HTTPErrorProcessor.http_response(self, request,
                response)
    https_response = http_response

def formatAnvlFromDict(d):
    '''Produce anvl formatted text from a dict of name value pairs.
    Values should be simple data types

    >>> formatAnvlFromDict({'dc.title':'test title', 'dc.creator':'mer',})
    'dc.creator: mer\\ndc.title: test title'
    '''
    r = []
    for k, v in d.items():
        label = re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), k)
        value = re.sub("[%\r\n]", lambda c: "%%%02X" % ord(c.group(0)), v)
        r.append("%s: %s" % (label, value))
    return "\n".join(r)

def formatAnvlFromList (l):
    '''Produce anvl formatted text from a list of name-value pairs.
    Values should be simple data types.
    >>> formatAnvlFromList( ['dc.title', 'test title', 'dc.creator', 'mer'])
    'dc.title: test title\\ndc.creator: mer'
    '''

    r = []
    for i in range(0, len(l), 2):
        k = re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), l[i])
        v = re.sub("[%\r\n]", lambda c: "%%%02X" % ord(c.group(0)), l[i+1])
        r.append("%s: %s" % (k, v))
    return "\n".join(r)


class EZIDClient(object):
    '''Class for conducting EZID transactions
    Use http if has session_id, else need credentials for most operations


    >>> ez=EZIDClient()
    >>> info = ez.view('ark:/13030/c88s')
    Traceback (most recent call last):
        ...
    HTTPError: HTTP Error 400: BAD REQUEST
    >>> info = ez.view('ark:/13030/c88s4n09')
    >>> for x in info.split('\\n'):
    ...     print x
    success: ark:/13030/c88s4n09
    _updated: 1319652711
    dc.date: 1957
    _target: http://content.cdlib.org/ark:/13030/c88s4n09/
    _profile: dc
    dc.publisher: San Jose State University Special Collections & Archives
    _ownergroup: cdldsc
    _owner: cdldsc
    dc.creator: Wang Shifu
    _export: yes
    _created: 1302192449
    _status: public
    dc.title: "The Romance of the West Chamber," a Classic of Chinese Literature
    <BLANKLINE>
    >>> sid = ez.login()
    Traceback (most recent call last):
        ...
    HTTPError: HTTP Error 401: UNAUTHORIZED
    >>> ark = ez.mint('ark:/99999/fk4')
    Traceback (most recent call last):
        ...
    HTTPError: HTTP Error 401: UNAUTHORIZED
    '''
    def __init__(self, server=SERVER, proxy=None, credentials=None, session_id=None):
        self._proxy = proxy # dict of http, https proxies
        proxy_handler = None
        if self._proxy:
            proxy_handler = urllib2.ProxyHandler(self._proxy)
            self._opener = urllib2.build_opener(proxy_handler, _MyHTTPErrorProcessor())
        else:
            self._opener = urllib2.build_opener(_MyHTTPErrorProcessor())
        self._server = server
        self._credentials = credentials # dict of username, password
        self._session_id = session_id
        self._cookie = None
        if self._session_id:
            self._cookie = "sessionid=" + session_id
        if self._credentials:
            h = urllib2.HTTPBasicAuthHandler()
            h.add_password("EZID", self._server, self._credentials['username'], self._credentials['password'])
            self._opener.add_handler(h)

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, sid):
        self._session_id = sid
        if self._session_id:
            self._cookie = "sessionid=" + self._session_id

    def _get_request(self, request, login=False):
        if self._cookie: request.add_header("Cookie", self._cookie)
        try:
            c = self._opener.open(request)
        except urllib2.HTTPError as e:
            print  e.read()
            raise
        output = c.read()
        if not output.endswith("\n"): output += "\n"
        if login:
            output = c.info()["set-cookie"].split(";")[0].split("=")[1]
        return output

    def view(self, identifier):
        '''View an id. If id is public, no login or session id required
        for public ids.
        '''
        url = "%s/id/%s" % (self._server, identifier)
        request = urllib2.Request(url)
        return self._get_request(request)

    def login(self):
        '''Login, caching session id
        '''
        request = urllib2.Request("%s/%s" % (self._server, 'login'))
        self.session_id = self._get_request(request, login=True)
        return self.session_id

    def logout(self):
        '''logout, caching session id
        '''
        request = urllib2.Request("%s/%s" % (self._server, 'logout'))
        self.session_id = self._get_request(request)
        return self.session_id

    def update(self, identifier, data):
        if not self.session_id:
            self.session_id = self.login()
        request = urllib2.Request("%s/id/%s" % (self._server, identifier))
        request.get_method = lambda: "POST"
        request.add_header("Content-Type", "text/plain; charset=UTF-8")
        request.add_data(formatAnvlFromDict(data).encode("UTF-8"))
        return self._get_request(request)

    def create(self, identifier, data=None):
        if not self.session_id:
            self.session_id = self.login()
        request = urllib2.Request("%s/id/%s" % (self._server, identifier))
        request.get_method = lambda: "PUT"
        if data:
            request.add_header("Content-Type", "text/plain; charset=UTF-8")
            request.add_data(formatAnvlFromDict(data).encode("UTF-8"))
        return self._get_request(request)

    def mint(self, shoulder, data=None):
        '''Mint a new identifier on EZID. Return the identifier if successful
        '''
        if not self.session_id:
            self.session_id = self.login()
        request = urllib2.Request("%s/shoulder/%s" % (self._server, shoulder))
        request.get_method = lambda: "POST"
        if data:
            request.add_header("Content-Type", "text/plain; charset=UTF-8")
            request.add_data(formatAnvlFromDict(data).encode("UTF-8"))
        return self._get_request(request).replace('success: ','').strip()

    def delete(self, identifier):
        if not self.session_id:
            self.session_id = self.login()
        request = urllib2.Request("%s/id/%s" % (self._server, identifier))
        request.get_method = lambda: "DELETE"
        request.add_header("Content-Type", "text/plain; charset=UTF-8")
        return self._get_request(request)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Begin command line code
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def process_args(args):
    if len(args) < 3: _usageError()
    credentials = session_id = identifier = data = None
    if ":" in args[1]:
        u, p = args[1].split(':', 1)
        credentials = dict(username=u, password=p)
    elif args[1] != "-":
        sessionid=args[1]
    operation = [o for o in operations if o.startswith(args[2])]
    if len(operation) != 1: _usageError()
    operation = operation[0]
    if (type(operations[operation]) is int and\
        len(args)-3 != operations[operation]) or\
        (type(operations[operation]) is types.LambdaType and\
        not operations[operation](len(args)-3)): _usageError()
    identifier = args[3] if len(args) > 3 else None
    if operation in ["mint", "create", "update",] :
        if len(args) > 4:
            l = args[4:]
            data = {}
            for i in range(0, len(l), 2):
                data[l[i]] = l[i+1]
    return credentials, session_id, operation, identifier, data

def main(argvin=sys.argv):
    '''Mimics client sample from api docs
    '''
    #opener, request, operation = processargs(argvin)
    credentials, session_id, operation, identifier, data = process_args(argvin)
    ezid = EZIDClient(SERVER, credentials=credentials, session_id=session_id)
    try:
        if operation == 'login':
            print ezid.login()
        elif operation == 'view':
            print ezid.view(identifier)
        elif operation == 'update':
            if data:
                print ezid.update(identifier, data)
        elif operation == 'delete':
            print ezid.delete(identifier)
        elif operation == 'create':
            print ezid.create(identifier, data)
        elif operation == 'mint':
            print 'MINTING\n'
            print ezid.mint(identifier, data)
    except urllib2.HTTPError, e:
        print e.code, e.msg
        if e.fp:
            print e.fp.read()

if __name__=='__main__':
    main(sys.argv)
