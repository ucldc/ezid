import os,json
from datacite import DataCiteMDSClient, schema40
from EZID import EZIDClient

SERVER = "https://ezid.cdlib.org"
ez=EZIDClient(SERVER,
credentials={'username':os.environ['EZID_USER'],
'password':os.environ['EZID_PWD']})
sid = ez.login()

infile = open('example.json','r')
metadata = json.load(infile)
assert schema40.validate(metadata)
#Debugging if this fails
#v = datacite.schema40.validator.validate(metadata)
#errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
#for error in errors:
#        print(error.message)

xml = schema40.tostring(metadata)

resp = ez.mint('doi:10.5072/FK2', {'datacite':xml})
print(resp)
#resp = ez.mint('doi:10.5072/FK2',{'datacite.title': 'test title',
#        'datacite.creator': 'mer','datacite.publisher':
#        'CD','datacite.publicationyear':'2017','datacite.resourcetype':'Dataset'})
#print(resp)
doi = resp.split('|')[0].split()[0]#.decode('utf-8')
print(doi)

#print('doi:10.5072/FK2K64J47Z')
resp = ez.update(doi,{'_target':"http://www.caltech.edu"})
print(resp)

