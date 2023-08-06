from uuid import UUID

from .base_type_adapter import BaseTypeAdapter


class UUIDTypeAdapter(BaseTypeAdapter):
    @property
    def db_types(self):
        return []

    @property
    def domain_types(self):
        return [UUID]

    def from_db_type(self, value: str):
        return UUID(value)

    def to_db_type(self, value: UUID):
        return str(value)
