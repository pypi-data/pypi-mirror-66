# MergeTB Python Client

This repo contains a python wrapper around the MergeTB OpenAPI.

## Python3 client library for merge

This can be used for building Python based tools that interact with Merge, or for talking to Merge through Python in a Jupyter notebook. There are some special routines that are Jupyter aware that make working a Jupyter environment nicer.

The library is named `mergetb` and is pip installable via `pip3 install mergetb`. It is for the most part a simple wrapper around the MergeTB Open API spec, which is found here: https://gitlab.com/mergetb/engine/-/blob/master/api/portal/openapi.yml

Here is an example of using the library in a python script:

```python
#!/usr/bin/env python3

import mergetb
import json
from os import environ

uid, pid = environ.get('MERGEUSER'), environ.get('MERGEPWD')

if not uid or not pid:
    print('Set MERGEUSER and MERGEPWD before running.')
    exit(1)

if not mergetb.login(uid, pid):
    print('Error logging in.')
    exit(2)

projects = mergetb.list_projects()
print(f'My projects are {projects}')

pid = uid

exps = mergetb.list_experiments(pid)
print(f'My personal experiments are {exps}')

expinfo = mergetb.experiment_info(pid, exps[0])
print(f'Info about the {exps[0]} experiment is {expinfo}')

# This assumes realizations glawler.hi.one exists.
# (and it is glawler is logged in)
hione = mergetb.get_realization('glawler', 'hi', 'one')

# Grab addresses from the experiment model
model = mergetb.pull_experiment('glawler', 'hi', hione['xhash'])
xir = json.loads(model['xir'])

# walk the chain of json XIR to find addresses if they exist.
for node in xir['nodes']:
    if 'endpoints' in node:
        for ep in node['endpoints']:
            if 'props' in ep:
                if 'ip' in ep['props']:
                    if 'addrs' in ep['props']['ip']:
                        name = node['id']
                        addrs = ep['props']['ip']['addrs']
                        print(f'node {name} has addresses {addrs}')

```

## CLI application

NOTE: This package includes a command line utility at `mergetb/mergetb_cli.py` written using the library in `./mergetb`. It should now only be used as a reference. The official command line client for Merge TB is now written in Go and is here: https://gitlab.com/mergetb/cli

To use, you need to first login to the authentication server and get a client token. This token will be stashed in a local file and referenced in subseqeuent calls to the API. 
