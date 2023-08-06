from typing import Dict, Type

from .type_adapters import BaseTypeAdapter


class TypeAdapter:
    class _ListAdapter(BaseTypeAdapter):
        def __init__(self, type_adapter: "TypeAdapter"):
            self._type_adapter = type_adapter

        def to_db_type(self, values):
            return self._type_adapter.to_db_types(values)

    def __init__(
        self,
        default_type_adapter: BaseTypeAdapter,
        type_adapters: Dict[Type, Type[BaseTypeAdapter]],
    ):
        self._default_type_adapter = default_type_adapter
        self._list_adapter = TypeAdapter._ListAdapter(self)
        self._type_adapters = type_adapters

    def to_db_types(self, values):
        return [self._get(type(v)).to_db_type(v) for v in values]

    def _get(self, t: Type) -> BaseTypeAdapter():
        if t == list:
            return self._list_adapter
        else:
            return self._type_adapters.get(t) or self._default_type_adapter
