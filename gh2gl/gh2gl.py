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

def parse_args(args):
    # Get the command-line arguments to pass in the config file
    parser = argparse.ArgumentParser(description='Mirror github repo(s) in gitlab.')
    parser.add_argument('config', help='yaml file containing repo urls')
    parser.add_argument('--apitoken', help='gitlab api token')
    return parser.parse_args(args)


def createrepos(args):
    # Validate Inputs
    try:
        if not args.apitoken:
            gitlabtoken = os.environ['GITLAB_API_PRIVATE_TOKEN']
        else:
            gitlabtoken = args.apitoken
    except KeyError:
        print 'No API private token provided'
        raise

    try:
        with open(args.config) as datafile:
            repodata = yaml.load(datafile)
    except IOError:
        print 'Cannot read input file'
        raise
    except AttributeError:
        print 'File not valid yaml format'
        raise

    # Create the repos to be mirrored in gitlab
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
    parsed_args = parse_args(sys.argv[1:])
    createrepos(parsed_args)
