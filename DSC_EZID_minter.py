#! /usr/bin/env python

# Digital Special Collection minter for new arks from ezid
# Set the default metadata profile to dc (_profile dc)
# Save the new ark in a text file for later reference
# Currently, EZID does not provide a list of your arks
# You must save the ark somewhere for recall

import os, sys
import datetime
from EZID import EZIDClient
from config_reader import read_config
import plac

EZID_index = os.path.join(os.environ['HOME'], 'indexes/EZID.txt')

dbs = read_config()

USERNAME = dbs['EZID']['USER']
PASSWORD = dbs['EZID']['PASSWORD']
SHOULDER = dbs['EZID']['SHOULDER']

def save_new_id(ark):
    '''Save the ark to the index, just a text file for now
    '''
    with open(EZID_index, 'a+') as f:
        f.write(ark.strip()+','+datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%S')+'\n')

@plac.annotations(
    number=("Number of new ARKs to mint", 'positional', None, int),
    shoulder=("EZID shoulder to mint from", 'option', None, str),
)
def main(number, shoulder=SHOULDER):
    ezid = EZIDClient(credentials=dict(username=USERNAME, password=PASSWORD))
    new_ids = []
    for x in range(0, number):
        ez = ezid.mint(shoulder=SHOULDER, data={'_profile':'dc',})
        save_new_id(ez)
        new_ids.append(ez)
    return new_ids 

if __name__=='__main__':
    new_ids = plac.call(main)
    for ez in new_ids:
        print ez
