#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import argparse
import requests

def parse_args(args):
    """Get the command-line arguments to pass in the config file
    """
    parser = argparse.ArgumentParser(description='Mirror github repo(s) in gitlab.')
    parser.add_argument('config', help='yaml file containing repo urls')
    parser.add_argument('--apitoken', help='gitlab api token')
    return parser.parse_args()


def createrepos():
    """Create the repos to be mirrored in gitlab
    """
    parser = parse_args(sys.argv[1:])
    try:
        if not parser.apitoken:
            gitlabtoken = os.environ['GITLAB_API_PRIVATE_TOKEN']
        else:
            gitlabtoken = parser.apitoken
    except KeyError:
        sys.exit('No API private token provided')

    try:
        with open(parser.config) as datafile:
            repodata = yaml.load(datafile)
    except IOError:
        sys.exit('Cannot read file')

    headers = {'PRIVATE-TOKEN': gitlabtoken}
    gitlaburls = repodata.keys()
    for gitlaburl in gitlaburls:
        for item in repodata[gitlaburl]:
            data = {'name': item,
                    'namespace_id': repodata[gitlaburl][item]['gitlabgid'],
                    'import_url': repodata[gitlaburl][item]['github']
                   }
            r = requests.post(gitlaburl, headers=headers, data=data)
            print r.text

if __name__ == "__main__":
    parse_args(sys.argv[1:])
    createrepos()

