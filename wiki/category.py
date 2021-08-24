import requests

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "cmtitle": "Category:Afghanistan",
    "cmtype": "subcat",
    "list": "categorymembers",
    "format": "json"
}

R = requests.get(url=URL, params=PARAMS)
DATA = R.json()

PAGES = DATA["query"]["categorymembers"]

for page in PAGES:
    print(page['title'])