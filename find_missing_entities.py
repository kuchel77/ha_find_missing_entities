""" Find missing entity_id's from automations in Home Assistant"""
import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from requests import get

def findkeys(node, kv):
    """ Find a key in a list """
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

def find_missing_entities(filename, config):
    """ Find the missing entities from a single file """
    yaml_file = open(filename)
    try:
        data = load(yaml_file, Loader=Loader)
    except:
        print("failed to load" + filename)
        return

    try:
        automation_entities = set(findkeys(data, 'entity_id'))
    except:
        #failing at the moment with arrays in entity ids:
        return

    set_entities = set(entities_list)
    missing_entities = automation_entities.difference(set_entities)

    print(filename)
    if len(missing_entities) > 0:
        print(missing_entities)
    else:
        print("Nothing missing")

url = "http://192.168.0.245:8123/api/states"
token = ""
headers = {
    "Authorization": "Bearer "+token,
    "content-type": "application/json",
}

response = get(url, headers=headers)
json = response.json()

entities_list = []
for e in json:
    entities_list.append(e["entity_id"])

with os.scandir('.') as entries:
    for entry in entries:
        if entry.name.endswith(".yaml"):
            find_missing_entities(entry.name, entities_list)
