"""
cli

This module provides a command line interface into find-kedro

```
Usage: find-kedro [OPTIONS]

Options:
  --file-patterns TEXT       glob-style file patterns for Python node module
                             discovery

  --patterns TEXT            prefixes or glob names for Python pipeline, node,
                             or list object discovery

  -d, --directory DIRECTORY  Path to save the static site to
  --version                  Prints version and exits
  -v, --verbose              Prints extra information for debugging
  --help                     Show this message and exit.
```

"""
import os
import sys
from pathlib import Path

import click
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

from find_kedro.core import find_kedro

__version__ = "0.1.1"


# @click.group(name="Find-Kedro")
# def cli():
# pass


# @cli.command()
@click.command()
@click.option(
    "--file-patterns",
    type=str,
    multiple=True,
    default=["*node*", "*pipeline*"],
    help="glob-style file patterns for Python node module discovery",
)
@click.option(
    "--patterns",
    type=str,
    multiple=True,
    default=["*node*", "*pipeline*"],
    help="prefixes or glob names for Python pipeline, node, or list object discovery",
)
@click.option(
    "--directory",
    "-d",
    default=".",
    type=click.Path(exists=False, file_okay=False),
    help="Path to save the static site to",
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Prints extra information for debugging",
)
@click.version_option(__version__, "-V", "--version", help="Prints version and exits")
def cli(file_patterns: str, patterns: str, directory: Path, verbose: bool) -> None:
    if verbose:
        click.echo("python version: {}".format(sys.version))
        click.echo("current directory: {}".format(os.getcwd()))
        click.echo()

        click.echo("find nodes recieved the following input")
        click.echo("file_patterns: {}".format(file_patterns))
        click.echo("patterns: {}".format(patterns))
        click.echo("directory: {}".format(directory))
        click.echo("version: {}".format(__version__))
        click.echo("verbose: {}".format(verbose))

    pipelines = find_kedro(
        file_patterns=file_patterns,
        patterns=patterns,
        directory=directory,
        verbose=verbose,
    )
    import json

    click.echo(
        highlight(
            json.dumps(
                {p: [node.name for node in pipelines[p].nodes] for p in pipelines},
                sort_keys=True,
                indent=2,
            ),
            JsonLexer(),
            TerminalFormatter(),
        )
    )
