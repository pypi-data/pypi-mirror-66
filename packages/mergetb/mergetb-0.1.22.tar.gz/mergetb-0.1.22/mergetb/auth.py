from os import makedirs, remove, environ
from os.path import expanduser, exists, join
import yaml

from mergetb.cli import request_token_to, MergeApiCliException
from mergetb.lib import set_token, set_api

def login(userid=None, password=None, config_path=None, api='api.mergetb.net'):

    cp = config_path
    if not cp:
        cp = join(expanduser('~'), ".config", "mergetb")

    if not exists(cp):
        makedirs(cp)

    tokenfile = join(cp, "token")

    try:
        request_token_to(tokenfile, userid, password)
    except MergeApiCliException as e:
        print(f'Error logging in: {e}')
        return False

    # read the token and load it into the library.
    try:
        token = ''
        with open(tokenfile) as fd:
            try:
                token = yaml.safe_load(fd)
            except yaml.YAMLError as e:
                print(f'Token parse error: {e}')
                return False

    except OSError as e:
        print(f'Read token error: {e}')
        return False

    set_token(token['token'])
    set_api(api)

    # make sure requests can see our CA cert.
    if not environ.get('REQUESTS_CA_BUNDLE'):
        environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

    return True

def logout(config_path=None):

    cp = config_path
    if not cp:
        cp = join(expanduser('~'), ".config", "mergetb")

    tokenfile = join(cp, "token")
    remove(tokenfile)
