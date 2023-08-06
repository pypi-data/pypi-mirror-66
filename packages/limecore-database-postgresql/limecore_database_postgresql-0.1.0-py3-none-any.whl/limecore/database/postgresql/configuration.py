from .type_adapter import TypeAdapter


class Configuration:
    def __init__(
        self,
        database: str,
        host: str,
        password: str,
        port: int,
        type_adapter: TypeAdapter,
        user: str,
    ):
        self._database = database
        self._host = host
        self._password = password
        self._port = port
        self._type_adapter = type_adapter
        self._user = user

    @property
    def database(self):
        return self._database

    @property
    def host(self):
        return self._host

    @property
    def password(self):
        return self._password

    @property
    def port(self):
        return self._port

    @property
    def type_adapter(self):
        return self._type_adapter

    @property
    def user(self):
        return self._user

    @property
    def __dict__(self):
        return {
            "database": self._database,
            "host": self._host,
            "password": self._password,
            "port": self._port,
            "user": self._user,
        }
