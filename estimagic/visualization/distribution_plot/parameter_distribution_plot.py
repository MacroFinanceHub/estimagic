"""
Plot the parameters from a list of optimization result params DataFrames.
The plot shows you how robust the estimated parameter values are across your models.

In particular, the plot can answer the following questions:

1. How are the parameters distributed?

2. How large are the differences in parameter estimates between results
compared to the uncertainty around the parameter estimates?

3. Are parameters of groups of results clustered?

The plot is basically a clickable histogram where each individual observation
(in this case the parameter estimate of a particular model) is represented as a brick
in the stack that corresponds to one bar of the histogram.
By hovering or clicking on a particular brick you can learn more about that observation
making it easy to identify and analyze patterns.

"""
import pandas as pd
from bokeh.plotting import curdoc

from estimagic.visualization.distribution_plot.interactive_distribution_plot import (
    interactive_distribution_plot,
)


def parameter_distribution_plot(
    results, group_cols=None, height=None, width=500, x_padding=0.1, num_bins=50,
):
    """Make a comparison plot from a dictionary containing optimization results.

    Args:
        results (list): List of estimagic optimization results where the info
            can have been extended with 'model_class' and 'model_name'
        group_cols (list):
            List of columns (or index levels) by which to group the parameters.
        height (int):
            height of the figure (i.e. of all plots together, in pixels).
        width (int):
            width of the plot (in pixels).
        x_padding (float): the x_range is extended on each side by x_padding
            times the range of the data
        num_bins (int): number of bins

    Returns:
        source (bokeh.models.ColumnDataSource): data underlying the plots
        gridplot (bokeh.layouts.Column): grid of the distribution plots.
    """
    doc = curdoc()
    df = _tidy_df_from_results(results)
    group_cols = ["group", "name"] if group_cols is None else group_cols

    source, grid = interactive_distribution_plot(
        doc=doc,
        source=df,
        value_col="value",
        id_col="model_name",
        group_cols=group_cols,
        subgroup_col="model_class" if "model_class" in df.columns else None,
        figure_height=height,
        width=width,
        x_padding=x_padding,
        num_bins=num_bins,
    )
    return source, grid


def _tidy_df_from_results(results):
    """Convert a list of results to a tidy DataFrame.

    Args:
        results (list): List of estimagic optimization results where the info
            can have been extended with 'model_class' and 'model_name'

    Returns:
        df (pd.DataFrame): tidy Dataframe without the histogram columns.
    """
    results = _add_model_names_if_missing(results)
    df = pd.concat(results, sort=True)
    keep = [x for x in df.columns if not x.startswith("_")]
    df = df[keep].reset_index()
    if "model_class" in df.columns:
        df["model_class"].fillna("No model class", inplace=True)
    return df


def _add_model_names_if_missing(results):
    if not any("model_name" in df.columns for df in results):
        results = [df.copy() for df in results]
        for i, df in enumerate(results):
            df["model_name"] = str(i)
    elif all("model_name" in df.columns for df in results):
        assert all(len(df["model_name"].unique()) == 1 for df in results), (
            """The model name must be the same for all parameters """
            + """in one results DataFrame."""
        )
        unique_model_names = {df["model_name"].unique()[0] for df in results}
        assert len(unique_model_names) == len(
            results
        ), """The model names are not unique."""
    return results
