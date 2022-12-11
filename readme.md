# kraken-utils

The <u>`kraken-utils`</u> package is the shared utility namespace for the Kraken build system and
the Kraken wrapper CLI. It contains various generic utilities, as well as the tools for loading
the metadata of a Kraken project.

### Kraken project metadata

A Kraken project contains at least one `.kraken.py` file (build script) and maybe a `.kraken.lock`
file (lock file). The build script at the root of a project may contain hints for the Kraken wrapper
CLI to be able to correctly bootstrap an environment that contains the Kraken build system.

```py
from kraken.utils import metadata

metadata(
    requirements=["kraken-std ^0.4.16"],
)
```

The way that this works is that the `metadata()` function raises an exception that aborts the execution
of the build script before the rest of the script is executed, and the exception contains the metadata.
When the build script is executed by the Kraken build system instead, the function does nothing.

The API to capture the data passed to a call to the `metadata()` function is as follows:

```py
from kraken.utils import metadata_capturing

with metadata_capturing() as metadata_future:
    ...

metadata = metadata_future.result()
```
