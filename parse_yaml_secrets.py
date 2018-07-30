#!/usr/bin/env python3

# pip3 install pyyaml
import yaml
import os
import base64
import sys

with open("secrets.yml", 'r') as stream:
    try:
        secrets = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

    if sys.argv[1] == 'host':
        print(base64.b64decode(secrets["data"]["host"]).decode())
    if sys.argv[1] == 'key':
        print(base64.b64decode(secrets["data"]["key"]).decode())
    if sys.argv[1] == 'database':
        print(base64.b64decode(secrets["data"]["database"]).decode())
    if sys.argv[1] == 'collection':
        print(base64.b64decode(secrets["data"]["collection"]).decode())
    