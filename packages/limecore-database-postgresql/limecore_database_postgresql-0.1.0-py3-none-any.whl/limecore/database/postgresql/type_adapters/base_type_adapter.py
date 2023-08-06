class BaseTypeAdapter:
    @property
    def db_types(self):
        raise NotImplementedError()

    @property
    def domain_types(self):
        raise NotImplementedError()

    def from_db_type(self, value: object):
        raise NotImplementedError()

    def to_db_type(self, value: object):
        raise NotImplementedError()
