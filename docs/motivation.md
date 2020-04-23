
## ![Motivation](./art/headers/1.png)

`kedro` is an amazing project that allows for super fast prototyping of data
pipelines, yet yielding production ready pipelines. `find-kedro` enhances this 
experience by adding a pytest like node discovery eliminating the need to bubble
up pipelines through modules.

When Working on larger pipelines it is advisable to break your pipeline down 
into different submodules which requires knowledge of building python libraries,
and knowing how to properly import each module.  While this is not too difficult, 
in some cases it can trip up even the most senior engineers, loosing precious
feature development time to debugging a library.
