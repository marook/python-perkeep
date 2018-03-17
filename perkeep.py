#
# Copyright 2018 Markus Peröbner
#
import json
import os
import platform
import ssl
import urllib.request

web_client_config = None

def query(opts):
    web_client_config = get_web_client_config()
    with urlopen(web_client_config['searchRoot'] + 'camli/search/query', data=bytearray(json.dumps(opts), 'utf-8')) as req:
        return json.load(req)

def download(ref):
    return urlopen('/ui/download/{}/blob'.format(ref))

def sign(data):
    '''Signs an dict object.
    '''
    config = get_web_client_config()
    data['camliSigner'] = config['signing']['publicKeyBlobRef']
    clear_text = '{"camliVersion":1,\n' + json.dumps(data, indent='\t')[len('{\n'):]
    with urlopen(config['signing']['signHandler'], data='json={}'.format(clear_text).encode('utf-8'), content_type='application/x-www-form-urlencoded') as req:
        print(req.read().decode('utf-8'))
        return req
    # TODO

def upload(blob, file_name, path='/ui/?camli.mode=uploadhelper'):
    boundary, form = build_multipart_form(blob, file_name)
    with urlopen(path, data=form, content_type='multipart/form-data; boundary={}'.format(boundary)) as req:
        body = json.load(req)
    return body['got'][0]['fileref']

def build_multipart_form(blob, file_name, content_type='application/octet-stream'):
    '''Formats a blob into a multipart form.

    blob shoud have type bytes.

    -----------------------------6930946476218338041418917799
    Content-Disposition: form-data; name="ui-upload-file-helper-form"; filename="hello_world.txt"
    Content-Type: text/plain

    Hello World!

    -----------------------------6930946476218338041418917799--
    '''
    nl = b'\r\n'
    boundary = '-----------------------------6930946476218338041418917799'
    fragments = [
        b'--',
        boundary.encode('ascii'),
        nl,
        b'Content-Disposition: form-data; name="ui-upload-file-helper-form"; filename="',
        file_name.encode('ascii'),
        b'"',
        nl,
        b'Content-Type: ',
        content_type.encode('ascii'),
        nl,
        nl,
        blob,
        nl,
        b'--',
        boundary.encode('ascii'),
        b'--',
    ]
    return boundary, b''.join(fragments)

def get_web_client_config():
    global web_client_config
    if(web_client_config is None):
        with urlopen('/ui/?camli.mode=config') as req:
            web_client_config = json.load(req)
    return web_client_config

def urlopen(path, data=None, content_type=None):
    server_config = get_default_server_config()
    request = urllib.request.Request(server_config['server'] + path, data=data)
    if(not content_type is None):
        request.add_header('Content-Type', content_type)
    return get_default_perkeep_opener().open(request)

perkeep_opener = None

def get_default_perkeep_opener():
    global perkeep_opener
    if(perkeep_opener is None):
        server_config = get_default_server_config()
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        https_handler = urllib.request.HTTPSHandler(debuglevel=0, check_hostname=False, context=ssl_ctx)
        auth_method, user, password = server_config['auth'].split(':')
        if(auth_method != 'userpass'):
            raise Exception('Unknown auth_method {}'.format(auth_method))
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(
            realm='',
            uri=server_config['server'],
            user=user,
            passwd=password)
        perkeep_opener = urllib.request.build_opener(https_handler)
        perkeep_opener.add_handler(auth_handler)
    return perkeep_opener

def get_default_server_config():
    config = get_client_config()
    for server in config['servers'].values():
        if(not server['default']):
            continue
        return server
    raise Exception('No default server found')

client_config_cache = None

def get_client_config():
    global client_config_cache
    if(client_config_cache is None):
        client_config_cache = read_client_config()
    return client_config_cache

def read_client_config():
    config_dir = get_perkeep_config_dir_path()
    with open(os.path.join(config_dir, 'client-config.json'), 'r') as f:
        return json.load(f)

def get_perkeep_config_dir_path():
    if('CAMLI_CONFIG_DIR' in os.environ):
        return os.environ['CAMLI_CONFIG_DIR']
    if(platform.system() == 'Windows'):
        return os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Camlistore')
    return os.path.join(os.path.expanduser('~'), '.config', 'camlistore')
