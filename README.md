# facts-totaling

This is a minimal prototype of a totaling module for summing sealevel rise projections generated from different sources and modules. `totaling` is a CLI tool that accepts a path to each netCDF file you would like summed as well as an output path where the summed result will be written. Each input netCDF file represents output from a FACTS sea level component module. It is the responsibility of the user to ensure that the desired and correct files are specified; check that file paths are correct and that each file specified belongs to the same scale ('global' or 'local'). 

It is possible to run multiple FACTS sea-level components with different default values for common parameters such as `pyear-start` and `pyear-end`. If that happens, `totaling` will not cause a failure, but will show a message similar to the following: 
```shell
⚠️⚠️ Start years are not the same across all datasets. Check default
values of --pyear-start in these modules. Received: [YYYY YYYY]. ⚠️⚠️
```

## Example running cli
Using output from an 'experiment' run using docker compose that multiple modules. Can specify any number of `--item` inputs, include a path to a module-level output for each. 

Clone repo (`initial_mvp` branch):
```shell
git clone --single-branch --branch initial_mvp git@github.com:fact-sealevel/totaling.git
```

From the project root, create a Docker container:
```shell
docker build -t totaling .
```

Run totaling in a container. Mount the directory containing the input data as a volume, and the directory where you'd like to write the output file. Then, use the file names in the actual arguments:
```shell
docker run --rm \
-v /path/to/input/data:/mnt/totaling_in \
-v /path/to/output/data:/mnt/totaling_out \
totaling \
--item /mnt/totaling_in/module_output_1.nc \
--item /mnt/totaling_in/module_output_2.nc \
--item /mnt/totaling_in/module_output_3.nc \
--output-path /mnt/totaling_out/totaled_output.nc
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
docker run --rm totaling --help
```
