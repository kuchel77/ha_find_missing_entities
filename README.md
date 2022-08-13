# Find missing entities 

This is a simple tool designed to be able to find missing (or changed) entities in your automations.

For instance, if a entity is changed (_2 added to the end on a new setup for instance), then the automation can break.

This can help you find these before the automation runs and you get the error message.

This needs two environmental variables set.

HASS_SERVER = "http://hassio:8123" 

Change this to your local server. Make sure not to have a / on the end as this will break it (and HASS-CLI).

HASS_TOKEN = "mytoken"

After logging into your account, you need to create a token that can be used to access your server.

Otherwise, it will parse all of the files in the current directory that end in .yaml and print the results out for you.

## TODO:

Command line parameter for a different directory.
Command line parameter for a single file.

Include this sort of thing in the VS Code extension.

## Example using Drone

``docker build -t findmissing .``

In .drone.yml

``  - name: findmissing
    image: findmissing
    pull: if-not-exists 
    commands:
      - cd automations 
      - python3 find_missing.py``
