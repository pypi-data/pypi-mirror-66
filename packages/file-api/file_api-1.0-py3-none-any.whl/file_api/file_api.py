import requests
import io
import json


class Client(object):
    def __init__(self, token: str, default_namespace: str = None, endpoint: str ="https://av-upload.bmat.com/api/files"):
        self.default_namespace = default_namespace
        self.token = token
        self.endpoint = endpoint
        self.headers = {
            'authorization': "Bearer " + token,
        }

    def put(self, filename: str, data: io.BytesIO, namespace:str = None, metadata: dict = None):
        files = {'file': (filename, data)}
        r = requests.post(self.endpoint, files=files, data=self.__get_params(namespace, metadata), headers=self.headers)
        if r.status_code == 200:
            return r.json()['id']
        else:
            print(r.text)

    def get(self, file_id, namespace=None):
        return requests.get("{endpoint}/{file_id}".format(
            endpoint=self.endpoint,
            file_id=file_id
        ), data=self.__get_params(namespace), headers=self.headers).json()

    def list(self, page=1, page_size=10, namespace=None):
        return requests.get(
            "{endpoint}?page={page}&pageSize={page_size}".format(
                endpoint=self.endpoint,
                page=page,
                page_size=page_size
            ), data=self.__get_params(namespace), headers=self.headers).json()

    def delete(self, file_id, namespace=None):
        r = requests.delete("{endpoint}/{file_id}".format(
            endpoint=self.endpoint,
            file_id=file_id
        ), data=self.__get_params(namespace), headers=self.headers)
        return r.status_code == 200

    def download(self, file_id, namespace=None):
        r = requests.get("{endpoint}/{file_id}/download".format(
            endpoint=self.endpoint,
            file_id=file_id
        ), data=self.__get_params(namespace), headers=self.headers)
        return r.content

    def __get_params(self, namespace=None, metadata=None):
        d = {
            "namespace": namespace or self.default_namespace
        }

        if metadata:
            d["data"] = json.dumps(metadata)

        return d
