import difflib
import filecmp
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ComparisonResult:
    diffs: List[str]


class FileComparator:
    def compare(self, file1: Path, file2: Path) -> ComparisonResult:
        equal = filecmp.cmp(str(file1), str(file2))
        if equal:
            return ComparisonResult([])
        content1 = file1.read_text().split("\n")
        content2 = file2.read_text().split("\n")
        diffs = difflib.unified_diff(content1, content2)
        return ComparisonResult([*diffs])
