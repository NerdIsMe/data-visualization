import requests, json
from fake_useragent import UserAgent

# get country top 1000 views
url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/VN/all-access/2021/08/18'
top1000 = requests.get(url, headers={'user-agent': UserAgent().random})

top_dict = top1000.json()
print(top_dict)
if 'title' in top_dict and top_dict['title'] == 'Not found.':
	print('not exist.')
# # 如果 top_dict 有 'title' key = 'Not found.' 代表該國沒有 wiki 資料
# with open('result.json', 'w') as f:
# 	json.dump(top_dict, f)

# with open('result.json', 'r') as f:
# 	aa = json.load(f)
# print(aa)