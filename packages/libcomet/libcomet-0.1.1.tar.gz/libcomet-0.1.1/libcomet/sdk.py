#!/usr/bin/env python3

import requests


class Comet:
    def __init__(self, host):
        self.host = host
        self.name = None
        self.id = None
        self.version = None
        self.connected = 0
        self.organization_id = None
        self.orgnaization_name = None

    def ping(self):
        response = requests.get(self.host+'/api/comet/ping')
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def connect(self, auth_key):
        payload = {"auth-key": auth_key}
        response = requests.post(self.host+'/api/comet', json=payload)
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def configure(self):
        raise NotImplementedError

    def get_status(self):
        response = requests.get(self.host+'/api/comet')
        if response.status_code == 200:
            status = response.json().get('data')
            output = status
        else:
            output = False
        return output

    def get_datasets(self):
        response = requests.get(self.host+'/api/dataset')
        if response.status_code == 200:
            datasets = response.json().get('data')
            output = datasets
        else:
            output = False
        return output

    def add_dataset(self, dataset_name, file_ptr):
        with open(file_ptr, 'r') as source_file:
            content = source_file.read()
        payload = {"name": dataset_name, "content": content}
        response = requests.post(self.host+'/api/dataset', json=payload)
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def remove_dataset(self, dataset_name):
        payload = {"name": dataset_name}
        response = requests.delete(self.host+'/api/dataset', json=payload)
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def configure_dataset(self, transfer=0, query=0):
        payload = {"transfer": transfer, "query": query}
        response = requests.post(
            self.host+'/api/dataset/configure', json=payload)
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def download_dataset(self, dataset_name):
        payload = {"name": dataset_name}
        response = requests.post(
            self.host+'/api/dataset/transfer', json=payload)
        if response.status_code == 200:
            output = True
        else:
            output = False
        return output

    def run_query(self, dataset_name, query):
        payload = {"dataset-name": dataset_name, "query": query}
        response = requests.post(self.host+'/api/query', json=payload)
        if response.status_code == 200:
            output = response.json()
        else:
            output = False
        return output

    def get_query_result(self, query_id):
        response = requests.get(self.host + '/api/query/'+str(query_id))
        if response.status_code == 200:
            output = response.json()
        else:
            output = False
        return output
