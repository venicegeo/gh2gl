#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import argparse
import requests

parser = argparse.ArgumentParser(description='Mirror github repo(s) in gitlab.')
parser.add_argument('config', help='yaml file containing repo urls')
parser.add_argument('--apitoken', help='gitlab api token')
args = parser.parse_args()

try:
    if not args.apitoken:
        gitlabtoken = os.environ['GITLAB_API_PRIVATE_TOKEN']
    else:
        gitlabtoken = args.apitoken
except KeyError:
    sys.exit('No API private token provided')

try:
    with open(args.config) as data:
        data = yaml.load(data)
except IOError:
    sys.exit('Cannot read file')

def createrepos(data):
    """Create the repos to be mirrored in gitlab
       Vars needed: name, gitlab, github, id
    """
    print 'creating repos'
    headers = {'PRIVATE-TOKEN': gitlabtoken}
    repos = data['repos']
    names = repos.keys()
    for name in names:
        url = repos[name][0]['gitlab']
        ghurl = repos[name][1]['github']
        glname = name
        glid = repos[name][2]['id']
        data = {'name': glname,
                'namespace_id': glid,
                'import_url': ghurl
               }
        print 'name: ', name, 'url: ', url, 'ghurl: ', ghurl, 'glname: ', glname, 'glid: ', glid
        r = requests.post(url, headers=headers, data=data)
        print r.text

if __name__ == "__main__":
    createrepos(data)

