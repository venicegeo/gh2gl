# Github to Gitlab Mirrorer

Have you ever wanted to mirror multiple github repositories in a gitlab instance?
Well, look no further because you've arrived at this project!

gh2gl is writtent in Python 2 and uses a yaml configuration file to specify
the urls and project ids to mirror 1 or a thousand github repos in gitlab.

## What you need

1. A github repo that you want to mirror. (Actually it can be any git repo 
that your gitlab instance can access).
2. Access to a gitlab instance
3. Your gitlab access tokens

## How to do it

1. Clone this repo or download it locally
2. Either add your access token as an environment variable: `GITLAB_API_PRIVATE_TOKEN=782fxBsiRGx7h-zkwZvx` or it can be supplied as an argument when you run gh2gl
3. Determine your gitlab group id:
`$ curl --header "PRIVATE-TOKEN: $GITLAB_API_PRIVATE_TOKEN" "localhost/api/v3/groups"`
3. Create your yaml configuration file similar to the [!](./sample.config.yaml) found here:
```
repos:
  githubproj:
    - gitlab: http://some.gitlab.yoursite.com/api/v3/projects
    - github: https://github.com/githuborg/githubproj
    - id: 2
  othergithubproj:
    - gitlab: http://some.gitlab.yoursite.com/api/v3/projects
    - github: https://github.com/githuborg/othergithubproj
    - id: 2
```
4. Use `$ gh2gl` to mirror your repositories, specifying the path to your configuration file:
```
usage: gh2gl.py [-h] [--apitoken APITOKEN] config

Mirror github repo(s) in gitlab.

positional arguments:
  config               yaml file containing repo urls

optional arguments:
  -h, --help           show this help message and exit
  --apitoken APITOKEN  gitlab api token
``` 

## Dependencies
- [requests](http://docs.python-requests.org/en/master/)
- [pyyaml](http://pyyaml.org/)

