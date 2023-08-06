#!/usr/bin/env python3

from cometcli.utils import *
import os
import requests


@daemon_check
def list_queries():
    try:
        print("> Listing queries")
        config = get_comet_config()
        api = config.get('api_url')
        response = requests.get(api+'/query')
        data = response.json()
        print_table(data)
    except Exception as e:
        print(" > Unable to list queries "+str(e))


def execute_query(dataset_name, query):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        payload = {"dataset-name": dataset_name,
                   "query": query}
        response = requests.post(api+'/query', json=payload)
        if response.status_code == 200:
            print('> Executing query')
        else:
            print('> Failed to execute query ' +
                  response.json()['status']['message'])
    except Exception as e:
        print('> Failed to execute query '+str(e))


def export_query_results(query_id, output_file_name):
    try:
        config = get_comet_config()
        api = config.get('api_url')
        response = requests.get(api+'/query/'+str(query_id))
        if response.status_code == 200:
            response_data = response.json()
            if response_data['status']['message'] == 'OK':
                with open('output_file_name', 'w') as output_file:
                    output_file.write(response_data['data'])
            else:
                print('> Query is still being processed')
    except Exception as e:
        print('> Failed to export query results '+str(e))


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
