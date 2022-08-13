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


def load_entities():
    json = load_from_url("/states")

    entities_list = []
    for e in json:
        entities_list.append(e["entity_id"])

    return entities_list


def load_services():
    json = load_from_url("/services")
    services_list = []

    for domain in json:
        for service in domain["services"]:
            services_list.append(domain["domain"] + "." + service)
    return services_list


def load_from_url(append_url):
    full_url = url + append_url
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }
    try:
        response = get(full_url, headers=headers)
    except requests.exceptions.RequestException:  # This is the correct syntax
        raise SystemExit()

    try:
        json = response.json()
    except JSONDecodeError:
        print("Error with JSON decoding. Check your URL for you server.")
        sys.exit()

    return json


def find_missing(filename):
    """Load the file data"""
    yaml_file = open(filename)
    try:
        data = yaml.load(yaml_file, Loader=Loader)
    except yaml.YAMLError:
        print("Failed to load: " + filename)
        return

    automation_entities = set(findkeys(data, "entity_id"))
    find_missing_entities(automation_entities, filename)
    automation_services = set(findkeys(data, "service"))
    find_missing_services(automation_services, filename)


def find_missing_entities(automation_entities, filename):
    """Find the missing entities"""
    global entites
    set_entities = set(entities)
    missing_entities = automation_entities.difference(set_entities)
    missing_entities = {e for e in missing_entities if "{" not in e}

    global error_count
    if len(missing_entities) > 0:
        print(filename + " - Missing entities")
        print(missing_entities)
        error_count = error_count + 1
    else:
        if verbose is True:
            print(filename + " - No missing entities")


def find_missing_services(automation_services, filename):

    global services
    set_services = set(services)
    missing_services = automation_services.difference(set_services)
    missing_services = {e for e in missing_services if "{" not in e}

    global error_count

    if len(missing_services) > 0:
        print(filename + " - Missing Services")
        print(missing_services)
        error_count = error_count + 1
    else:
        if verbose is True:
            print(filename + " - Not missing services")

url = os.environ.get("HASS_SERVER")
if url is None:
    print("HASS_SERVER environmental variable needs to be set")
url = url + "/api"
verbose = False

token = os.environ.get("HASS_TOKEN")
if token is None:
    print("HASS_TOKEN environmental variable needs to be set")

error_count = 0

entities = load_entities()
services = load_services()

with os.scandir(".") as files:
    for file in files:
        if file.name.endswith(".yaml"):
            find_missing(file.name)

sys.exit(error_count)
