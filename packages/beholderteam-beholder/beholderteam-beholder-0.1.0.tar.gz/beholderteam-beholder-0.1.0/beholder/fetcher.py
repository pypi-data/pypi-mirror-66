from pathlib import Path

import requests

import beholder.const as const
from beholder.errors import IncorrectStatusError


class WebFetcher:
    __slots__ = ()

    def fetch(self, addr: str, path: Path) -> None:
        res = requests.get(addr)
        if res.status_code not in const.ALLOWED_STATCODES:
            raise IncorrectStatusError(addr, res.status_code)
        path.write_text(res.text, encoding='utf-8')
