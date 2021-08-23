import geopandas as gpd 
import pandas as pd
import folium

wiki_country = pd.read_csv('../country_code.csv')
wiki_to_gpd = pd.read_csv('wiki_CountryName_map_to_geopandas.csv')
for i in wiki_to_gpd.index:
	if pd.isnull(wiki_to_gpd.loc[i, 'geopandas name']):
		print(wiki_to_gpd.loc[i, 'wiki name'])
		continue
	wiki_country['country name'] = wiki_country['country name'].replace(wiki_to_gpd.loc[i, 'wiki name'], wiki_to_gpd.loc[i, 'geopandas name'])

world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_map = world_map.merge(wiki_country, how='left', left_on='name', right_on='country name')
world_map['wiki stats'] = world_map['wiki stats'].replace(True, 'Exists')
world_map['wiki stats'] = world_map['wiki stats'].replace(False, 'Not Exists')

world_map = world_map.fillna('Not Exists')

world_map.rename(columns={'wiki stats': 'wiki_stats'}, inplace=True)
world_map.to_file('countries.geojson', driver='GeoJSON')
world_map.to_csv('countries.csv')
# print(world_map)
# plotly


# # folium 
# mymap = folium.Map()
# choropleth = folium.Choropleth(
# 	geo_data = world_map,
# 	data = world_map,
# 	columns = ['name', 'wiki_stats'],
# 	key_on = 'feature.properties.wiki_stats',
# 	highlight=True
# ).add_to(mymap)

# mymap.save('index.html')