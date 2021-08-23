import plotly.express as px
import pandas as pd
import json 

with open('./countries.geojson') as f:
	countries = json.load(f)

df = pd.read_csv('./countries.csv')

fig = px.choropleth(df, geojson=countries, locations='name', color='wiki_stats',
					featureidkey='properties.name')
print(countries["features"][0]["properties"]['name'])

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(projection_type="natural earth")
fig.write_html('plotly.html')