import configparser, os

config_filepath = 'config.ini'
config = configparser.ConfigParser()

def save_config():
    with open(config_filepath, 'w') as configfile:
        config.write(configfile)

if os.path.exists(config_filepath):
    # Load the config.ini file.
    config.read(config_filepath)
else:
    # Creata a default config.ini file.
    config["UDP"] = {
        "IP": "127.0.0.1",
        "Port": "11111"
    }

    save_config()