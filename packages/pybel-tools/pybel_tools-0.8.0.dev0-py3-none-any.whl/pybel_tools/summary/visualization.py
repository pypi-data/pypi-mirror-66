# -*- coding: utf-8 -*-

"""Functions for summarizing graphs.

This module contains functions that provide aggregate summaries of graphs including visualization with matplotlib,
printing summary information, and exporting summarized graphs
"""

import logging

import pandas as pd

from pybel import BELGraph
from pybel.struct.summary import count_functions, count_relations

__all__ = [
    'plot_summary_axes',
    'plot_summary',
]

logger = logging.getLogger(__name__)


def plot_summary_axes(graph: BELGraph, lax, rax, logx: bool = True):
    """Plot the graph summary statistics on the given axes.

    After, you should run :func:`plt.tight_layout` and you must run :func:`plt.show` to view.

    Shows:
    1. Count of nodes, grouped by function type
    2. Count of edges, grouped by relation type

    :param pybel.BELGraph graph: A BEL graph
    :param lax: An axis object from matplotlib
    :param rax: An axis object from matplotlib

    Example usage:

    >>> import matplotlib.pyplot as plt
    >>> from pybel import from_pickle
    >>> from pybel_tools.summary import plot_summary_axes
    >>> graph = from_pickle('~/dev/bms/aetionomy/parkinsons.gpickle')
    >>> fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    >>> plot_summary_axes(graph, axes[0], axes[1])
    >>> plt.tight_layout()
    >>> plt.show()
    """
    ntc = count_functions(graph)
    etc = count_relations(graph)

    df = pd.DataFrame.from_dict(dict(ntc), orient='index')
    df_ec = pd.DataFrame.from_dict(dict(etc), orient='index')

    df.sort_values(0, ascending=True).plot(kind='barh', logx=logx, ax=lax)
    lax.set_title('Number of nodes: {}'.format(graph.number_of_nodes()))

    df_ec.sort_values(0, ascending=True).plot(kind='barh', logx=logx, ax=rax)
    rax.set_title('Number of edges: {}'.format(graph.number_of_edges()))


def plot_summary(graph: BELGraph, plt, logx: bool = True, **kwargs):
    """Plot your graph summary statistics.

    This function is a thin wrapper around :func:`plot_summary_axis`. It
    automatically takes care of building figures given matplotlib's pyplot module as an argument. After, you need
    to run :func:`plt.show`.

    :code:`plt` is given as an argument to avoid needing matplotlib as a dependency for this function

    Shows:

    1. Count of nodes, grouped by function type
    2. Count of edges, grouped by relation type

    :param plt: Give :code:`matplotlib.pyplot` to this parameter
    :param kwargs: keyword arguments to give to :func:`plt.subplots`

    Example usage:

    >>> import matplotlib.pyplot as plt
    >>> from pybel import from_pickle
    >>> from pybel_tools.summary import plot_summary
    >>> graph = from_pickle('~/dev/bms/aetionomy/parkinsons.gpickle')
    >>> plot_summary(graph, plt, figsize=(10, 4))
    >>> plt.show()
    """
    fig, axes = plt.subplots(1, 2, **kwargs)
    lax = axes[0]
    rax = axes[1]

    plot_summary_axes(graph, lax, rax, logx=logx)
    plt.tight_layout()

    return fig, axes
