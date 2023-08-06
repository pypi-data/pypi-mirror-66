from datetime import datetime

from beholder.file_comparator.comparators import ComparisonResult


def build(site: str, comparison_result: ComparisonResult, with_diffs: bool = False) -> str:
    now = datetime.now()
    diffs = comparison_result.diffs
    if not diffs:
        return ""
    status = "Website has changed.\n"
    if with_diffs:
        status += "\n".join(diffs)
    return f"{now} - {site} - {status}"
