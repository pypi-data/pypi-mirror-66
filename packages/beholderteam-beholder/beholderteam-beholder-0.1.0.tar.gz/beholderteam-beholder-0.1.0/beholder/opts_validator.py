from argparse import Namespace

import beholder.const as const


def validate_opts(opts: Namespace) -> None:
    _validate_time(opts)
    _validate_out_path(opts)
    _validate_cfg_path(opts)


def _validate_time(opts: Namespace) -> None:
    if opts.time < const.T_MIN:
        raise ValueError(f"Checking interval must be at least {const.T_MIN} sec.")


def _validate_out_path(opts: Namespace) -> None:
    out_path = opts.output_path
    if out_path and out_path.is_file():
        raise FileExistsError(f"File {out_path.resolve()} exists. It would be overwritten.")


def _validate_cfg_path(opts: Namespace) -> None:
    cfg_path = opts.config_path.resolve()
    if not cfg_path.is_file():
        raise FileNotFoundError(f"{cfg_path} does not exist or is not a file.")
