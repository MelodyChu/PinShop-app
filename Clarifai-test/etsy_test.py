from etsy_py.api import EtsyAPI
import json
import pprint

api = EtsyAPI(api_key='w31e04vuvggcsv6iods79ol7')

# get a list of all top level Etsy categories; look at trending categories
#r = api.get('https://openapi.etsy.com/v2/listings/trending?fields=listing_id,title,price')
r = api.get('https://openapi.etsy.com/v2/listings/active?fields=listing_id,title&keywords=wedding,ring,ruby') # how to get sizes?
#r = api.get('https://openapi.etsy.com/v2/taxonomy/categories?fields=category_id,category_name,meta_title')
data = r.json()
#pprint(data)
pprint.pprint(data)
# https://openapi.etsy.com/v2/listings/active?api_key=w31e04vuvggcsv6iods79ol7 -- request that worked

# URL searching for "white boots women"
# https://www.etsy.com/search?q=white%20boots%20women