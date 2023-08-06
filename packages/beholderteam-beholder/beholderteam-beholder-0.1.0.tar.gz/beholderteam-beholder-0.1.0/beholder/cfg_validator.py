from typing import List

from beholder.errors import IncorrectWebsitesError


def validate_websites(sites: List[str]) -> None:
    inc_sites = _find_incorrect_websites(sites)
    if inc_sites:
        raise IncorrectWebsitesError(inc_sites)


def _find_incorrect_websites(sites: List[str]) -> List[str]:
    return [site for site in sites if not _protocol_correct(site)]


def _protocol_correct(addr: str) -> bool:
    return addr.startswith("https://") or addr.startswith("http://")
