#!/usr/bin/env python

"""Common CLI commands."""

import logging
import sys

import click

from docker_sign_verify import __version__


def logging_options(function):
    """Common logging options."""

    function = click.option(
        "-s", "--silent", "verbosity", flag_value=0, help="Suppress all output."
    )(function)
    function = click.option(
        "-q",
        "--quiet",
        "verbosity",
        flag_value=1,
        help="Restrict output to warnings and errors.",
    )(function)
    function = click.option(
        "-d",
        "--debug",
        "-v",
        "--verbose",
        "verbosity",
        flag_value=3,
        help="Show debug logging.",
    )(function)
    function = click.option(
        "-vv", "--very-verbose", "verbosity", flag_value=4, help="Enable all logging."
    )(function)

    return function


def set_log_levels(verbosity):
    """
    Assigns the logging levels in a consistent way.

    Args:
        verbosity: The logging verbosity level from  0 (least verbose) to 4 (most verbose).
    """
    levels = {
        0: logging.FATAL,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: logging.NOTSET,
    }

    if verbosity is None:
        verbosity = 2

    format = None
    if verbosity < 3:
        format = "%(message)s"
        logging.getLogger("gnupg").setLevel(logging.FATAL)
    elif verbosity == 3:
        format = "%(asctime)s %(levelname)-8s %(message)s"
        logging.getLogger("gnupg").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
    else:
        # format = "%(asctime)s.%(msecs)d %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d]  %(message)s"
        format = "%(asctime)s.%(msecs)d %(levelname)-8s %(name)s %(message)s"

    logging.basicConfig(
        stream=sys.stdout,
        level=levels[verbosity],
        format=format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@click.command()
def version():
    """Displays the utility version."""

    print(__version__)
