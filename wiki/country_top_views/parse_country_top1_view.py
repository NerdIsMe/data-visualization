import os
import pandas as pd 

folder = './0818/csv'
files = os.listdir(folder)

# read country code to country name
country_code_map = pd.read_csv('./data/country_code.csv')

countries = pd.DataFrame()
# country, article_transformed, view_ceil, rank

for i in files:
	file_pd = pd.read_csv(folder + '/' + i)
	country_code = i.split('.')[0]
	country_name = country_code_map[country_code_map['country code'] == country_code]['country name'].values[0]
	print(country_name)
	countries.loc[country_code, 'country'] = country_name
	countries.loc[country_code, 'article'] = file_pd.loc[0, 'article_transformed']
	countries.loc[country_code, 'views'] = file_pd.loc[0, 'views_ceil']

countries.index.name = 'code'
print(countries)
countries.to_csv('./0818/country_top1_view.csv')