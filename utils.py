import os

from storage.bedrock_provider import BedrockProvider
from storage.s3_provider import S3Provider
from storage.fs_provider import FSProvider

def create_provider(pr_type, pr_info):
    if pr_type == 'FS':
        return FSProvider(pr_info['dir'])
    elif pr_type == 'Bedrock':
        return pr_info['ips']
    elif pr_type == 'S3':
        return S3Provider(pr_info['creds'], pr_info['bucket'])
    else:
        print('Unknown provider type: ' + pr_type + '.')
        return None

# NOTE: This is necessary because we cannot serialize and pickle the
# BedrockProvider class. That's because we are maintaining an open connection
# via a ZMQ context, which can't be serialized.
def get_provider(p_obj):
    if isinstance(p_obj, FSProvider) or isinstance(p_obj, S3Provider):
        return p_obj
    elif isinstance(p_obj, list):
        return BedrockProvider(p_obj)

def read_creds(path=None):
    if path == None:
        home = os.path.expanduser('~')
        path = home + '/.aws/credentials'

    creds = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        creds['access_key_id'] = lines[1].split('=')[-1].strip()
        creds['secret_access_key'] = lines[2].split('=')[-1].strip()

    return creds
