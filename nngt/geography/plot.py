import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs

from ..plot import draw_network
from .countries import maps, convertors, country_points, country_codes


def draw_map(graph, node_names, geodata=None, geodata_names=None,
             points=None, show_points=False, linecolor=None, hue=None,
             proj=None, all_geodata=True, axis=None, show=False, **kwargs):
    '''
    Draw a network on a map.

    Parameters
    ----------
    graph : :class:`~nngt.Graph` or subclass
        Graph to plot.
    node_names : str
        Name of the node attribute containing the nodes names that will be
        used to place them on the map. By default (if no `geodata` is
        provided), these must be country names or (better) A3 codes.
    geodata : :class:`geopandas.GeoDataFrame`, optional (default: world map)
        Optional dataframe containing the geospatial information.
        Predefined geodatas are "110m", "50m", and "10m" for world maps with
        respectively 110, 50, and 10 meter resolutions, or "adaptive" (default)
        for a world map with adaptive resolution depending on the country size.
    geodata_names : str, optional (default: "NAME_LONG" or "SU_A3")
        Column in `geodata` corresponding to the `node_names` (respectively
        for full country names or A3 codes).
    points : str, optional (default: capitals and representative points)
        Whether a precise point should be associated to each node.
        Either an entry in `geodata`, "centroid", or "representative".
    show_points : bool, optional (default: False)
        Wether the points should be displayed.
    linecolor : str, char, float or array, optional (default: current palette)
        Color of the map lines.
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

    # check whether the names are full names or A3 codes
    is_a3_codes = True

    for n in names:
        if len(n) != 3:
            is_a3_codes = False
            break

    convert = None

    if geodata_names is None:
        if is_a3_codes:
            geodata_names = "SU_A3"
        else:
            geodata_names = "NAME_LONG"

    # set map
    world_map = True
    dataframe = None

    geodata = "adaptive" if geodata is None else geodata

    if isinstance(geodata, str):
        dataframe = maps[geodata]

        # update names
        if not is_a3_codes:
            names = [convertors.get(name, name) for name in names]
    else:
        world_map = False

    # projection
    if proj is None:
        proj = ccrs.PlateCarree()
    else:
        try:
            crs_proj4 = proj.proj4_init
            dataframe = dataframe.to_crs(crs_proj4)
        except:
            # PlateCarree
            pass

    if axis is None:
        fig = plt.figure()
        axis = plt.axes(projection=proj)

    # underlying map (optional)
    if all_geodata:
        dataframe.boundary.plot(ax=axis, color=linecolor, alpha=0.2, zorder=0)

    # get existing elements
    mapping = None

    if is_a3_codes and isinstance(geodata, str):
        cc = country_codes[geodata]
        mapping = {n: cc[n] for n in names}
    else:
        mapping = {s[geodata_names]: i for i, s in dataframe.iterrows()}

    elements = [mapping[n] for n in names]

    if hue is None:
        dataframe.iloc[elements].boundary.plot(ax=axis, color=linecolor,
                                               zorder=1)
    else:
        if hue not in dataframe:
            dataframe[hue] = np.full(len(dataframe), np.NaN)

            dataframe.loc[elements, hue] = graph.node_attributes[hue]

        dataframe.iloc[elements].plot(column=hue, ax=axis, zorder=1)

    # get positions
    pos = []

    if points in dataframe:
        if show_points:
            dataframe[elements, points].plot(ax=axis, zorder=2)
        pos = [(p.xy[0][0], p.xy[1][0])
               for p in dataframe.iloc[elements, points]]
    elif points == "centroid":
        df = dataframe.loc[elements, "geometry"].centroid
        if show_points:
            df.plot(ax=axis, zorder=2)
        pos = [(p.xy[0][0], p.xy[1][0]) for p in df]
    elif points == "representative":
        df = dataframe.loc[elements, "geometry"].representative_point()
        if show_points:
            df.plot(ax=axis, zorder=2)
        pos = [(p.xy[0][0], p.xy[1][0]) for p in df]
    elif points is None and geodata in (None, "adaptive"):
        try:
            crs_proj4 = proj.proj4_init
            cpoints = country_points.to_crs(crs_proj4)
        except:
            # PlateCarree
            cpoints = country_points
        df = cpoints.loc[elements, "geometry"]
        pos = [(p.xy[0][0], p.xy[1][0]) for p in df]
    elif points is None:
        df  = dataframe.loc[elements, "geometry"].representative_point()
        pos = [(p.xy[0][0], p.xy[1][0]) for p in df]
    else:
        raise ValueError("Invalid value for `points`: {}".format(points))

    pos = np.array(pos)

    if "restrict_nodes" in kwargs:
        pos = pos[kwargs["restrict_nodes"]]

    rm_kw = [
        "show_environment", "positions", "axis", "tight", "fast", "spatial"
    ]

    for k in rm_kw:
        if k in kwargs:
            del kwargs[k]

    # make plot
    draw_network(graph, layout=pos, axis=axis, show_environment=False,
                 fast=True, tight=False, proj=proj, spatial=False, show=False,
                 **kwargs)

    # restore full map
    if all_geodata:
        axis.set_global()

    if show:
        plt.show()

    return axis
