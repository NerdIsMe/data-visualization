import os
import pandas as pd 

topics = ['Afghanistan', 'Taliban']
folder = './0818/csv'
files = os.listdir(folder)

# read country code to country name
country_code_map = pd.read_csv('./data/country_code.csv')

# get per day pageview by countries
country_monthly_pageviews = pd.read_csv('./data/monthly_pageviews_by_countries_202107.csv')
country_monthly_pageviews.set_index('country_code', inplace=True)

countries = pd.DataFrame()
# country, article_transformed, view_ceil, rank

for i in files:
	file_pd = pd.read_csv(folder + '/' + i)
	file_pd.set_index('article_transformed', inplace=True)
	country_code = i.split('.')[0]
	
	sum = 0
	for i in topics:
		if i in file_pd.index:
			sum += file_pd.loc[i, 'views_ceil']
	if sum != 0:
		country_name = country_code_map[country_code_map['country code'] == country_code]['country name'].values[0]
		countries.loc[country_code, 'country'] = country_name
		countries.loc[country_code, 'article'] = ', '.join(topics)
		countries.loc[country_code, 'views'] = sum / country_monthly_pageviews.loc[country_code, 'views_ceil_per_day']

countries.index.name = 'code'
print(countries)
countries.to_csv('./0818/country_topic_views.csv')