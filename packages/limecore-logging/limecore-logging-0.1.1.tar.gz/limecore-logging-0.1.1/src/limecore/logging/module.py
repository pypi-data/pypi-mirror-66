from injector import Module as _Module, provider, singleton
from logging import Logger, getLogger
from typing import Callable


class Module(_Module):
    @singleton
    @provider
    def provider_logger_factory(self) -> Callable[[str], Logger]:
        return getLogger
