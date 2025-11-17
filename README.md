# facts-totaling

This is a very minimal prototype of a totaling module for summing sealevel rise projections generated from different sources and modules. Probably want to change much of how this is set up but this works for now for checking things.

- only global implemented so far
- user needs to pass a list of the full file paths for the desired files to `WorkflowTotaler`
- attr parsing only in place for bamber and deconto so far (want to handle this differently anyway)

## Example

Imagine we ran a FACTS experiment that included bamber and deconto modules. We want to total the projections written for each of these modules into a singular estimate for global and local sea level change. (Note: local not impl yet)

First, specify files to output paths from modules
```shell
file0 = "/path/to/data/output/ais_gslr.nc"
file1 = "/path/to/data/output/output_ais_gslr.nc"
file2 = "path/to/data/output/output_gis_gslr.nc"

files_ls = [file0, file1, file2]
```

Create a `WorkflowTotaler` obj w/ a phony name and the paths list
```shell
from totaling.core import WorkflowTotaler

totaler = WorkflowTotaler(name = "wf name",
                          paths_list = files_ls)

#call get_projections() to read and combine module-level data cubes
# see comments in core.py or notebook about scale and type_flag 
totaler.get_projections(scale='global',
                        type_flag = 'minimal')

# call total.projections() to sum across modules
global_total_ds = totaler.total_projections(type_flag='minimal')

# write totaled output by passing desired output path
totaler.write_totaled_projections(scale='global', outpath = my_output_path)
```
