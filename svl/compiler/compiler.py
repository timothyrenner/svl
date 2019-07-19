import os
import sqlite3

from svl.compiler.ast import parse_svl
from svl.compiler.errors import (
    SvlSyntaxError,
    SvlMissingFileError,
    SvlMissingDatasetError,
    SvlDataLoadError,
    SvlPlotError,
    SvlDataProcessingError,
)
from svl.compiler.layout import tree_to_grid
from svl.compiler.plot_validators import validate_plot
from svl.data_sources.sqlite import create_datasets, get_svl_data
from svl.plotly import plotly_template, plotly_template_vars


def _extract_additional_datasets(datasets):
    """ Converts the additional datasets from the name=location format into
        dictionaries for injection into the ast.
    """
    return dict(map(lambda x: x.split("="), datasets))


def svl(
    svl_source, backend="plotly", datasets=[], offline_js=False, debug=False
):
    """ Compiles the SVL source into a rendered plot template.

    Parameters
    -----------
    svl_source : str
        The SVL source code.
    backend : str
        Which plotting backend to render the plots with. Default: "plotly".
    datasets : list[str]
        A list of additional datasets to inject into the ast, for datasets not
        present in the SVL source code. Each dataset specifier must be of the
        form "dataset_name=dataset_location".
    offline_js : bool
        Whether to embed the javascript into the final HTML directly.
        Default: False.
    debug : bool
        If this flag is true, return the pretty-printed parse tree instead of
        the compiled program.

    Returns
    -------
    str
        The rendered HTML template for the plots.

    Raises
    ------
    ValueError
        If there is a malformed additional dataset specifier.
    SvlSyntaxError
        If there is a syntax error in the SVL source.
    SvlMissingFileError
        If there is a missing file in the SVL source or additional datasets.
    SvlMissingDatasetError
        If there is a dataset specified in a plot that isn't in the dataset
        specifiers for the SVL program.
    SvlPlotError
        If there is an error in any of the SVL plots.
    SvlDataLoadError
        If there is an error loading the data into sqlite.
    SvlDataProcessingError
        If there is an error processing the plot data.
    NotImplementedError
        If a backend is selected that hasn't been implemented.
    """
    if debug:
        return parse_svl(svl_source, debug=True).pretty()

    for dataset in datasets:
        if len(dataset.split("=")) != 2:
            raise ValueError(
                "dataset {} needs to be name=path".format(dataset)
            )

    additional_datasets = _extract_additional_datasets(datasets)

    try:
        svl_ast = parse_svl(svl_source, **additional_datasets)
    except SvlSyntaxError as e:
        raise e

    # Validate that all of the files exist that need to exist.
    for _, dataset in svl_ast["datasets"].items():
        if ("file" in dataset) and (not os.path.exists(dataset["file"])):
            raise SvlMissingFileError(
                "File {} does not exist.".format(dataset["file"])
            )

    # Flatten the AST plot representation into a list with grid coordinates.
    svl_plots = tree_to_grid(svl_ast)

    # Validate the plots.
    for plot in svl_plots:
        # Each plot must point to a dataset that exists.
        if plot["data"] not in svl_ast["datasets"]:
            existing_dataset = ", ".join(list(svl_ast["datasets"].keys()))
            raise SvlMissingDatasetError(
                "Dataset {} is not in provided datasets {}.".format(
                    plot["data"], existing_dataset
                )
            )
        # Each plot must be a valid specification.
        ok, msg = validate_plot(plot)
        if not ok:
            raise SvlPlotError("Plot error: {}".format(msg))

    # Set up the connection to sqlite. Eventually this will be abstracted since
    # in principle we could have other data sources but for now sqlite is what
    # we've got.
    try:
        sqlite_conn = create_datasets(svl_ast["datasets"])
    except sqlite3.DatabaseError as e:
        raise SvlDataLoadError("Error loading data: {}.".format(e))

    # Get the data for the plots.
    try:
        svl_plot_data = [get_svl_data(plot, sqlite_conn) for plot in svl_plots]
    except sqlite3.DatabaseError as e:
        raise SvlDataProcessingError(
            "Error processing plot data: {}".format(e)
        )

    # Select and render the template.
    if backend == "plotly":
        template_vars = plotly_template_vars(svl_plots, svl_plot_data)
        template = plotly_template()

        # If offline is selected, use the offline plotly in the template.
        template_vars["plotly_offline"] = offline_js
    else:
        raise NotImplementedError(
            "Unable to use {} as a backend.".format(backend)
        )

    return template.render(**template_vars)
