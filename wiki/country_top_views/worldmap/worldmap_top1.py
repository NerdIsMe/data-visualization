import plotly.express as px
import pandas as pd
import json 

# import geojson data
with open('./countries.geojson') as f:
	countries = json.load(f)

# import visualization data
df = pd.read_csv('../0818/country_top1_view.csv')
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

fig = px.choropleth(df, geojson=countries, locations='country', color='article',
					featureidkey='properties.name', 
					color_discrete_sequence=px.colors.qualitative.Light24, # set color
					custom_data=['country', 'article', 'views'])
print(countries["features"][0]["properties"]['name'])

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.update_traces(hovertemplate = ("%{customdata[0]}<br>Article: %{customdata[1]}<br>"
                                        + "Pageviews: %{customdata[2]}<br>" 
                                       + "<extra></extra>"))

# 設置地圖呈現模式
fig.update_geos(projection_type="natural earth")
fig.write_html('top1.html')