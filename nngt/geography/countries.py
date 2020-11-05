import os

import geopandas as gpd


folder = os.path.abspath(os.path.dirname(__file__)) + "/world_maps/"


# --------------------------------------------- #
# Load and store the worlds at different scales #
# --------------------------------------------- #

world_110 = gpd.read_file(folder + "ne_110m_admin_0_countries.shp")
world_50  = gpd.read_file(folder + "ne_50m_admin_0_countries.shp")
world_10  = gpd.read_file(folder + "ne_10m_admin_0_countries.shp")

maps = {
    "110m": world_110,
    "50m": world_50,
    "10m": world_10
}


# ----------------------------------------- #
# Store countries and their world/positions #
# ----------------------------------------- #

countries_adaptive = {}
countries_110 = {}
countries_50 = {}
countries_10 = {}


for i, v in world_110.iterrows():
    countries_110[v.NAME_LONG] = i
    countries_adaptive[v.NAME_LONG] = i


new_countries = []

for i, v in world_50.iterrows():
    countries_50[v.NAME_LONG] = i

    if v.NAME_LONG not in countries_adaptive:
        countries_adaptive[v.NAME_LONG] = len(countries_adaptive)
        new_countries.append(i)


world = world_110.append(world_50.iloc[new_countries], ignore_index=True)


new_countries = []

for i, v in world_10.iterrows():
    countries_10[v.NAME_LONG] = i

    if v.NAME_LONG not in countries_adaptive:
        countries_adaptive[v.NAME_LONG] = len(countries_adaptive)
        new_countries.append(i)


world = world.append(world_10.iloc[new_countries], ignore_index=True)

maps["adaptive"] = world

countries = {
    "110m": countries_110,
    "50m": countries_50,
    "10m": countries_10,
    "adaptive": countries_adaptive
}


# ------------------------------------- #
# Add usual covertors for country names #
# ------------------------------------- #

convertors = {
    'Democratic Republic of Korea': 'Dem. Rep. Korea',
    'Iran (Islamic Republic of)': 'Iran',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'China, Taiwan Province of': 'Taiwan',
    'North Macedonia': 'Macedonia',
    'China, mainland': 'China',
    'Serbia and Montenegro': 'Serbia',
    'Sudan (former)': 'Sudan',
    'Belgium-Luxembourg': 'Belgium',
    'Ethiopia PDR': 'Ethiopia',
    'Yugoslav SFR': 'Serbia',
    'Cabo Verde': 'Republic of Cabo Verde',
    'Eswatini': 'eSwatini',
    'Sao Tome and Principe': 'São Tomé and Principe',
    'China, Hong Kong SAR': 'Hong Kong',
    'China, Macao SAR': 'Macao',
    'Congo': 'Republic of the Congo',
    'Czechia': 'Czech Republic',
    'Gambia': 'The Gambia',
}


for k, v in zip(world.FORMAL_EN, world.NAME_LONG):
    if k is not None:
        convertors[k] = v


convertors.update(
    {k: v for k, v in zip(world.NAME_EN, world.NAME_LONG)})


# ----------------------------------- #
# Representative points for countries #
# ----------------------------------- #

country_points = gpd.GeoDataFrame({
    'country': world.NAME_LONG,
    'geometry': world.geometry.representative_point()
})
