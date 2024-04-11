import configparser, os

from src.config_default import default_dict

config_filepath = default_dict['Application']["name"] + '.ini'
config = configparser.ConfigParser()

def default_config():
    for section in default_dict.keys():
        if not section in config:
            config.add_section(section)
        for key, value in default_dict[section].items():
            if not key in config[section]:
                config[section][key] = str(value)

def save_config():
    with open(config_filepath, 'w') as configfile:
        config.write(configfile)

def validate_config():
    if not "Application" in config:
        return False
    if not ("name" in config["Application"]) or not ("config_version" in config["Application"]):
        return False
    if  ( ( str(default_dict["Application"]["name"]) == str(config["Application"].get("name")) ) and
          ( str(default_dict["Application"]["config_version"]) == str(config["Application"].get("config_version"))) ) :
        return True
    else:
        return False

if os.path.exists(config_filepath):
    # Load the config.ini file.
    config.read(config_filepath)
    if not validate_config():
        config = configparser.ConfigParser()
        default_config()
else:
    default_config()