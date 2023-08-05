from pathlib import Path
from typing import Any, Optional
from yaml import safe_load

from .configuration import Configuration


class YAMLFile(Configuration):
    def __init__(self, data: Any):
        self._data = data

    @classmethod
    def load(cls, path: Path) -> "YAMLFile":
        with open(path) as f:
            return cls(safe_load(f))

    def get_int(self, name: str) -> Optional[int]:
        if name not in self._data:
            return None

        return int(self._data[name])

    def get_string(self, name: str) -> Optional[str]:
        if name not in self._data:
            return None

        return str(self._data[name])

    def section(self, *names: str) -> Optional["Configuration"]:
        data = self._data

        for name in names:
            if name not in data:
                return None

            data = data[name]

        return YAMLFile(data)
