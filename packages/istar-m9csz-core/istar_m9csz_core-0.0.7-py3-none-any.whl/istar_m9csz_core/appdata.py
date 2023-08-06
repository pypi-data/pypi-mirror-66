import os
import json

rootdir = os.path.dirname(os.path.abspath(__file__))

config = json.load(open(os.path.join(rootdir, 'appdata', 'config.json')))
data_format = json.load(open(os.path.join(rootdir, config['paths']['data_format'])))
