""" Find missing entity_id's from automations in Home Assistant"""
import os
import sys
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from requests import get

try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError
import requests


def findkeys(node, key_value):
    """Find a key in a dict or list"""
    if isinstance(node, list):
        for i in node:
            for item in findkeys(i, key_value):
                yield item
    elif isinstance(node, dict):
        if key_value in node:
            if isinstance(node[key_value], list):
                for i in node[key_value]:
                    yield i
            else:
                yield node[key_value]
        for j in node.values():
            for item in findkeys(j, key_value):
                yield item


def find_missing_entities(filename, entities):
    """Find the missing entities from a single file"""
    yaml_file = open(filename)
    try:
        data = yaml.load(yaml_file, Loader=Loader)
    except yaml.YAMLError:
        print("Failed to load: " + filename)
        return

    automation_entities = set(findkeys(data, "entity_id"))

    set_entities = set(entities)
    missing_entities = automation_entities.difference(set_entities)
    missing_entities = {e for e in missing_entities if '{' not in e}

    print(filename)
    if len(missing_entities) > 0:
        print(missing_entities)
    else:
        print("Nothing missing")


url = os.environ.get("HASS_SERVER")
if url is None:
    print("HASS_SERVER environmental variable needs to be set")
url = url + "/api/states"

token = os.environ.get("HASS_TOKEN")
if token is None:
    print("HASS_TOKEN environmental variable needs to be set")

headers = {
    "Authorization": "Bearer " + token,
    "content-type": "application/json",
}

try:
    response = get(url, headers=headers)
except requests.exceptions.RequestException:  # This is the correct syntax
    raise SystemExit()

try:
    json = response.json()
except JSONDecodeError:
    print("Error with JSON decoding. Check your URL for you server.")
    sys.exit()

entities_list = []
for e in json:
    entities_list.append(e["entity_id"])

with os.scandir(".") as files:
    for file in files:
        if file.name.endswith(".yaml"):
            find_missing_entities(file.name, entities_list)
