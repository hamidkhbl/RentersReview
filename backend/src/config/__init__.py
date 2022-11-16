import json
def get_config(config):
    config_file = open('config/config.json')
    json_ = json.loads(config_file.read())
    return json_[config]