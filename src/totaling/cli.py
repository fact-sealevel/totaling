import click
from totaling.core import WorkflowTotaler


@click.command()
@click.option(
    "--name",
    type=str,
    default="my_workflow_name",
    show_default=True,
    help="Name of the workflow being totaled.",
)
@click.option(
    "--item",
    multiple=True,
    required=True,
    help="Paths to component-level projection netcdf files to be totaled.",
)
@click.option(
    "--scale",
    type=str,
    default="global",
    show_default=True,
    help="Scale at which to total projections: 'global' or 'local'.",
)
@click.option(
    "--output-path",
    type=str,
    required=True,
    help="Path to write totaled projections netcdf file.",
)
def main(name, item, scale, output_path):
    click.echo("Hello from FACTS totaling!")
    paths_list = list(item)
    # Create totaler obj
    totaler = WorkflowTotaler(
        name=name,
        paths_list=paths_list,
    )

    # Read files and total projections
    totaler.get_projections(scale=scale)

    # Calc sum
    totaler.total_projections(scale=scale)

    # Write totaled projections to file
    totaler.write_totaled_projections(scale=scale, outpath=output_path)
