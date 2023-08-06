from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path
from typing import List

import beholder.const as const

_CFG_HELP = "Path to the config file containing website addresses."
_T_HELP = "Number of seconds between subsequent checks."
_O_HELP = "File where the session should be dumped."
_D_HELP = "Display not only if something changes but also what changes."


def path(x: str) -> Path:
    return Path(x)


def parse(args: List[str]) -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("config_path", type=path, help=_CFG_HELP)
    parser.add_argument("-t", "--time", type=int, default=const.DEFAULT_T, help=_T_HELP,
                        required=False)
    parser.add_argument("-o", "--output_path", type=path, help=_O_HELP, required=False)
    parser.add_argument("-d", "--show_diffs", action='store_true', default=const.DEFAULT_D,
                        help=_D_HELP, required=False)
    return parser.parse_args(args)
