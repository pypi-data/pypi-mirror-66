#!/usr/bin/env python

from pprint import pprint
from functools import wraps
import os
import json
import requests


def handle_exceptions(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        function_name = f.__name__
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print('Exception | %s | %s |' % (function_name, str(e)))
    return wrapped_function


def get_comet_config():
    config_file_path = os.path.join(os.environ['HOME'], '.comet.config')
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        docker_daemon_uri = 'https://0.0.0.0:9999/api'
        config = {"api_url": docker_daemon_uri}
        with open(config_file_path, 'w') as config_file:
            json.dump(config, config_file)
    return config


def daemon_ping():
    config = get_comet_config()
    api = config.get('api_url')
    try:
        response = requests.get(api+'/comet/ping')
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


def daemon_check(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if not daemon_ping():
            print('> Unable to connect to daemon')
            exit(1)
        else:
            return f(*args, **kwargs)
    return wrapped_function


@daemon_check
def connect_comet(auth_key):
    config = get_comet_config()
    api = config.get('api_url')
    payload = {"auth-key": auth_key}
    response = requests.post(api+'/comet', json=payload)
    if response.status_code == 200:
        print("> Comet connected successfully")
    else:
        print("> Failed to connect comet")


@daemon_check
def get_comet_status():
    try:
        config = get_comet_config()
        api = config.get('api_url')
        response = requests.get(api+'/comet')
        response_data = response.json().get('data')
        print("\n> Comet info")
        print("    Name         : "+response_data.get('name'))
        print("    Comet Id     : "+response_data.get('comet_id'))
        print("    Version      : "+response_data.get('version'))
        print("    Connected    : "+str(response_data.get('connected')))
        print("    Organization : "+response_data.get('org_id'))
    except Exception as e:
        print("> Failed to get comet status")
