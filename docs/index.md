<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery.terminal/2.15.2/js/jquery.terminal.min.js'></script>

# ![Find Kedro Title](./art/find-kedro.png)

`find-kedro` is a small library to enhance your kedro experience.  It looks through your modules to find kedro pipelines, nodes, and iterables (lists, sets, tuples) of nodes.  It then assembles them into a dictionary of pipelines, each module will create a separate pipeline, and `__default__` being a combination of all pipelines.  This format is compatible with the kedro `_create_pipelines` format.

## ![Installation](./art/headers/2.png)

`find-kedro` is deployed to [pypi](https://pypi.org/project/find-kedro/) and can easily be `pip` installed.
 
> if you dont already have python and kedro installed follow the [kedro](https://kedro.readthedocs.io/en/stable/02_getting_started/01_prerequisites.html) prerequisites

<div class="termy">
``` console
pip install find-kedro
---> 100%
Successfully installed find-kedro
```
</div>


### Example Response

``` json
{
  "__default__": [
    "create_int_iris",
  ],
  "pipelines.data_engineering.pipeline": [
    "create_int_iris",
  ],
```
