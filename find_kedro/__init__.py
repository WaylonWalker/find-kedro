"""
find-kedro

kedro plugin to automatically construct pipelines using pytest style pattern matching

Example Usage of find-kedro:

``` python
# run.py
from kedro.context import KedroContext
from find_kedro import find_kedro

class ProjectContext(KedroContext):
    def _get_pipelines(self) -> Pipeline:
        return find_kedro()
```
"""
__version__ = "0.1.0"

__all__ = ["find_kedro"]
from find_kedro.core import find_kedro
