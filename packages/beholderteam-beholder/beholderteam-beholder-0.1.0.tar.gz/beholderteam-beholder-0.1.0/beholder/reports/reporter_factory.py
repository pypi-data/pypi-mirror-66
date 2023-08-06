from pathlib import Path
from typing import Optional

from beholder.reports.reporters import BaseReporter, StdoutReporter, FileReporter, Reporter


class ReporterFactory:
    @staticmethod
    def create(output_path: Optional[Path] = None):
        reporter: Reporter = StdoutReporter(BaseReporter())
        if output_path:
            reporter = FileReporter(reporter, output_path)
        return reporter
