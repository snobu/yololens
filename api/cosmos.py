from pydocumentdb import document_client
from pydocumentdb import errors
import uuid
import sys
import json
import os

COSMOS_HOST = os.environ['COSMOS_HOST']
COSMOS_KEY = os.environ['COSMOS_KEY']
COSMOS_DATABASE = os.environ['COSMOS_DATABASE']
COSMOS_COLLECTION = os.environ['COSMOS_COLLECTION']

print(COSMOS_HOST, COSMOS_KEY, COSMOS_DATABASE, COSMOS_COLLECTION)