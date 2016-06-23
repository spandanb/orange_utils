"""
Contains various methods for IO
"""
import yaml
import pprint
import json
import os

def read_yaml(filepath=""):
    """
    reads topology file at `filepath` and
    returns corresponding object
    """

    with open(filepath, 'r') as stream:
        try:
            template = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    
    if template is None:
        template = {}
    return template

def write_yaml(data, filepath=""):
    """
    Writes obj in YAML format at filename
    """
    with open(filepath, 'w') as filedesc:
        filedesc.write(yaml.dump(data))

def pretty_print(obj):
    """
    pretty prints an object
    """
    pprint.pprint(obj)
    #print json.dumps(obj, sort_keys=True, indent=4)

def log(text, width=80):
    """
    Prints to stdout
    """
    count = width - len(text) - 1
    print "{} {}\n".format(text, '*'*count)
   
def yaml_to_envvars(yamlfile):
    """
    Reads a YAML file and stores variables as env vars.
    NOTE: The YAML should consist of one flat dictionary.
    """
    conf = read_yaml(yamlfile)
    for param, value in conf.items():
        os.environ[param] = str(value)

