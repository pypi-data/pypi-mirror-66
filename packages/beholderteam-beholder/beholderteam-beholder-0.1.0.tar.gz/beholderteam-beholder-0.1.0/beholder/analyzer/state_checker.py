import time
from argparse import Namespace
from typing import List, Optional

import beholder.reports.report_builder as report_builder
from beholder.analyzer.file_manager import FileManager
from beholder.fetcher import WebFetcher
from beholder.file_comparator.comparators import FileComparator
from beholder.reports.reporter_factory import ReporterFactory
from beholder.reports.reporters import Reporter


class StateChecker:
    comparator: FileComparator
    fetcher: WebFetcher
    sites: List[str]
    time: int
    reporter: Reporter
    file_manager: FileManager
    show_diffs: bool = False
    output_path: Optional[str] = None

    def __init__(self, sites: List[str], opts: Namespace):
        self.sites = sites
        self.time = opts.time
        self.comparator = FileComparator()
        self.reporter = ReporterFactory.create(opts.output_path)
        self.file_manager = FileManager(sites)
        self.fetcher = WebFetcher()
        self.output_path = opts.output_path
        self.show_diffs = opts.show_diffs

    def run(self) -> None:
        self._download_websites()
        while 1:
            for site in self.sites:
                self._check_site(site)
            time.sleep(self.time)

    def _download_websites(self) -> None:
        for site in self.sites:
            path = self.file_manager.latest_path(site)
            self.fetcher.fetch(site, path)

    def _check_site(self, site: str) -> None:
        latest_path = self.file_manager.latest_path(site)
        chall_path = self.file_manager.chall_path(site)
        self.fetcher.fetch(site, chall_path)
        res = self.comparator.compare(latest_path, chall_path)
        if res.diffs:
            report = report_builder.build(site, res, with_diffs=self.show_diffs)
            self.reporter.report(site, report)
            latest_path.write_text(chall_path.read_text())
