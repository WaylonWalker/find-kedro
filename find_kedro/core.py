import importlib
import importlib.util
import os
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Union

from colorama import Fore
from kedro.pipeline import Pipeline, node
from kedro.pipeline.node import Node

raw_pattern_type = Union[List[Union[str, float, int]], str, float, int]


def find_kedro(
    file_patterns: raw_pattern_type = ["*node*", "*pipeline*"],
    patterns: raw_pattern_type = ["*node*", "*pipeline*"],
    directory: Union[str, Path] = ".",
    verbose: bool = False,
) -> Dict[str, Pipeline]:
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
    sys.path.append(str(directory))
    # file_patterns, patterns = _cleanse_inputs(file_patterns, patterns, verbose=verbose)
    cleansed_file_patterns = _cleanse_inputs(
        file_patterns, verbose=verbose, is_file_pattern_type=True
    )
    cleansed_patterns = _cleanse_inputs(
        patterns, verbose=verbose, is_file_pattern_type=False
    )

    nodes_files = _discover_files(directory, cleansed_file_patterns, verbose=verbose)

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
        module_nodes = _discover_nodes(
            modules[module], cleansed_patterns, verbose=verbose
        )
        if module_nodes != []:
            nodes[module] = module_nodes
    _vprint("module found with nodes pattern match", verbose, nodes=nodes)

    pipelines = _generate_pipelines(nodes, verbose=verbose)
    _vprint("find kedro end", verbose, main=True)
    return pipelines


def _vprint(
    title: str, verbose: bool = False, main: bool = False, **kwargs: Any
) -> None:
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
    patterns: raw_pattern_type, verbose: bool = False, is_file_pattern_type: bool = True
) -> List[str]:
    """
    normalizes user input and ensures that inputs are properly typed.

    Arguments:
        file_patterns {Union[List[str, float, int], str, float, int]} -- file patterns that find-kedro will use to match files.
        patterns {Union[List[str, float, int], str, float, int]} -- file patterns that find-kedro will use to match variables.
        verbose {bool} -- prints extra information

    """

    _vprint("raw inputs", verbose, patterns=patterns)
    # force List[str] type
    if not isinstance(patterns, Iterable):
        patterns = str(patterns)
    if type(patterns) == str:
        patterns = list(patterns)

    str_patterns = [str(pattern) for pattern in _flatten(patterns)]

    if is_file_pattern_type:
        cleansed_patterns = [
            pattern + ".py" if pattern[-3:] != ".py" else pattern
            for pattern in str_patterns
        ]
        cleansed_patterns = [
            "**/" + pattern if pattern[:3] != "**/" else pattern
            for pattern in str_patterns
        ]
    else:
        cleansed_patterns = str_patterns

    _vprint("cleansed inputs", verbose, patterns=cleansed_patterns)
    return cleansed_patterns


def _generate_pipelines(nodes: Dict, verbose: bool = False) -> Dict[str, Pipeline]:
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
    _vprint("nodes for generating pipelines", verbose, nodes=nodes)
    for _node in nodes:
        pipelines[_node] = Pipeline(nodes[_node])
    pipelines["__default__"] = Pipeline(
        set(_flatten([p.nodes for p in pipelines.values()]))
    )
    _vprint("generated pipelines", verbose, pipelines=pipelines)
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
    files: List[Path] = list()
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


def _discover_nodes(
    module: str, patterns: List[str], verbose: bool = False
) -> List[Node]:
    """
    looks for variables with patterns within the given module

    returns a flat list of node objects
    """
    nodes: List[Union[List, Node, Pipeline, List[Node]]] = []
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
    _vprint("discovered patterns", verbose, nodes=nodes)

    def assert_pipeline_types(pipeline: Any) -> Union[Node, Pipeline, None]:
        if isinstance(pipeline, Node):
            return pipeline
        if isinstance(pipeline, Pipeline):
            return pipeline
        if callable(pipeline) and pipeline.__name__ == "create_pipeline":
            return pipeline()
        else:
            return None

    def pipeline_to_nodes(pipeline: Union[Node, Pipeline]) -> List[Node]:
        if isinstance(pipeline, Pipeline):
            return pipeline.nodes
        else:
            return [pipeline]

    asserted_nodes = [assert_pipeline_types(n) for n in list(_flatten(nodes))]
    _vprint("asserted_nodes", verbose, nodes=asserted_nodes)
    not_none_nodes = [n for n in list(_flatten(asserted_nodes)) if n is not None]
    _vprint("not_none_nodes", verbose, nodes=not_none_nodes)
    listed_nodes = list(_flatten([pipeline_to_nodes(n) for n in not_none_nodes]))
    listed_nodes = list(_flatten([pipeline_to_nodes(n) for n in not_none_nodes]))
    _vprint("listed_nodes", verbose, nodes=listed_nodes)
    deduped_nodes = list(_flatten(list(set(listed_nodes))))
    _vprint("deduped_nodes", verbose, nodes=deduped_nodes)

    return deduped_nodes


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


def _import(
    path: Path, directory: Path, verbose: bool = False
) -> Any:  # unsure how to type module
    """dynamically imports module given a path"""
    cwd = os.getcwd()
    os.chdir(directory)
    name = path.name
    # path = str(path).replace(str(directory) + "/", "")
    path = _make_path_relative(path, directory)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
    except (ModuleNotFoundError, ValueError, AttributeError):
        module = _use_importmodule(
            str(path).replace(os.sep, ".").replace(".py", ""), verbose=verbose  # type: ignore
        )
    os.chdir(cwd)

    return module


def _use_importmodule(path: Path, verbose: bool = False) -> Any:
    """
    relative imports do not work well with importlib.util.spec_from_file_location,
    and require a sys.path.append to be imported correctly.  For this reason
    importlib.import_module is the second option.
    """

    # Not sure if this is needed, but it was never hit in a test
    # if path[0] == ".":
    #     path = path[1:]

    sys.path.append(os.getcwd())
    mod = importlib.import_module(str(path))
    sys.path.pop()  # clean up path, do not permananatly change users path
    return mod
