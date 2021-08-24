import requests
import pandas as pd
from fake_useragent import UserAgent

response = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/top-by-country/all-projects/all-access/2021/07', headers={'user-agent': UserAgent().random})
# print(response.text)
data = response.json()
countries = data['items'][0]['countries']

monthly_views = pd.DataFrame()
for i in countries:
	monthly_views.loc[i['country'], 'rank'] = i['rank']
	monthly_views.loc[i['country'], 'views_ceil'] = i['views_ceil']

monthly_views['views_ceil_per_day'] = monthly_views.views_ceil/31
monthly_views['views_ceil_per_day'] = monthly_views['views_ceil_per_day'].astype(int)

monthly_views.index.name = 'country_code'
monthly_views.to_csv('./data/monthly_pageviews_by_countries_202107.csv')