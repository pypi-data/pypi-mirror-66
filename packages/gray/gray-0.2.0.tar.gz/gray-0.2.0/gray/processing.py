import logging
from pathlib import Path
from typing import Iterator, Sequence

from configargparse import Namespace

from gray.formatters import FORMATTERS, BaseFormatter, CompositeFormatter


log = logging.getLogger(__name__)


def gen_filepaths(paths: Sequence[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_file() and (path.suffix == ".py"):
            yield path
        elif path.is_dir():
            yield from path.glob("**/*.py")


def process(arguments: Namespace):
    formatter = CompositeFormatter(
        *[FORMATTERS[k](arguments) for k in arguments.formatters],
    )
    for path in gen_filepaths(arguments.paths):
        fade_file(path, formatter)


def fade_file(file_path: Path, formatter: BaseFormatter):
    log.info("Going to process file %s", file_path)
    formatter.process(file_path)
    log.info("%s file was processed", file_path)
