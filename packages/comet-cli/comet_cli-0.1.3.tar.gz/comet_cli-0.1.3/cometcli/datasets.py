#!/usr/bin/env python3

from cometcli.utils import *
import os
import requests


@daemon_check
def add_dataset(file_path):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        if os.path.exists(file_path) is not True:
            print('> File not found')
            exit(1)
        file_name = file_path.split('/')[-1]
        with open(file_path, 'r') as data_file:
            content = data_file.read()
        payload = {'name': file_name, 'content': content}
        response = requests.post(api+'/dataset', json=payload)
        if response.status_code == 200:
            print('> File added to comet')
        else:
            print('> Failed to add file to comet')
    except Exception as e:
        print('> Failed to add file to comet : '+str(e))


@daemon_check
def remove_dataset(file_name):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        payload = {'name': file_name}
        response = requests.delete(api+'/dataset', json=payload)
        if response.status_code == 200:
            print('> Deleted file from Comet')
        else:
            print('> Failed to delete file from comet')
    except Exception as e:
        print('> Failed to remove dataset :'+str(e))


@daemon_check
def list_datasets():
    try:
        config = get_comet_config()
        api = config.get('api_url')
        response = requests.get(api+'/dataset')
        data = response.json()['data']
        print_table(data)
    except Exception as e:
        print('> Failed to get files : '+str(e))


@daemon_check
def get_dataset(dataset_name):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        payload = {'name': dataset_name}
        response = requests.post(api+'/dataset/transfer', json=payload)
        if response.status_code == 200:
            print('> Downloading file from remote comet')
        else:
            print('> Unable to get file')
    except Exception as e:
        print('Failed to transfer dataset :'+str(e))


@daemon_check
def configure_dataset(dataset_name):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        print('> Configuring dataset ...')
        transfer = input('    - Transferable (y/n) : ')
        query = input('    - Queryable    (y/n) : ')
        transfer = 1 if transfer.lower() == 'y' else 0
        query = 1 if query.lower() == 'y' else 0
        payload = {"transfer": transfer, "query": query}
        response = requests.post(api+'/dataset/configure', json=payload)
        if respnonse.status_code == 200:
            print('> Dataset configured')
        else:
            print('> Failed to configure dataset')
    except Exception as e:
        print('Failed to configure dataset :'+str(e))


def print_table(data):
    if data:
        print('\n')
        columns = list(data[0].keys())
        column_string = '\t'.join(columns)
        content_string = ''
        for each in data:
            for key, value in each.items():
                content_string += str(value)+'\t'
            content_string += '\n'
        print(column_string+'\n')
        print(content_string)
    else:
        print('> No files added to comet')
