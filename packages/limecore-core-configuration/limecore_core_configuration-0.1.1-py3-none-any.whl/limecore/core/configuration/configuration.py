from typing import Optional


class Configuration:
    def get_int(self, name: str) -> Optional[int]:
        raise NotImplementedError()

    def get_string(self, name: str) -> Optional[str]:
        raise NotImplementedError()

    def section(self, *names: str) -> Optional["Configuration"]:
        raise NotImplementedError()
