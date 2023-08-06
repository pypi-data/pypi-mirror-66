from injector import Module as _Module, multiprovider, provider, singleton
from limecore.core.configuration import Configuration
from limecore.database.api import Database
from limecore.logging import LoggerFactory
from typing import Dict, List, Type

from .configuration import Configuration as DatabaseConfiguration
from .database import Database as PostgreSQLDatabase
from .type_adapter import TypeAdapter
from .type_adapters import BaseTypeAdapter, DefaultTypeAdapter, UUIDTypeAdapter


class Module(_Module):
    @singleton
    @provider
    def provide_configuration(
        self, configuration: Configuration, type_adapter: TypeAdapter
    ) -> DatabaseConfiguration:
        database_configuration = configuration.section(
            "limecore", "database", "postgresql"
        )

        return DatabaseConfiguration(
            database=database_configuration.get_string("database")
            or database_configuration.get_string("user")
            or "postgres",
            host=database_configuration.get_string("host") or "localhost",
            password=database_configuration.get_string("password") or "postgres",
            port=database_configuration.get_int("port") or 5432,
            type_adapter=type_adapter,
            user=database_configuration.get_string("user") or "postgres",
        )

    @singleton
    @provider
    def provide_database(
        self, configuration: DatabaseConfiguration, logger_factory: LoggerFactory
    ) -> Database:
        return PostgreSQLDatabase(configuration, logger_factory)

    @singleton
    @provider
    def provide_type_adapter(
        self,
        custom_type_adapters: List[BaseTypeAdapter],
        default_type_adapter: DefaultTypeAdapter,
    ) -> TypeAdapter:
        type_adapters: Dict[Type, Type[BaseTypeAdapter]] = {}

        for type_adapter in custom_type_adapters:
            for t in type_adapter.domain_types:
                type_adapters[t] = type_adapter

        return TypeAdapter(default_type_adapter, type_adapters)

    @singleton
    @multiprovider
    def provide_type_adapters(self) -> List[BaseTypeAdapter]:
        return [UUIDTypeAdapter()]
