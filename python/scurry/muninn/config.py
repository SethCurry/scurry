import abc
import os.path
import typing

import scurry.muninn.models as models
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ConfigClass(abc.ABC):
    @abc.abstractmethod
    def validate(self):
        return

    @abc.abstractmethod
    def merge_dict(self, d: typing.Dict[str, typing.Any]):
        pass


class Config(ConfigClass):
    def __init__(self):
        self.database = DatabaseConfig()
        self.spotify = SpotifyConfig()
        return

    def validate(self):
        self.database.validate()

    def merge_dict(self, d: typing.Dict[str, typing.Any]):
        if "database" in d:
            self.database.merge_dict(d["database"])

        if "spotify" in d:
            self.spotify.merge_dict(d["spotify"])


class SpotifyConfig(ConfigClass):
    def __init__(self, client_id: str = "", client_secret: str = "", token: str = ""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def validate(self):
        if self.client_id == "":
            raise Exception("spotify client_id cannot be empty")

        if self.client_secret == "":
            raise Exception("spotify client_secret cannot be empty")

    def merge_dict(self, d: typing.Dict[str, typing.Any]):
        if "client_id" in d:
            self.client_id = d["client_id"]

        if "client_secret" in d:
            self.client_secret = d["client_secret"]

        if "token" in d:
            self.token = d["token"]

        return


class DatabaseConfig(ConfigClass):
    def __init__(self):
        self.host = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.Session = None
        return

    def validate(self):
        if self.host == "":
            raise Exception("host cannot be empty")

        if self.database == "":
            raise Exception("database cannot be empty")

        if self.user == "":
            raise Exception("user cannot be empty")

        if self.password == "":
            raise Exception("password cannot be empty")

        return

    def merge_dict(self, d: typing.Dict[str, typing.Any]):
        if "host" in d:
            self.host = d["host"]

        if "database" in d:
            self.database = d["database"]

        if "user" in d:
            self.user = d["user"]

        if "password" in d:
            self.password = d["password"]

    def create(self):
        connection = self.connect()

        models.Base.metadata.create_all(connection)

        return connection

    def connect(self):
        engine = create_engine(
            "postgres://%s:%s@%s/%s"
            % (self.user, self.password, self.host, self.database)
        )

        self.Session = sessionmaker(bind=engine)

        return engine


def load(path: str = "") -> Config:
    with open(path) as fd:
        contents = fd.read()
    loaded = yaml.safe_load(contents)

    conf = Config()
    conf.merge_dict(loaded)
    return conf


def load_default():
    config_path = os.path.expanduser("~/.config/muninn/config.yml")
    return load(config_path)
