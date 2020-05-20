# iris


The iris dataset is a data science classic.  It is part of the default kedro pipeline
as of `0.15.9` if you choose to include an example pipeline, which we will use 
for this example. This is a great starting point for your very first experience
with `find-kedro`.  If you are already using kedro with a completed project there
is no need to refactor it to use `find-kedro`, but if you want to implement it on
an active project this example will show you how to refactor your existing `kedro`
pipeline to use `find-kedro`.


## Create a new Environment and activate

I **CANNOT** under emphasize the importance separate environments for each project, example, or
toy that you create.  Not only does it help your project be easier to run later,
but it prevents you from causing major issues inside of environments for you active
development projects.  The **LAST** thing I want you to do is to wreck a day of 
work by installing `find-kedro` and wrecking dependencies in a working environment.

### example using conda

``` console
$ conda create -n find-kedro-iris python=3.7 -y
$ actiavte find-kedro-iris
```

## Install find-kedro and check version

Let's get after it and install `kedro` and `find-kedro` into our new environment.
As I am unsure of what the iris example will look like in future versions of `kedro`
I recommend following along with `kedro==0.15.9`, but feel free to try it with
the latest if you are feeling adventurous.

> ## STOP
> Before continuting make sure that you are using a separate environment for this example using, conda, pipenv, virtualenv or whatever your environment manager of choice is

``` console
$ pip install kedro==0.15.9 find-kedro
```

let's check out our installation before moving forward and make sure everything
looks right.

``` console
$ kedro --version
find-kedro, version 0.15.9
```

``` console
$ find-kedro --version
find-kedro, version 0.0.5
```

``` console
$ find-kedro --help

Usage: find-kedro [OPTIONS]

Options:
  --file-patterns TEXT       glob-style file patterns for Python node module
                             discovery

  --patterns TEXT            prefixes or glob names for Python pipeline, node,
                             or list object discovery

  -d, --directory DIRECTORY  Path to save the static site to
  -v, --verbose              Prints extra information for debugging
  -V, --version              Prints version and exits
  --help                     Show this message and exit.
```


> # Checkpoint
> At this point your development machine is setup for the `find-kedro-iris` project.
> Next we will get the project started by using `kedro-new`


## kedro new

Like I said before, this example is built off of the default kedro iris template.
When Running `kedro new` make sure that you answer `y` to the last question in order
to generate the example project.

``` console
$ kedro new
```

## Follow through these answers
``` bash
Project Name:
=============
Please enter a human readable name for your new project.
Spaces and punctuation are allowed.
 [New Kedro Project]: Find Kedro Iris
Repository Name:
================
Please enter a directory name for your new project repository.
Alphanumeric characters, hyphens and underscores are allowed.
Lowercase is recommended.
 [find-kedro-iris]:
Python Package Name:
====================
Please enter a valid Python package name for your project package.
Alphanumeric characters and underscores are allowed.
Lowercase is recommended. Package name must start with a letter or underscore.
 [find_kedro_iris]:
Generate Example Pipeline:
==========================
Do you want to generate an example pipeline in your project?
Good for first-time users. (default=N)
 [y/N]: y
Change directory to the project generated in /mnt/c/temp/find-kedro-examples/find-kedro-iris
A best-practice setup includes initialising git and creating a virtual environment before running `kedro install` to install project-specific dependencies. Refer to the Kedro documentation: https://kedro.readthedocs.io/
```

Next cd into the `find-kedro-iris` example directory install kedro dependencies and
the project itself.  It is very important that if you have any imports that are 
fully qualified/absolute i.e `from find_kedro_iris.pipeline.data_engineering import pipeline`
that you install the project otherwise `find-kedro` will not not be able to process
the imports.

``` console
$ cd find-kedro-iris
$ kedro install
$ pip install -e src
```

Running `find-kedro` at this point will render an empty pipeline.

``` console
$ find-kedro
{
  "__default__": []
}
```

## implement find-kedro compatible pipelines

`find-kedro` works by pattern matching variables that are either an iterable of nodes,
a node, or a pipeline. By default the pattern is set to any variable with `pipeline`
or `node` in the name.  In order to utilize the existing codebase we will simply
append the following to the end of 
`src/find_kedro_iris/pipelines/data_science/pipeline.py`.

``` diff
+ data_science_pipeline = create_pipeline()
```

And essentially the same to the end of
`src/find_kedro_iris/pipelines/data_engineering/pipeline.py`

``` diff
+ data_engineering_pipeline = create_pipeline()
```

**NOTE** its important to have the word `pipeline` in the name, or to change the
default `patterns` in `find-kedro`.

At this point you should be able to run `find-kedro` and see that it is picking up
pipelines from both modules, and that both modules get combined into the `__default__`
pipeline.

``` console
$ find-kedro

{
  "__default__": [
    "split_data([example_iris_data,params:example_test_data_ratio]) -> [example_test_x,example_test_y,example_train_x,example_train_y]",
    "train_model([example_train_x,example_train_y,parameters]) -> [example_model]",
    "predict([example_model,example_test_x]) -> [example_predictions]",
    "report_accuracy([example_predictions,example_test_y]) -> None"
  ],
  "src.find_kedro_iris.pipelines.data_engineering.pipeline": [
    "split_data([example_iris_data,params:example_test_data_ratio]) -> [example_test_x,example_test_y,example_train_x,example_train_y]"
  ],
  "src.find_kedro_iris.pipelines.data_science.pipeline": [
    "train_model([example_train_x,example_train_y,parameters]) -> [example_model]",
    "predict([example_model,example_test_x]) -> [example_predictions]",
    "report_accuracy([example_predictions,example_test_y]) -> None"
  ]
}
```

I do prefer a bit shorter/cleaner pipeline names so I would personally pass in
`src/find_kedro_iris/pipelines` as the directory to `find-kedro`.

``` console
$ find-kedro -d src/find_kedro_iris/pipelines
{
  "__default__": [
    "split_data([example_iris_data,params:example_test_data_ratio]) -> [example_test_x,example_test_y,example_train_x,example_train_y]",
    "train_model([example_train_x,example_train_y,parameters]) -> [example_model]",
    "predict([example_model,example_test_x]) -> [example_predictions]",
    "report_accuracy([example_predictions,example_test_y]) -> None"
  ],
  "data_engineering.pipeline": [
    "split_data([example_iris_data,params:example_test_data_ratio]) -> [example_test_x,example_test_y,example_train_x,example_train_y]"
  ],
  "data_science.pipeline": [
    "train_model([example_train_x,example_train_y,parameters]) -> [example_model]",
    "predict([example_model,example_test_x]) -> [example_predictions]",
    "report_accuracy([example_predictions,example_test_y]) -> None"
  ]
}
```

## Implement find-kedro plugin

Now you can swap out `create_pipelines` for `find-kedro`, and it will be responsible
for collecting pipelines for you.

line 36 of src/find_kedro_iris/run.py
``` diff
- from find_kedro_iris.pipeline import create_pipelines
+ from find_kedro import find_kedro
```

line 48 of 
``` diff
    def _get_pipelines(self) -> Dict[str, Pipeline]:
-       return create_pipelines()
+       return find_kedro()
```

## remove create_pipelines

Since `find-kedro` is now responsible for collecting pipelines for you, the 
`src/find_kedro_iris/pipelines.py` is no longer used and can be removed.

``` console
$ rm src/find_kedro_iris/pipelines.py
```

## Final Step

🤞Fingers crossed it is time to run your pipeline. Running `kedro run` in your console 
should yield the following result.

``` console
$ kedro run

2020-05-02 23:15:21,755 - root - INFO - ** Kedro project find-kedro-iris
fatal: not a git repository (or any parent up to mount point /mnt)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
2020-05-02 23:15:22,411 - kedro.versioning.journal - WARNING - Unable to git describe /mnt/c/temp/find-kedro-examples/find-kedro-iris
/home/username/miniconda3/envs/find-kedro-iris/lib/python3.7/site-packages/fsspec/implementations/local.py:33:
FutureWarning: The default value of auto_mkdir=True has been deprecated and will be changed to auto_mkdir=False by default in a future release.
  FutureWarning,
2020-05-02 23:15:24,849 - kedro.io.data_catalog - INFO - Loading data from `example_iris_data` (CSVDataSet)...2020-05-02 23:15:24,877 - kedro.io.data_catalog - INFO - Loading data from `params:example_test_data_ratio` (MemoryDataSet)...
2020-05-02 23:15:24,879 - kedro.pipeline.node - INFO - Running node: split_data([example_iris_data,params:example_test_data_ratio]) -> [example_test_x,example_test_y,example_train_x,example_train_y]
2020-05-02 23:15:24,928 - kedro.io.data_catalog - INFO - Saving data to `example_train_x` (MemoryDataSet)...
2020-05-02 23:15:24,929 - kedro.io.data_catalog - INFO - Saving data to `example_train_y` (MemoryDataSet)...
2020-05-02 23:15:24,930 - kedro.io.data_catalog - INFO - Saving data to `example_test_x` (MemoryDataSet)...
2020-05-02 23:15:24,931 - kedro.io.data_catalog - INFO - Saving data to `example_test_y` (MemoryDataSet)...
2020-05-02 23:15:24,933 - kedro.runner.sequential_runner - INFO - Completed 1 out of 4 tasks
2020-05-02 23:15:24,934 - kedro.io.data_catalog - INFO - Loading data from `example_train_x` (MemoryDataSet)...
2020-05-02 23:15:24,936 - kedro.io.data_catalog - INFO - Loading data from `example_train_y` (MemoryDataSet)...
2020-05-02 23:15:24,939 - kedro.io.data_catalog - INFO - Loading data from `parameters` (MemoryDataSet)...
2020-05-02 23:15:24,940 - kedro.pipeline.node - INFO - Running node: train_model([example_train_x,example_train_y,parameters]) -> [example_model]
2020-05-02 23:15:25,536 - kedro.io.data_catalog - INFO - Saving data to `example_model` (MemoryDataSet)...
2020-05-02 23:15:25,537 - kedro.runner.sequential_runner - INFO - Completed 2 out of 4 tasks
2020-05-02 23:15:25,538 - kedro.io.data_catalog - INFO - Loading data from `example_model` (MemoryDataSet)...
2020-05-02 23:15:25,539 - kedro.io.data_catalog - INFO - Loading data from `example_test_x` (MemoryDataSet)...2020-05-02 23:15:25,539 - kedro.pipeline.node - INFO - Running node: predict([example_model,example_test_x]) -> [example_predictions]
2020-05-02 23:15:25,543 - kedro.io.data_catalog - INFO - Saving data to `example_predictions` (MemoryDataSet)...
2020-05-02 23:15:25,544 - kedro.runner.sequential_runner - INFO - Completed 3 out of 4 tasks
2020-05-02 23:15:25,545 - kedro.io.data_catalog - INFO - Loading data from `example_predictions` (MemoryDataSet)...
2020-05-02 23:15:25,546 - kedro.io.data_catalog - INFO - Loading data from `example_test_y` (MemoryDataSet)...2020-05-02 23:15:25,546 - kedro.pipeline.node - INFO - Running node: report_accuracy([example_predictions,example_test_y]) -> None
2020-05-02 23:15:25,547 - src.find_kedro_iris.pipelines.data_science.nodes - INFO - Model accuracy on test set: 96.67%
2020-05-02 23:15:25,549 - kedro.runner.sequential_runner - INFO - Completed 4 out of 4 tasks
2020-05-02 23:15:25,550 - kedro.runner.sequential_runner - INFO - Pipeline execution completed successfully.
```