import falcon
from pydocumentdb import document_client
from pydocumentdb import errors
import uuid
import sys
import json
import os

class History:
    def __init__(self):
        try:
            self.COSMOS_HOST = os.environ['COSMOS_HOST']
            self.COSMOS_KEY = os.environ['COSMOS_KEY']
            self.COSMOS_DATABASE = os.environ['COSMOS_DATABASE']
            self.COSMOS_COLLECTION = os.environ['COSMOS_COLLECTION']
        except KeyError as e:
            print('Secret {var} not found. Terminating...'.format(var=e.args[0]))
            sys.exit(255)
        
        self.cosmos = document_client.DocumentClient(
            self.COSMOS_HOST, {'masterKey': self.COSMOS_KEY})

        # YOU HAD ONE JOB, SDK TEAM
        self.database_link = 'dbs/' + self.COSMOS_DATABASE
        self.collection_link = self.database_link + '/colls/' + self.COSMOS_COLLECTION

    def on_get(self, req, resp):
        query_str = 'SELECT c.id, c.probability FROM c'
        query_result = self.cosmos.QueryDocuments(self.collection_link, query_str)
        docs = json.dumps(list(query_result))
        resp.status = falcon.HTTP_200
        resp.body = docs