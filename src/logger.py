import logging, sys
import pathlib
from src.config import config

LOG_FILENAME = config["Application"]["name"] + ".log"

# Probably want to look at running Tee and grabbing output for logging C wrapped modules.
# https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file

class LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg):
        if msg.endswith('\n'):
            self.buf.append(msg.removesuffix('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self):
        pass

# https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
# https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python#4675744
if config['Application'].getboolean('debug_log'):
    path_file = pathlib.Path(LOG_FILENAME)
    if path_file.is_file():
        path_file.unlink()
    logging.basicConfig(filename=LOG_FILENAME,
                        filemode='a', 
                        format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        level=logging.INFO)
    """
    # consider this: https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file/14058475#14058475
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.__stdout__)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    """
    
    root = logging.getLogger()
    sys.stdout = LoggerWriter(root.info)
    sys.stderr = LoggerWriter(root.error)

    print(config["Application"].get('name'))
    print("Error logging is on.")