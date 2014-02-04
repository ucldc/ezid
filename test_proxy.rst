==============================
Test EZID Client through proxy
==============================
Test the EZID client working through a proxy.
Should test the authenticated interface as well

You'll need to set up a proxy and change the settings below to match the proxy.


    >>> import os
    >>> from EZID import EZIDClient
    >>> SERVER = "http://ezid.cdlib.org"
    >>> proxy_http = os.environ.get('EZID_PROXY_HTTP', 'http://localhost:8000')
    >>> proxy_https = os.environ.get('EZID_PROXY_HTTPS', 'https://localhost:8000')
    >>> proxy = dict(http=proxy_http, https=proxy_https)
    >>> ez=EZIDClient(SERVER, proxy=proxy)
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
    _created: 1302192449
    _status: public
    dc.title: "The Romance of the West Chamber," a Classic of Chinese Literature
    <BLANKLINE>
