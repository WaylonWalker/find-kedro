import importlib
import importlib.util
import os
import sys
from collections.abc import Iterable  # < py38
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, Generator, List, Tuple, Union

from colorama import Fore
from kedro.pipeline import Pipeline, node
from kedro.pipeline.node import Node

raw_pattern_type = Union[List[Union[str, float, int]], str, float, int]


def find_kedro(
    file_patterns: raw_pattern_type = ["*node*", "*pipeline*"],
    patterns: raw_pattern_type = ["*node*", "*pipeline*"],
    directory: Union[str, Path] = ".",
    verbose: bool = False,
):
    """
    collect kedro nodes into a single dictionary of pipelines

    Each module will become a pipeline with a key of its name,
    All modules will be combined together to create the '__default' pipeine

    Arguments
        file_patterns {list} -- list of file globbing patterns
        patterns {list} -- list of variable globbing file_patterns
        directory {str} -- directory to look for pipeline modules in
        verbose {bool} -- prints extra information

    Returns
        {dict} -- dictionary of pipelines
    """
    _vprint("find kedro start", verbose, main=True)
    directory = Path(directory)
    sys.path.append(directory)
    file_patterns, patterns = _cleanse_inputs(file_patterns, patterns, verbose=verbose)
    nodes_files = _discover_files(directory, file_patterns, verbose=verbose)

    if len(nodes_files) == 0:
        _vprint("no modules found, Exiting Now", verbose)
        return {"__default__": Pipeline([])}
    modules = {}
    for nodes_file in nodes_files:
        key = (
            str(nodes_file)
            .replace(f"{directory}{os.sep}", "")
            .replace(os.sep, ".")
            .replace(".py", "")
        )
        modules[key] = _import(nodes_file, directory)
    _vprint("modules found with file pattern match", verbose, modules=modules)

    nodes = {}

    for module in modules:
        module_nodes = _discover_nodes(modules[module], patterns)
        if module_nodes != []:
            nodes[module] = module_nodes
    _vprint("module found with nodes pattern match", verbose, nodes=nodes)

    pipelines = _generate_pipelines(nodes, verbose=verbose)
    _vprint("find kedro end", verbose, main=True)
    return pipelines


def _vprint(title: str, verbose: bool = False, main: bool = False, **kwargs) -> None:
    if verbose:
        if main:
            print(
                f"\n\n{Fore.BLUE}―――――― {Fore.YELLOW}{title.upper()}{Fore.BLUE} ――――――{Fore.RESET}\n\n"
            )
        else:
            print(Fore.LIGHTBLACK_EX, "―" * 30, Fore.RESET)
            print(f"{Fore.YELLOW}{title}{Fore.RESET}")
        for kwarg in kwargs:
            print(f"{Fore.CYAN}{kwarg}: {Fore.GREEN}{kwargs[kwarg]}{Fore.RESET}")


def _cleanse_inputs(
    file_patterns: Union[List[Union[str, float, int]], str, float, int],
    patterns: Union[List[Union[str, float, int]], str, float, int],
    verbose: bool = False,
) -> Tuple[List[str]]:
    """
    normalizes user input and ensures that inputs are properly typed.

    Arguments:
        file_patterns {Union[List[str, float, int], str, float, int]} -- file patterns that find-kedro will use to match files.
        patterns {Union[List[str, float, int], str, float, int]} -- file patterns that find-kedro will use to match variables.
        verbose {bool} -- prints extra information

    """

    _vprint("raw inputs", verbose, file_patterns=file_patterns, patterns=patterns)
    if type(file_patterns) == int or type(file_patterns) == float:
        file_patterns = [str(file_patterns)]
    if type(patterns) == int or type(patterns) == float:
        patterns = [str(patterns)]
    if type(file_patterns) == str:
        file_patterns = [file_patterns]
    if type(patterns) == str:
        patterns = [patterns]
    file_patterns = [str(pattern) for pattern in file_patterns]
    patterns = [str(pattern) for pattern in patterns]
    file_patterns = [
        pattern + ".py" if pattern[-3:] != ".py" else pattern
        for pattern in file_patterns
    ]
    file_patterns = [
        "**/" + pattern if pattern[:3] != "**/" else pattern
        for pattern in file_patterns
    ]

    _vprint("cleansed inputs", verbose, file_patterns=file_patterns, patterns=patterns)
    return file_patterns, patterns


def _generate_pipelines(nodes: Dict, verbose: bool = False) -> Dict[str, List[Node]]:
    """
    generates a dictionary of pipelines to use in ProjectContet

    Arguments:
        nodes {dict} -- dictionary of lists of nodes to turn into pipelines
        verbose {bool} -- prints extra information

    Returns:
        dict -- dictionary of pipelines with each .py file as its own pipeline,
        and every pipeline combined into __default__.
    
    ## Changelog

    * 0.1.0 - deduplicated `__default__` pipeline
    """
    pipelines = {}
    for _node in nodes:
        pipelines[_node] = Pipeline(nodes[_node])
    pipelines["__default__"] = Pipeline(
        set(_flatten([p.nodes for p in pipelines.values()]))
    )
    _vprint(f"generated pipelines", verbose, pipelines=pipelines)
    return pipelines


def _discover_files(
    directory: Path, patterns: List[str], verbose: bool = False
) -> List[Path]:
    """
    looks for filename patterns within the given directory using fnmatch, which
    is a unix like file name match.

    * matches any number of characters
    ? matches single characters
    [] mathes anything in the sequence

    Example
        *nodes* will match ['de_nodes', 'ds_nodes_raw']
        *nodes will match ['de_nodes']
        nodes* will match ['ds_nodes_raw']

    Arguments
        directory {Path} -- directory to start looking for nodes from
        patterns {Lit[str]} -- list of patterns to match files with

    Returns
        list -- list of files that match the pattern within the given directory
    """
    # _vprint(f'looking for files inside {str(directory)}', verbose)
    files = []
    for pattern in patterns:
        globbed = [
            file
            for file in list(directory.glob(str(pattern)))
            if fnmatch(file.name, pattern.replace("**/", ""))
        ]
        files = [*files, *globbed]
    files = [file for file in files if "__pycache__" not in str(file)]
    files = list(set(files))
    _vprint(
        "pattern matched modules",
        verbose & len(files) > 0,
        num_modules_found=len(files),
        directory=directory,
        files_found=[str(f).replace(str(directory) + "/", "") for f in files],
    )
    return files


def _discover_nodes(module, patterns: List[str], verbose: bool = False) -> List[Node]:
    """
    looks for variables with patterns within the given module

    returns a flat list of node objects
    """
    nodes = []
    for pattern in patterns:
        nodes = [
            *nodes,
            *list(
                [
                    getattr(module, var)
                    for var in dir(module)
                    if fnmatch(var, str(pattern))
                ]
            ),
        ]
    # remove kedro.pipeline.nodes
    nodes = [_node for _node in nodes if _node != node]
    nodes = [n.nodes if type(n) == Pipeline else n for n in nodes]
    nodes = [[n] if type(n) != list else n for n in nodes]
    nodes = list(_flatten(nodes))
    nodes = [_node for _node in nodes if isinstance(_node, Node)]
    nodes = list(set(nodes))

    return nodes


def _flatten(items: Iterable) -> Generator:
    """Yield items from any nested iterable"""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in _flatten(x):
                yield sub_x
        else:
            yield x


def _make_path_relative(path: Path, directory: Path) -> Path:
    """removes directory from path, and any leading anchors"""
    relative = Path(str(path.absolute()).replace(str(directory.absolute()), ""))
    if str(relative)[: len(os.sep)] == os.sep:
        relative = Path(str(relative)[len(os.sep) :])
    return relative


def _import(path: Path, directory: Path, verbose: bool = False):
    """dynamically imports module given a path"""
    cwd = os.getcwd()
    os.chdir(directory)
    name = path.name
    # path = str(path).replace(str(directory) + "/", "")
    path = _make_path_relative(path, directory)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (ModuleNotFoundError, ValueError):
        module = _use_importmodule(
            str(path).replace(os.sep, ".").replace(".py", ""), verbose=verbose
        )
    os.chdir(cwd)

    return module


def _use_importmodule(path: Path, verbose: bool = False):
    """
    relative imports do not work well with importlib.util.spec_from_file_location,
    and require a sys.path.append to be imported correctly.  For this reason
    importlib.import_module is the second option.
    """

    # Not sure if this is needed, but it was never hit in a test
    # if path[0] == ".":
    #     path = path[1:]

    sys.path.append(os.getcwd())
    mod = importlib.import_module(path)
    sys.path.pop()  # clean up path, do not permananatly change users path
    return mod
