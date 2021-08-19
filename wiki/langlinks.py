import requests, json
from fake_useragent import UserAgent

url = "https://zh.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "titles": "阿富汗",
    "prop": "langlinks",
    "format": "json",
    "lllang": "en",
    # "lllimit": "100",
    # "llcontinue": "15580374|es",
}
R = requests.get(url=url, params=PARAMS)
data_dict = R.json()
print(data_dict)

result = list((data_dict['query']['pages']).values())[0]
if 'langlinks' in result:
    title_transform = result['langlinks'][0]['*']
    print(title_transform)
else:
    
print(result)
