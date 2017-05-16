#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import argparse
import requests
from urlparse import urlparse

def parse_args(args):
    """Get the command-line arguments to pass in the config file
    """
    parser = argparse.ArgumentParser(description='Mirror github repo(s) in gitlab.')
    parser.add_argument('config', help='yaml file containing repo urls')
    parser.add_argument('--apitoken', help='gitlab api token')
    return parser.parse_args()

def validate_datafile():
    parser = parse_args(sys.argv[1:])

    # Ensure an actual valid file was provided
    try:
        with open(parser.config) as datafile:
            repodata = yaml.load(datafile)
    except IOError:
        sys.exit('Cannot read file %s' % (parser.config))

    # Ensure proper keys and values in the file
    try:
        gitlaburls = repodata.keys()
        for gitlaburl in gitlaburls:
            if ('http' or 'https') not in urlparse(gitlaburl).scheme:
                raise KeyError('No valid gitlab url provided %s' % (gitlaburl))
            for item in repodata[gitlaburl]:
                if ('github' or 'gitlabgid') not in repodata[gitlaburl][item].keys():
                    raise KeyError('No gitlabgid or github for %s %s' % (item, repodata[gitlaburl][item].keys()))
                if ('http' or 'https') not in urlparse(repodata[gitlaburl][item]['github']).scheme:
                    raise ValueError('No valid github url provided %s %s' % (item, repodata[gitlaburl][item]['github']))
                if not isinstance(repodata[gitlaburl][item]['gitlabgid'], int):
                    raise ValueError('No gitlabgid %s %s' % (item, repodata[gitlaburl][item]['gitlabgid']))
    except Exception as e:
        sys.exit('Error in config file: %s' % (e))

    return repodata


def createrepos():
    """Create the repos to be mirrored in gitlab
    """
    parser = parse_args(sys.argv[1:])
    try:
        if not parser.apitoken:
            gitlabtoken = os.environ['GITLAB_API_PRIVATE_TOKEN']
        else:
            gitlabtoken = parser.apitoken
    #except KeyError:
    except Exception as e:
        sys.exit('No API private token provided %s' % (e))
    repodata = validate_datafile()
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
    createrepos()

