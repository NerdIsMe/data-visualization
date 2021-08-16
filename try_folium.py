import folium
import pandas as pd
import geopandas as gpd

income_file = pd.read_csv('106_165-9.csv')
# columns: 縣市 鄉鎮市區   村里  納稅單位   綜合所得總額   平均數  中位數  第一分位數  第三分位數      標準差    變異係數
# print(income_file.head())
income_file = income_file.rename(columns={income_file.columns[0]: '縣市'})
a = income_file[['縣市', '鄉鎮市區', '納稅單位', '綜合所得總額']].groupby(['縣市', '鄉鎮市區']).sum()
a['平均數'] = (a.綜合所得總額 / a.納稅單位).round(1)
a['COUNTYNAME'] = a.index.get_level_values(0)
a['TOWNNAME'] = a.index.get_level_values(1)
a['C-T_NAME'] = a['COUNTYNAME'] + '-' + a['TOWNNAME']

geo_data = gpd.read_file('geo_data/TOWN_MOI_1100415.shp', encoding='utf-8')
geo_data['C-T_NAME'] = geo_data.COUNTYNAME + '-' + geo_data.TOWNNAME
merged_data = geo_data.merge(a, how='left', on=['C-T_NAME'])

# geo_data.to_file('geo_data.json', driver='GeoJSONS')

mymap = folium.Map(location=[24, 120.5], zoom_start=7,tiles=None)

choropleth = folium.Choropleth(
	geo_data=merged_data,# 地理資料
	#  name='Choropleth',
	data=merged_data, # 數值資料
	columns=['C-T_NAME', '平均數'], # 用數值資料的哪些欄位顯示
	key_on="feature.properties.C-T_NAME",
	highlight=True,
	fill_color='RdBu',
	#  # threshold_scale=myscale,
	#  fill_opacity=1,
	line_opacity=0.5,
	legend_name='全國各縣市鄉鎮 綜合所得稅所得總額（千元）',
	#  smooth_factor=0
).add_to(mymap)

folium.LayerControl().add_to(mymap)
choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['C-T_NAME', '平均數']))
# folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

mymap.save('index.html')
