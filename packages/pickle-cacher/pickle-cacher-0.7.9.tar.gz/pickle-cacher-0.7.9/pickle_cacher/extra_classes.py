from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Union
from warnings import warn


class PathWithClear:
    def __init__(self: PathWithClear, path: Union[Path, str]) -> None:
        self._path = Path(path)

    def __eq__(self: PathWithClear, other: Union[Path, str]) -> bool:
        return self._path == Path(other)

    def __repr__(self: PathWithClear) -> str:
        return repr(self._path)

    def __str__(self: PathWithClear) -> str:
        return str(self._path)

    def clear(self: PathWithClear) -> None:  # dead: disable
        warn(f"Clearing {self._path}...")
        rmtree(self._path)


class Cache(Dict[str, Any]):
    def __init__(self: Cache, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._path: Optional[PathWithClear] = None

    @property
    def path(self: Cache) -> Optional[PathWithClear]:
        return self._path

    @path.setter
    def path(self: Cache, path: Union[Path, str]) -> None:
        self._path = PathWithClear(path)


class DotDict(Dict[str, Any]):
    def __dir__(self: DotDict) -> Iterable[str]:
        return self.keys()

    def __getattr__(self: DotDict, key: str) -> Any:
        if key.startswith("_"):
            raise AttributeError(key)
        else:
            return self[key]

    def __setattr__(self: DotDict, key: str, value: Any) -> None:
        self[key] = value
