# facts-totaling

This is a very minimal prototype of a totaling module for summing sealevel rise projections generated from different sources and modules. Probably want to change much of how this is set up but this works for now for checking things.

- only global implemented so far
- user needs to pass a list of the full file paths for the desired files to `WorkflowTotaler`
- attr parsing only in place for bamber and deconto so far (want to handle this differently anyway)

## Example running cli
Using output from a 'experiment' run using docker compose that included a bamber and a deconto module. Can specify any number of `--item` inputs, include a path to a module-level output for each. 

Clone repo (`initial_mvp` branch):
```shell
git clone --single-branch --branch initial_mvp git@github.com:fact-sealevel/totaling.git
```

Then, from the root directory, run totaling application:
```shell
uv run totaling --item "/path/to/ais_gslr.nc" \
--item "path/to/ais_gslr.nc" \
--item "path/to/output_gis_gslr.nc" \
--scale 'global' \
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
  --scale TEXT        Scale at which to total projections: 'global' or
                      'local'.  [default: global]
  --output-path TEXT  Path to write totaled projections netcdf file.
                      [required]
  --help              Show this message and exit.

```

See the above by running:
```shell
uv run --help
```