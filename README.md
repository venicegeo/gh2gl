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
3. Determine your gitlab group id from the `"id"` field:
        $ curl --header "PRIVATE-TOKEN: $GITLAB_API_PRIVATE_TOKEN" "your.gitlab.url/api/v3/groups"
        [
            {
                "avatar_url": null,
                "description": "",
                "id": 2,
                "lfs_enabled": true,
                "name": "venice",
                "path": "venice",
                "request_access_enabled": true,
                "visibility_level": 10,
                "web_url": "http://gitlab.rbtcloud.dev/groups/venice"
            }
        ]
4. Create your yaml configuration file similar to the [sample config](./sample.config.yaml),
optionally specifying `visibility` level and a `deploykey_id`:
```
http://some.gitlab.yoursite.com/api/v3/projects:
  pz-idam:
    github: https://github.com/venicegeo/pz-idam
    gitlabgid: 2
  pz-sak:
    github: https://github.com/venicegeo/pz-sak
    gitlabgid: 2
http://another.gitlab.yoursite.com/api/v3/projects:
  bf-ui:
    github: https://github.com/venicegeo/bf-ui
    gitlabgid: 3
  bf-tideprediction:
    github: https://github.com/venicegeo/bf-tideprediction
    gitlabgid: 3
    # visibility is optional and can be 0 for private 10 for internal
    # or 20 for public. In newer versions of gitlab, the api
    # uses strings instead of integers for this value
    visibility: 10
    # The deploy key must exist already in your gitlab
    deploykey_id: 19

```
5. Use `$ ./gh2gl/gh2gl` to mirror your repositories, specifying the path to your configuration file:
```
usage: gh2gl.py [-h] [--apitoken APITOKEN] [--visibility {0,10,20}] config

Mirror github repo(s) in gitlab.

positional arguments:
  config                yaml file containing repo urls

optional arguments:
  -h, --help            show this help message and exit
  --apitoken APITOKEN   gitlab api token
  --visibility {0,10,20}
                        project visibility level 0=private 10=internal
                        20=public
```

## Dependencies
- [requests](http://docs.python-requests.org/en/master/)
- [pyyaml](http://pyyaml.org/)

