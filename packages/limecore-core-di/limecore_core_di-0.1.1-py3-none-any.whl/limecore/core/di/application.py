from injector import Injector, Module, Scope
from limecore.util import T
from typing import ClassVar, Optional


class Application:
    def __init__(self, injector: Optional[Injector] = None):
        self._injector = injector or Injector()

    def bind(self, impl: T, to: ClassVar[T], scope: Scope):
        self._injector.binder.bind(to, to=impl, scope=scope)

        return self

    def using(self, module: Module):
        self._injector.binder.install(module)

        return self

    def run(self, klass):
        self._injector.get(klass).start()
