import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.config import config

class ConfigVar:
    def __init__(self, config_type, config_path, fallback=""):
        self.type = config_type
        self.path = config_path
        self.fallback = fallback
        self.tk_var = None
        self.init_type()
        # sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
        self.tk_var.trace("w", self.on_changed)

    def exists_or_create(self):
        section = self.path[0]
        key = self.path[1]
        if not section in config:
            config.add_section(section)
        if not key in config[section]:
            config[section][key] = (self.fallback or "")

    def on_changed(self, var, index, mode):
        new_val = str(self.tk_var.get())
        if new_val == "":
            new_val = self.fallback
        config[self.path[0]][self.path[1]] = new_val

    def get(self):
        if (self.type == str):
            return config[self.path[0]].get(self.path[1], fallback="")
        elif (self.type == int):
            return config[self.path[0]].getint(self.path[1], fallback=0)
        elif (self.type == bool):
            return config[self.path[0]].getboolean(self.path[1], fallback=False)
        elif (self.type == float):
            return config[self.path[0]].getfloat(self.path[1], fallback=0)
        else:
            return config[self.path[0]].get(self.path[1])

    def init_type(self):
        if (self.type == str):
            self.tk_var = ttk.StringVar(value=self.get())
        elif (self.type == int):
            self.tk_var = ttk.IntVar(value=self.get())
        elif(self.type == bool):
            self.tk_var = ttk.BooleanVar(value=self.get())
        elif(self.type == float):
            self.tk_var = ttk.DoubleVar(value=self.get())
        else:
            self.tk_var = ttk.StringVar(value=self.get())

    # Validators
    def validate_digit(self, P):
        return True if (str.isdigit(P)) else False
    