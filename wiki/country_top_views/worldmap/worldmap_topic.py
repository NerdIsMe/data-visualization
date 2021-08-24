import plotly.express as px
import geopandas as gpd
import pandas as pd
import json 

# import geojson data
wiki_country = pd.read_csv('../data/country_code.csv')
wiki_to_gpd = pd.read_csv('wiki_CountryName_map_to_geopandas.csv')
for i in wiki_to_gpd.index:
	if pd.isnull(wiki_to_gpd.loc[i, 'geopandas name']):
		# print(wiki_to_gpd.loc[i, 'wiki name'])
		continue
	wiki_country['country name'] = wiki_country['country name'].replace(wiki_to_gpd.loc[i, 'wiki name'], wiki_to_gpd.loc[i, 'geopandas name'])

world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_map = world_map.merge(wiki_country, how='left', left_on='name', right_on='country name')
world_map['wiki stats'] = world_map['wiki stats'].replace(True, 'Exists')
world_map['wiki stats'] = world_map['wiki stats'].replace(False, 'Not Exists')

world_map = world_map.fillna('Not Exists')
world_map.rename(columns={'wiki stats': 'wiki_stats'}, inplace=True)

# select continents
world_map = world_map[world_map.continent == 'Asia']
countries = world_map.to_json()
countries = json.loads(countries)
# with open('./countries.geojson') as f:
# 	countries = json.load(f)

# import visualization data
df = pd.read_csv('../0818/country_topic_views.csv')
df.set_index('country', inplace=True)

# change wiki country names to geojson
wiki_to_gpd = pd.read_csv('wiki_CountryName_map_to_geopandas.csv')
for i in wiki_to_gpd.index:
	# wiki 有，但 geopandas 沒有的
	if pd.isnull(wiki_to_gpd.loc[i, 'geopandas name']):
		print(wiki_to_gpd.loc[i, 'wiki name'])
		continue
	# wiki 改名 to geopandas
	df = df.rename(index={wiki_to_gpd.loc[i, 'wiki name']: wiki_to_gpd.loc[i, 'geopandas name']})# ['country'] = ['country name'].replace(wiki_to_gpd.loc[i, 'wiki name'], wiki_to_gpd.loc[i, 'geopandas name'])

df.reset_index(inplace=True)

# select countries from continent
# df = df.merge(world_map[['name']], how='right', left_on='country', right_on='name')

# print(df)

fig = px.choropleth(df, geojson=countries, locations='country', color='views',
					featureidkey='properties.name', 
					# color_discrete_sequence=px.colors.qualitative.Light24, # set color
					# custom_data=['country', 'article', 'views'],
					)
# print(countries["features"][0]["properties"]['name'])

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# fig.update_traces(hovertemplate = ("%{customdata[0]}<br>Article: %{customdata[1]}<br>"
#                                         + "Pageviews: %{customdata[2]}<br>" 
#                                        + "<extra></extra>"))

# 設置地圖呈現模式
fig.update_geos(projection_type="natural earth")
fig.write_html('topic.html')