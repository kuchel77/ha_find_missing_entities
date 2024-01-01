""" Find missing entity_id's from automations in Home Assistant"""
from html import entities
import os
import sys
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from requests import get
import requests

try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError

def find_missing(filename):
    """Load the file data"""
    yaml_file = open(filename)
    try:
        data = yaml.load(yaml_file, Loader=Loader)
    except yaml.YAMLError:
        print("Failed to load: " + filename)
        return

    find_mismatches(data, filename)

def find_mismatches(data, filename):
    if data == None:
        return 
    for automation in data:
        if 'action' in automation.keys():
            for action in automation['action']:
                if 'service' in action.keys():
                    service_domain = action['service'].split('.')[0]
                    if 'target' in action.keys():
                        test = action['target']['entity_id']
                        if isinstance(action['target']['entity_id'], list):
                            for entity in action['target']['entity_id']:
                                entityid_domain = entity.split('.')[0]
                                if service_domain != entityid_domain:
                                    print("Error at")
                                    print(filename)
                                    print(action)
                        else:
                            entityid_domain = action['target']['entity_id'].split('.')[0]
                            if service_domain != entityid_domain:
                                print("Error at")
                                print(filename)
                                print(action)


with os.scandir("/Volumes/mark/config/homeassistant/automations") as files:
    for file in files:
        if file.name.endswith(".yaml"):
            find_missing(file.path)


