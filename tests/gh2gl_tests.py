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

from gh2gl import gh2gl
import os
import requests
import requests_mock

from mock import patch
from nose.tools import assert_raises

def test_argument_parsing():
	# Successful parse
	parsed_args = gh2gl.parse_args(['no_config.yaml', '--apitoken', 'test1234'])
	assert parsed_args.apitoken == 'test1234'
	assert parsed_args.config == 'no_config.yaml'
	parsed_args = gh2gl.parse_args(['no_config.yaml'])
	assert parsed_args.config == 'no_config.yaml'
	assert parsed_args.apitoken == None
	# Errors detected
	assert_raises(BaseException, gh2gl.parse_args, ['--apitoken', 'test1234'])
	assert_raises(BaseException, gh2gl.parse_args, [])

def test_create_repos_invalid_token():
	parsed_args = gh2gl.parse_args(['no_config.yaml'])
	# Mock environment to ensure no Token is set
	with patch.dict('os.environ'):
		assert_raises(KeyError, gh2gl.createrepos, parsed_args)

def test_create_repos_no_file_exists():
	parsed_args = gh2gl.parse_args(['no_config.yaml', '--apitoken', 'test1234'])
	assert_raises(IOError, gh2gl.createrepos, parsed_args)

def test_create_repos_invalid_yaml():
	parsed_args = gh2gl.parse_args(['tests/data/invalid_yaml.yaml', '--apitoken', 'test1234'])
	assert_raises(AttributeError, gh2gl.createrepos, parsed_args)

def test_create_repos_incomplete_yaml():
	parsed_args = gh2gl.parse_args(['tests/data/incomplete_config.yaml', '--apitoken', 'test1234'])
	assert_raises(KeyError, gh2gl.createrepos, parsed_args)
	parsed_args = gh2gl.parse_args(['tests/data/incomplete_config_2.yaml', '--apitoken', 'test1234'])
	assert_raises(KeyError, gh2gl.createrepos, parsed_args)
	parsed_args = gh2gl.parse_args(['tests/data/incomplete_config_3.yaml', '--apitoken', 'test1234'])
	assert_raises(TypeError, gh2gl.createrepos, parsed_args)

def test_create_repos_invalid_url():
	parsed_args = gh2gl.parse_args(['tests/data/invalid_config.yaml', '--apitoken', 'test1234'])
	assert_raises(ValueError, gh2gl.createrepos, parsed_args)

def test_create_repos_invalid_gitlab_id():
	parsed_args = gh2gl.parse_args(['tests/data/invalid_config_2.yaml', '--apitoken', 'test1234'])
	assert_raises(ValueError, gh2gl.createrepos, parsed_args)

def test_create_repos_timeout():
	parsed_args = gh2gl.parse_args(['tests/data/test_config.yaml', '--apitoken', 'test1234'])
	assert_raises(requests.ConnectionError, gh2gl.createrepos, parsed_args)

def test_create_repos_success():
	parsed_args = gh2gl.parse_args(['tests/data/test_config.yaml', '--apitoken', 'test1234'])
	# Mock a successful HTTP Response
	with requests_mock.mock() as mock:
		mock.post('http://1.2.3.4.5/api/v3/projects', text='success')
		gh2gl.createrepos(parsed_args)