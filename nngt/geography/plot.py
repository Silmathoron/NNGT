import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs

from nngt.plot import draw_network
from .countries import maps, countries, convertors


def draw_map(graph, node_names, geodata=None, geodata_names="NAME_LONG",
             points=None, show_points=False, hue=None, proj=None,
             all_geodata=True, axis=None, show=False, **kwargs):
    '''
    Draw a network on a map.

    Parameters
    ----------
    graph : :class:`~nngt.Graph` or subclass
        Graph to plot.
    node_names : str
        Name of the node attribute containing the nodes names that will be
        used to place them on the map. By default (if no `geodata` is
        provided), these must be country names.
    geodata : :class:`geopandas.GeoDataFrame`, optional (default: world map)
        Optional dataframe containing the geospatial information.
        Predefined geodatas are "110m", "50m", and "10m" for world maps with
        respectively 110, 50, and 10 meter resolutions, or "adaptive" (default)
        for a world map with adaptive resolution depending on the country size.
    geodata_names : str, optional (default: "NAME_LONG")
        Column in `geodata` corresponding to the `node_names`.
    points : str, optional (default: no points)
        Whether a precise point should be associated to each node.
        Either an entry in `geodata` or "centroid", or "representative"
    show_points : bool, optional (default: False)
        Wether the points should be displayed.
    esize : float, str, or array of floats, optional (default: 0.5)
        Width of the edges in percent of canvas length. Available string values
        are "betweenness" and "weight".
    ecolor : str, char, float or array, optional (default: "k")
        Edge color. If ecolor="groups", edges color will depend on the source
        and target groups, i.e. only edges from and toward same groups will
        have the same color.
    max_esize : float, optional (default: 5.)
        If a custom property is entered as `esize`, this normalizes the edge
        width between 0. and `max_esize`.
    threshold : float, optional (default: 0.5)
        Size under which edges are not plotted.
    proj : cartopy crs object, optional (default: cartesian plane)
        Projection that will be used to draw the map.
    all_geodata : bool, optional (default: True)
        Whether all the data contained in `geodata` should be plotted, even if
        `graph` contains only a subset of it.
    axis : matplotlib axis, optional (default: a new axis)
        Axis that will be used to plot the graph.
    **kwargs : dict
        All possible arguments from :func:`~nngt.plot.draw_network`.
    '''
    names = graph.node_attributes[node_names]

    world_map = True

    if geodata is None:
        geodata = maps["adaptive"]

        # update names
        names = [convertors.get(name, name) for name in names]
    elif isinstance(geodata, str):
        geodata = maps[geodata]

        # update names
        names = [convertors.get(name, name) for name in names]
    else:
        world_map = False

    if proj is None:
        proj = ccrs.PlateCarree()
    else:
        crs_proj4 = proj.proj4_init
        geodata = geodata.to_crs(crs_proj4)

    if axis is None:
        fig = plt.figure()
        axis = plt.axes(projection=proj)

    # underlying map (optional)
    if all_geodata:
        geodata.boundary.plot(ax=axis, alpha=0.2, zorder=0)

    # get existing elements
    mapping  = {s[geodata_names]: i for i, s in geodata.iterrows()}
    elements = [mapping[n] for n in names]

    if hue is None:
        geodata.iloc[elements].boundary.plot(ax=axis, zorder=1)
    else:
        if hue not in geodata:
            geodata[hue] = np.full(len(geodata), np.NaN)

            geodata.loc[elements, hue] = graph.node_attributes[hue]

        geodata.iloc[elements].plot(column=hue, ax=axis, zorder=1)

    pos = []

    if points is not None:
        if points in geodata:
            geodata[points].plot(ax=axis, zorder=2)
            pos = [(p.xy[0], p.xy[1]) for p in geodata[points]]
        elif points == "centroid":
            df = geodata.loc[elements, "geometry"].centroid
            df.plot(ax=axis, zorder=2)
            pos = [(p.xy[0], p.xy[1]) for p in df]
        elif points == "representative":
            df = geodata.loc[elements, "geometry"].representative_point()
            df.plot(ax=axis, zorder=2)
            pos = [(p.xy[0][0], p.xy[1][0]) for p in df]

    # get positions
    if len(pos) != graph.node_nb():
        df  = geodata.loc[elements, "geometry"].representative_point()
        pos = [(p.xy[0][0], p.xy[1][0]) for p in df]

    pos = np.array(pos)

    rm_kw = [
        "show_environment", "positions", "axis", "tight", "fast", "spatial"
    ]

    for k in rm_kw:
        if k in kwargs:
            del kwargs[k]

    draw_network(graph, positions=pos, axis=axis, show_environment=False,
                 fast=True, tight=False, proj=proj, spatial=False, show=show,
                 **kwargs)

    return axis
