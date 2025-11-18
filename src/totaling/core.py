from typing import List
import xarray as xr
import pathlib


class WorkflowTotaler:
    """This is a class that handles totaling of sealevel projections from modules included in a workflow."""

    def __init__(
        self,
        name: str,
        paths_list: List[str],
    ):
        self.name = name
        self.paths_list = paths_list

    def get_projections(self, scale) -> xr.Dataset:
        """Method to read in component-level projection datasets from nc files and combine
        along a 'file' dim that is added to each.
        - scale is 'global' or 'local'
              - currently only 'global' is implemented.
        """

        def preprocess_fn(ds: xr.Dataset) -> xr.Dataset:
            """minimal preprocess function to just add file dimension.
            you can still total a file prepared this way but won't know what
            modules were summed."""

            ds = ds.expand_dims("file")
            ds["file"] = ["abc"]
            return ds

        assert hasattr(self, "paths_list"), (
            "WorkflowTotaler object must have 'paths_list' attribute."
        )

        if scale.lower() not in ["global", "local"]:
            raise ValueError(
                f"Scale '{scale}' not recognized, must be 'global' or 'local'."
            )
        if scale.lower() == "local":
            raise NotImplementedError("Local scale totaling not yet implemented.")

        if scale.lower() == "global":
            combined_ds = xr.open_mfdataset(
                self.paths_list,
                concat_dim="file",
                combine="nested",
                preprocess=preprocess_fn,
            )
        else:
            raise ValueError(
                f"Scale '{scale}' not recognized, must be 'global' or 'local'."
            )

        setattr(self, f"projections_ds_{scale}", combined_ds)

    def total_projections(self, scale) -> xr.Dataset:
        """function to total projections along 'file' dim added in get_projections().
        returns xr.Dataset with totaled projections and sets a self.totaled_ds_{scale} attr"""

        assert scale.lower() in ["global", "local"], (
            f"Scale '{scale}' not recognized, must be 'global' or 'local'."
        )

        # Make sure projections have been read in
        assert hasattr(self, f"projections_ds_{scale}"), (
            f"No projections dataset found for scale '{scale}'. Please run get_projections first."
        )
        ds = getattr(self, f"projections_ds_{scale}")

        ds["totaled_sea_level_change"] = ds["sea_level_change"].sum(dim="file")
        setattr(self, f"totaled_ds_{scale}", ds)
        return ds

    def write_totaled_projections(self, outpath: str, scale: str):
        """Writes the totaled projections to a netCDF file.

        Args:
            scale (str): Scale of totaling, 'global' or 'local'.
            outpath (str): Path to write the netCDF file to.
        """
        assert hasattr(self, f"totaled_ds_{scale}"), (
            f"No totaled dataset found for scale '{scale}'. Please run get_projections first."
        )
        totaled_ds = getattr(self, f"totaled_ds_{scale}")
        outpath = pathlib.Path(outpath)
        totaled_ds.to_netcdf(outpath)
