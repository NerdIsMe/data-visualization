import pandas as pd
import plotly.express as px
import json, sys

with open('./data/countries.geojson') as f:
	countries = json.load(f)

# country = pd.read_csv('./data/Metadata_Country_API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_2764027.csv')
data = pd.read_csv('./data/age_data.csv', skiprows=4).drop(['Unnamed: 65', "Indicator Name","Indicator Code"], axis=1)
data_long = pd.wide_to_long(data, [''], i=['Country Name', 'Country Code'], j='year')
data_long.rename(columns={'':"percentage"}, inplace=True)
data_long.reset_index(inplace=True)
# ls -ahprint(data_long)
# sys.exit()

fig = px.choropleth(data_long, geojson=countries, locations='Country Code', color='percentage', animation_frame='year',
					featureidkey='properties.iso_a3', range_color=[0, 30],
                    color_continuous_scale='YlGnBu',
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



