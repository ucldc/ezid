==========================
Test EZID Client with Auth
==========================
Test the EZID client on methods that require authentication. The tests are run against temporary test ids provided by the 99999 shoulder.
Require setting of environment variables EZID_USER and EZID_PWD 

    >>> import os
    >>> from EZID import EZIDClient
    >>> SERVER = "https://ezid.cdlib.org"
    >>> ez=EZIDClient(SERVER, credentials={'username':os.environ['EZID_USER'], 'password':os.environ['EZID_PWD']})
    >>> sid = ez.login()
    >>> ark = ez.mint('ark:/99999/fk4', {'_profile':'dc',})
    >>> resp = ez.update(ark, {'dc.title':'Test Title', 'dc.creator':'Test Creator', 'dc.publisher':'CDL', 'dc.date':'1965'})
    >>> resp = ez.view(ark)
    >>> print resp # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    success: ark:/99999/...
    _updated: ...
    _target: https://ezid.cdlib.org/id/ark:/99999/...
    _profile: dc
    dc.publisher: CDL
    _ownergroup: cdldsc
    dc.date: 1965
    _owner: cdldsc
    dc.creator: Test Creator
    _export: yes
    _created: ...
    _status: public
    dc.title: Test Title
    <BLANKLINE>
    >>> x=ez.logout()
    >>> print x # doctest: +NORMALIZE_WHITESPACE
    success: authentication credentials flushed
    <BLANKLINE>
