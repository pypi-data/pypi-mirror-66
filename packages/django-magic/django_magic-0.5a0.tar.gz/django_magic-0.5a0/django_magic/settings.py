import os
from pathlib import Path

import dj_database_url


class EnvironmentVariableNotFoundError(Exception):
    pass


class SettingsManager:
    def __init__(self, base_dir):
        self.vars = {}
        self.files = []
        self.base_dir = base_dir

    def try_read_env(self, env):
        try:
            return os.environ[env]
        except KeyError:
            return None

    def relative_path(self, path):
        self.files.append(path)
        return str(Path(self.base_dir, path))

    def env(self, env_var, val=None):
        if self.try_read_env(env_var):
            if os.environ[env_var] == "True":
                value = True
            elif os.environ[env_var] == "False":
                value = False
            else:
                value = os.environ[env_var]
            self.vars[env_var] = ["found", value]
            return value
        else:
            if val is None:
                print(f"warning: setting {env_var} is None")
                self.vars[env_var] = ["defaulted", None]
            elif val == "__optional__":
                self.vars[env_var] = ["skipped", None]
                return None
            else:
                self.vars[env_var] = ["defaulted", val]
                return val

    def db(self, env_var, sqlite_path):
        if env_var in os.environ:
            self.vars[env_var] = "found"
            return dj_database_url.parse(os.environ[env_var])
        else:
            sqlite_abs_path = Path(self.base_dir, sqlite_path)
            self.vars[env_var] = ["defaulted", sqlite_abs_path]
            return dj_database_url.parse(f"sqlite:////{sqlite_abs_path}")

