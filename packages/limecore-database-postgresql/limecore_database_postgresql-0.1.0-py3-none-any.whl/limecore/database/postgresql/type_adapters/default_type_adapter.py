from .base_type_adapter import BaseTypeAdapter


class DefaultTypeAdapter(BaseTypeAdapter):
    @property
    def db_types(self):
        return [object]

    @property
    def domain_types(self):
        return [object]

    def from_db_type(self, value: object):
        return value

    def to_db_type(self, value: object):
        return value
