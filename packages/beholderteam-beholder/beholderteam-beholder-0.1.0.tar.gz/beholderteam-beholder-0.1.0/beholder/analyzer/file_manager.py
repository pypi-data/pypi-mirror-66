from pathlib import Path
from tempfile import mkdtemp
from typing import List


class FileManager:
    __slots__ = ('_temp_dir', '_lut')

    _temp_dir: Path
    _lut: dict

    def __init__(self, sites: List[str]):
        self._temp_dir = Path(mkdtemp())
        self._lut = {v: str(i) for i, v in enumerate(sites)}

    def latest_path(self, addr: str) -> Path:
        return self._temp_dir / (self._lut[addr] + "o.html")

    def chall_path(self, addr: str) -> Path:
        return self._temp_dir / (self._lut[addr] + "n.html")
