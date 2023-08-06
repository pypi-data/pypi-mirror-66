import abc
from datetime import datetime
from pathlib import Path


class Reporter(abc.ABC):
    @abc.abstractmethod
    def report(self, site: str, report: str) -> str:
        pass


class BaseReporter(Reporter):
    def report(self, site: str, report: str) -> str:
        now = datetime.now()
        return f"{now} - {site} - {report}"


class StdoutReporter(Reporter):
    reporter: Reporter

    def __init__(self, reporter: Reporter):
        self.reporter = reporter

    def report(self, site: str, report: str) -> str:
        report = self.reporter.report(site, report)
        print(report)
        return report


class FileReporter(Reporter):
    reporter: Reporter
    file: Path

    def __init__(self, reporter: Reporter, path: Path):
        self.reporter = reporter
        self.path = path

    def report(self, site: str, report: str) -> str:
        report = self.reporter.report(site, report)
        with self.path.open(mode='a') as fd:
            fd.write(report)
        return report
