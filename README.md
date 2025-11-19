# facts-totaling

This is a very minimal prototype of a totaling module for summing sealevel rise projections generated from different sources and modules. 

## Example running cli
Using output from an 'experiment' run using docker compose that multiple modules. Can specify any number of `--item` inputs, include a path to a module-level output for each. 

Clone repo (`initial_mvp` branch):
```shell
git clone --single-branch --branch initial_mvp git@github.com:fact-sealevel/totaling.git
```

Then, from the root directory, run totaling application:
```shell
uv run totaling --item "/path/to/ais_gslr.nc" \
--item "path/to/ais_gslr.nc" \
--item "path/to/output_gis_gslr.nc" \
--output-path "path/to/test_totaled_output.nc"
```

## Features 
```shell
Usage: totaling [OPTIONS]

Options:
  --name TEXT         Name of the workflow being totaled.  [default:
                      my_workflow_name]
  --item TEXT         Paths to component-level projection netcdf files to be
                      totaled.  [required]
  --output-path TEXT  Path to write totaled projections netcdf file.
                      [required]
  --help              Show this message and exit.

```

See the above by running:
```shell
uv run --help
```
