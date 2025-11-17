from typing import List
import xarray as xr
import pathlib


class WorkflowTotaler:
    """This is a class that handles totaling of sealevel projections from modules included in a workflow."""

    def __init__(
        self,
        name: str,
        # modules: List[AbstractSealevelModuleCaller],
        paths_list: List[str],
    ):
        self.name = name
        self.paths_list = paths_list
        # self.modules = modules

    def validate_modules(self):
        # validate that the modules provided
        # are real and are members of sealevel_step.modules
        raise NotImplementedError

    def get_projections(self, type_flag: str, scale="global") -> xr.Dataset:
        """Method to read in component-level projection datasets from nc files and combine
        along a 'file' dim that is added to each.
        - type_flag is a standin-in thing for now. it need to be 'minimal' or 'w/attrs'.
             - 'minimal' just adds file dim, no parsing of attrs. (doesn't know what modules it sums)
             - 'w/attrs/ has a very quick way of parsing the module from the description attr (only works for bamber, deconto)
                but the output dataset has an attr that lists what modules were summed.
        - scale is 'global' or 'local'
              - currently only 'global' is implemented.
        """

        # Make sure that totaler object has path list and they're valid
        assert hasattr(self, "paths_list"), (
            "WorkflowTotaler object must have 'paths_list' attribute."
        )

        if type_flag not in ["minimal", "w/ attrs"]:
            raise ValueError(
                f"type_flag '{type_flag}' not recognized, must be 'minimal' or 'w/ attrs'."
            )

        if scale not in ["global", "local"]:
            raise ValueError(
                f"Scale '{scale}' not recognized, must be 'global' or 'local'."
            )

        def preprocess_minimal(ds: xr.Dataset) -> xr.Dataset:
            """minimal preprocess function to just add file dimension.
            you can still total a file prepared this way but won't know what
            modules were summed."""

            ds = ds.expand_dims("file")
            ds["file"] = ["abc"]
            return ds

        def preprocess_w_attrs(ds: xr.Dataset) -> xr.Dataset:
            """preprocess function for global datasets to prepare for totaling.
            currently, 'manually' parses the description attr to identify source module.
            this only done for a few modules so far bc done by hand, want to change approach in future.
            without this, could still sum but wouldn't know what was summed."""

            ds = ds.expand_dims("file")
            ds["file"] = ["abc"]
            desc = ds.attrs["description"]

            if "Global" not in desc:
                raise ValueError(
                    "This preprocess function expects global datasets, did you pass a local one?"
                )
            if "Bamber" in desc:
                if "AIS" in desc:
                    ds["file"] = ["bamber_ais_global"]
                elif "GIS" in desc:
                    ds["file"] = ["bamber_gis_global"]
            elif "Deconto" in desc:
                if "AIS" in desc:
                    ds["file"] = ["deconto_ais_global"]
            return ds

        if scale == "local":
            raise NotImplementedError("Local scale totaling not yet implemented.")

        elif scale.lower() == "global":
            if type_flag == "w/ attrs":
                totaled_ds = xr.open_mfdataset(
                    self.paths_list,
                    concat_dim="file",
                    combine="nested",
                    preprocess=preprocess_w_attrs,
                )
                files_ls = totaled_ds["file"].values.tolist()
                totaled_ds.attrs["description"] = (
                    f"Summed global sealevel change projections from following sources: {files_ls}"
                )
                totaled_ds["projections_sea_level_change"] = totaled_ds[
                    "sea_level_change"
                ].sum(dim="file")
                setattr(self, f"projections_ds_{scale}_w_attrs", totaled_ds)

            elif type_flag == "minimal":
                totaled_ds = xr.open_mfdataset(
                    self.paths_list,
                    concat_dim="file",
                    combine="nested",
                    preprocess=preprocess_minimal,
                )
                totaled_ds["total_sea_level_change"] = totaled_ds[
                    "sea_level_change"
                ].sum(dim="file")
                setattr(self, f"projections_ds_{scale}_minimal", totaled_ds)
        else:
            raise ValueError(
                f"Scale '{scale}' not recognized, must be 'global' or 'local'."
            )

    def total_projections(self, type_flag: str, scale: str) -> xr.Dataset:
        """function to total projections along 'file' dim added in get_projections().
        returns xr.Dataset with totaled projections and sets a self.totaled_ds_{scale} attr"""

        assert scale.lower() in ["global", "local"], (
            f"Scale '{scale}' not recognized, must be 'global' or 'local'."
        )
        assert type_flag.lower() in ["minimal", "w/ attrs"], (
            f"type_flag '{type_flag}' not recognized, must be 'minimal' or 'w/ attrs'."
        )

        # this is a standin
        # soon, don't want two diff attrs for the projection ds, just a quick fix for now
        if type_flag == "minimal":
            assert hasattr(self, "projections_ds_global_minimal"), (
                "No 'minimal' projection dataset found. Did you run get_projections(scale='global', type_flag='minimal')?"
            )
            ds = getattr(self, "projections_ds_global_minimal")
        elif type_flag == "w/ attrs":
            assert hasattr(self, "projections_ds_global_w_attrs"), (
                "No 'w/ attrs' projection dataset found. Did you run get_projections(scale='global', type_flag='w/ attrs')?"
            )
            ds = getattr(self, "projections_ds_global_w_attrs")
        else:
            raise ValueError(
                f"type_flag '{type_flag}' not recognized, must be 'minimal' or 'w/ attrs'."
            )

        ds["totaled_sea_level_change"] = ds["sea_level_change"].sum(dim="file")
        setattr(self, f"totaled_ds_{scale}", ds)
        return ds

    def write_totaled_projections(self, scale: str, outpath: str):
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
