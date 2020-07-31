import json
import os

APP_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(APP_ROOT_PATH, 'settings.json'), 'r+') as f:
    settings = json.loads(f.read())

BFX_DETS = settings['BFX']
