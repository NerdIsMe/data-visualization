import geopandas as gpd
import matplotlib.pyplot as plt

def plot_taiwan_district(cities = None, cmap='RdBu'):
	geo_data = gpd.read_file('geo_data/TOWN_MOI_1100415.shp', encoding='utf-8')
	if cities == None:
		ax = geo_data.plot(cmap=cmap)
		min_x = 118; max_x = 122.5
		min_y = 21.8; max_y = 26.5
		ax.set_xlim(min_x, max_x)
		ax.set_ylim(min_y, max_y)
									
	else:
		geo_data_select = geo_data[geo_data.COUNTYNAME.isin(cities)]
		ax = geo_data_select.plot(cmap=cmap)
	ax.set_xlabel('Longitude')
	ax.set_ylabel('Latitude')
	fig = ax.figure
	return fig

fig = plot_taiwan_district(cities=['臺中市'])
fig.savefig('./first.jpg', dpi=500)

# 列出字體
# from matplotlib import font_manager
# font_set = {f.name for f in font_manager.fontManager.ttflist}
# for f in font_set:
# print(f)       