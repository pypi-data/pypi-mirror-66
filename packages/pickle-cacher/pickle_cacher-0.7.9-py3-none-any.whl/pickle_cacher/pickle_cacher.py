from __future__ import annotations

import gzip
import pickle  # noqa: S403
from functools import partial
from hashlib import sha512
from inspect import signature
from itertools import chain
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
from pathlib import Path
from sys import stdout
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

from atomic_write_path import atomic_write_path
from wrapt import decorator

from pickle_cacher.extra_classes import Cache  # noqa: S403
from pickle_cacher.extra_classes import DotDict  # noqa: S403


_PICKLE_CACHE = "pickle_cache"
_ATTR_NAME = f"_{_PICKLE_CACHE}"
LOGGER = getLogger(_PICKLE_CACHE)
_HANDLER = StreamHandler(stream=stdout)
_HANDLER.setLevel(DEBUG)
LOGGER.addHandler(_HANDLER)


def _gzip_load(file: Union[str, Path]) -> object:
    with gzip.open(str(file), mode="rb") as file_handle:
        return pickle.loads(file_handle.read())  # noqa: S301


def _gzip_dump(obj: object, file: Union[str, Path]) -> None:
    with gzip.open(file, mode="wb") as file_handle:
        file_handle.write(pickle.dumps(obj))


def cached(
    func: Any = None,
    *,
    disk: Optional[Union[str, Path, Callable[[Any, Any], Optional[Path]]]] = None,
    load: Callable[[Union[str, Path]], Any] = _gzip_load,
    dump: Callable[[Any, Union[str, Path]], None] = _gzip_dump,
) -> Any:
    if func is None:
        return partial(cached, disk=disk, load=load, dump=dump)
    else:

        @decorator
        def wrapper(
            wrapped: Callable[..., Any],
            instance: Any,
            args: Tuple[Any, ...],
            kwargs: Dict[str, Any],
        ) -> Any:
            name = wrapped.__name__

            if instance is None:
                try:
                    cache: Cache = getattr(wrapped, _ATTR_NAME)
                except AttributeError:
                    setattr(wrapped, _ATTR_NAME, Cache())
                    cache = getattr(wrapped, _ATTR_NAME)
            else:
                try:
                    instance_cache = getattr(instance, _ATTR_NAME)
                except AttributeError:
                    setattr(instance, _ATTR_NAME, DotDict())
                    instance_cache = getattr(instance, _ATTR_NAME)
                try:
                    cache = instance_cache[name]
                except KeyError:
                    cache = instance_cache[name] = Cache()

            kwarg_overwrite = kwargs.pop("overwrite", False)
            kwarg_disk = kwargs.pop("disk", True)
            bound_args = signature(wrapped).bind(*args, **kwargs)
            bound_args.apply_defaults()
            key = sha512(bytes(pickle.dumps((bound_args.args, bound_args.kwargs)))).hexdigest()

            def compute_and_cache(desc: str) -> Any:
                value = cache[key] = wrapped(*args, **kwargs)
                LOGGER.debug(
                    "%s and cached: %s -> %s", desc, bound_args, value,
                )
                return value

            if disk is None:
                path_file: Optional[Path] = None
            else:
                if isinstance(disk, str):
                    path_head: Optional[Path] = Path(disk)
                elif isinstance(disk, Path):
                    path_head = disk
                elif callable(disk):
                    path_head = disk(wrapped, instance)
                else:
                    raise TypeError(
                        f"'disk' must be a str, Path, or callable yielding a str or Path; got {type(disk)}",
                    )
                if path_head is None:
                    path_file = None
                else:
                    if instance is None:
                        path_middle = wrapped.__module__.split(".")
                    else:
                        path_middle = chain(
                            instance.__module__.split("."), [type(instance).__name__],
                        )
                    path_dir = path_head.joinpath(*path_middle, name)
                    if cache.path is None:
                        cache.path = path_dir
                    else:
                        if cache.path != path_dir:
                            raise ValueError(
                                f"Cache path ({cache.path}) and current path ({path_dir}) differ",
                            )
                    path_file = path_dir.joinpath(key)

            def persist_to_disk(obj: Any, desc: str) -> Any:
                if path_file is not None and kwarg_disk:
                    with atomic_write_path(path_file, overwrite=kwarg_overwrite) as temp1:
                        dump(obj, temp1)
                    LOGGER.debug(
                        "%s to %s: %s -> %s", desc, path_file, bound_args, obj,
                    )

            if kwarg_overwrite:
                out = compute_and_cache(desc="Re-computed")
                persist_to_disk(obj=out, desc="Re-persisted")
            else:
                try:
                    out = cache[key]
                except KeyError:
                    if path_file is None:
                        out = compute_and_cache(desc="Computed")
                    else:
                        try:
                            out = load(path_file)
                        except FileNotFoundError:
                            out = compute_and_cache(desc="Computed")
                            persist_to_disk(obj=out, desc="Persisted")
                        else:
                            LOGGER.debug(
                                "Retrieved from %s: %s -> %s", path_file, bound_args, out,
                            )
                else:
                    LOGGER.debug(
                        "Retrieved from cache: %s -> %s", bound_args, out,
                    )
            return out

        return wrapper(func)
