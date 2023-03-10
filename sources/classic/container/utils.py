import inspect
from types import ModuleType
from typing import Any, Sequence, Tuple, Optional, Type

from .types import Factory, Target


def _is_submodule(submodule: ModuleType, module: ModuleType) -> bool:
    return submodule.__name__.startswith(module.__name__)


def get_members(module: ModuleType) -> Tuple[Sequence[Target],
                                             Sequence[ModuleType]]:
    submodules = []
    targets = []

    for name, member in module.__dict__.items():
        if name.startswith('_'):
            continue
        if isinstance(member, ModuleType) and _is_submodule(member, module):
            submodules.append(member)
        elif inspect.isclass(member):
            targets.append(member)

    return targets, submodules


def get_interfaces_for_cls(target: Type):
    for cls in target.__mro__:
        if cls != object:
            yield cls


def get_factory_result(factory: Factory) -> Optional[Type]:
    if inspect.isclass(factory):
        return factory

    signature = inspect.signature(factory)
    result = signature.return_annotation
    if result == inspect.Parameter.empty:
        return None

    return result


def is_factory(obj: Any) -> bool:
    return inspect.isclass(obj) or inspect.isfunction(obj)
