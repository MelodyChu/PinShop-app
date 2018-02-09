from etsy_py.api import EtsyAPI
import json
import pprint

etsy_api = EtsyAPI(api_key=ETSY_KEY)

# get a list of all top level Etsy categories; look at trending categories
#r = api.get('https://openapi.etsy.com/v2/listings/trending?fields=listing_id,title,price')
### r = api.get('https://openapi.etsy.com/v2/listings/active?fields=listing_id,title&keywords=wedding,ring,ruby') # how to get sizes?
#r = api.get('https://openapi.etsy.com/v2/taxonomy/categories?fields=category_id,category_name,meta_title')
### data = r.json()
#pprint(data)
### pprint.pprint(data)


# URL searching for "white boots women"
# https://www.etsy.com/search?q=white%20boots%20women

def EtsyResults(c_concepts, c_color):
    """Construct Etsy API request using concepts extrated from Clarifai"""
    # sample concept list retured from Clarfai Results function: [u'Bodysuit', u'Midi Skirt', u"Women's Shorts"]
    # r = api.get('https://openapi.etsy.com/v2/listings/active?fields=listing_id,title,url&keywords=wedding,ring,ruby')
    api_request_str = 'https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&color_accuracy=30&color=' + c_color + '&keywords='
    for concept in c_concepts: #iterating through list of concepts from Clarifai
        concept = concept.replace(' ', '%20') # convert spaces into %20 for API request
        concept = concept.replace("'s", '') # remove 's from strings
        api_request_str += concept + ',' #append all keywords to end of URL
    
    api_request_str = api_request_str[:-1] # strip comma from end of API request str
    print api_request_str # debugging
    etsy_request = etsy_api.get(api_request_str)
    etsy_data = etsy_request.json()
    etsy_data_list = etsy_data['results'] # gives a list of dictionaries for the result key
    # etsy_data_pp = pprint.pprint(etsy_data)
    #print etsy_data_pp
    return etsy_data_list

test = EtsyResults(['Dress','Women'], 'e6e6fa') # need to process spaces, colons, commas
print test
# list_dict = test['results'] # gives a list of dictionaries

