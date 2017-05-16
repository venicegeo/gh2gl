# Copyright 2016, RadiantBlue Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import argparse
import requests
from urlparse import urlparse

def parse_args(args):
    # Get the command-line arguments to pass in the config file
    parser = argparse.ArgumentParser(description='Mirror github repo(s) in gitlab.')
    parser.add_argument('config', help='yaml file containing repo urls')
    parser.add_argument('--apitoken', help='gitlab api token')
    return parser.parse_args(args)

def validate_datafile(args):
    # Ensure an actual valid file was provided
    try:
        with open(args.config) as datafile:
            repodata = yaml.load(datafile)
    except IOError:
        print 'Cannot read file %s' % (args.config)
        raise

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
        print 'Error in config file: %s' % (e)
        raise

    return repodata


def createrepos(args):
    # Validate Inputs
    try:
        if not args.apitoken:
            gitlabtoken = os.environ['GITLAB_API_PRIVATE_TOKEN']
        else:
            gitlabtoken = args.apitoken
    except Exception as e:
        print 'No API private token provided %s' % (e)
        raise

    repodata = validate_datafile(args)
    headers = {'PRIVATE-TOKEN': gitlabtoken}

    gitlaburls = repodata.keys()
    for gitlaburl in gitlaburls:
        for item in repodata[gitlaburl]:
            data = {
                'name': item,
                'namespace_id': repodata[gitlaburl][item]['gitlabgid'],
                'import_url': repodata[gitlaburl][item]['github']
                }
            try:
                resp = requests.post(gitlaburl, headers=headers, data=data)
                resp.raise_for_status()
            except requests.ConnectionError:
                print "GitLab URL {} failed for GitHub Repo {}".format(gitlaburl, data['import_url'])
                raise

if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    createrepos(parsed_args)
