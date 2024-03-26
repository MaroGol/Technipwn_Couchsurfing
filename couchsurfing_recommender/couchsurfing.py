import hmac
import hashlib
import json
import re
import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib.parse
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import sys


def read_config():
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    return config_data


def set_config(config_key, config_value):
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    config_data[config_key] = config_value
    with open('config.json', 'w') as f:
        json.dump(config_data, f, indent=4)
    return


def sign_request(url, type="normal"):
    parsed_url = urllib.parse.urlparse(url)
    
    if type == "login":
        secret_key = read_config()['secret_key'].encode('utf-8')
        path = parsed_url.path
    
    else:
        secret_key = f"{read_config()['secret_key']}.{read_config()['user_id']}".encode('utf-8')
        path = f'{parsed_url.path}?{parsed_url.query}'
    
    message = path.encode('utf-8')    
    hash_obj = hmac.new(secret_key, message, hashlib.sha1)
    hex_digest = hash_obj.hexdigest()

    return hex_digest


def make_request(api_path):
    auth_token = read_config()['auth_token']
    user_id = read_config()['user_id']

    if (auth_token == None or auth_token == "" or user_id == None or user_id == ""):
        print('[!] No auth token/user id in config file. Need to log in....')
        email = input('Couchsurfing email: ')
        password = input('Couchsurfing password: ')
        get_auth_token(email, password)
        auth_token = read_config()['auth_token']
        
    url = 'https://hapi.couchsurfing.com' + api_path
    
    url = urllib.parse.quote(url, safe=':/?=&')
    signature = sign_request(url)

    headers = {
        'Host': 'hapi.couchsurfing.com',
        'X-Access-Token': auth_token,
        'X-Cs-Url-Signature': signature,
        'User-Agent': read_config()['user_agent'] # https://user-agents.net/devices/mobiles
    }

    proxies = {
        'http': read_config()['proxy'],
        'https': read_config()['proxy']
    }

    if (read_config()['proxy_status'] == True):
        response = requests.get(url, headers=headers, verify=False, proxies=proxies)
    
    else:
        response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code != 200:
        print('[!] Request error')
    
    return response.content


def get_auth_token(email, password):
    api_path = '/api/v4.1/sessions'
    url = 'https://hapi.couchsurfing.com' + api_path
    
    url = urllib.parse.quote(url, safe=':/?=&')
    signature = sign_request(url, "login")

    headers = {
        'Host': 'hapi.couchsurfing.com',
        'X-Cs-Url-Signature': signature,
        'User-Agent': read_config()['user_agent'] # https://user-agents.net/devices/mobiles
    }

    post_data = {
        "actionType" : "manual_login",
        "credentials" : {
            "email" : email,
            "authToken" : password
        }
    }

    proxies = {
        'http': read_config()['proxy'],
        'https': read_config()['proxy']
    }

    if (read_config()['proxy_status'] == True):
        response = requests.post(url, headers=headers, json=post_data, verify=False, proxies=proxies)

    else:
        response = requests.post(url, headers=headers, json=post_data, verify=False)

    if response.status_code != 200:
        print('Login error')
        sys.exit()

    else:
        print('Successful login! Updating config file.')
        print('Continuing program...')
        jdata = json.loads(response.content)
        user_id = jdata['sessionUser']['id']
        auth_token = jdata['sessionUser']['accessToken']
        set_config('user_id', user_id)
        set_config('auth_token', auth_token)
        return auth_token


def get_user_id(username):
    url = f'https://www.couchsurfing.com/people/{username}'

    response = requests.get(url, verify=False)

    extract_username_pattern = r'https:\/\/s3\.amazonaws\.com\/ht-images\.couchsurfing\.com\/u\/(.*?)\/'
    ids = re.findall(extract_username_pattern, response.content.decode('utf-8'))

    if (len(ids) == 0):
        print(f'Could not find id for user {username}')
        sys.exit()
    
    return ids[0]


def get_profile_data(user_id):
    api_path = f'/api/v4/users/{user_id}?includeMapExperience=true'
    data = make_request(api_path)
    jdata = json.loads(data)

    return jdata