"""Testing ShopStyle API"""
import json
import pprint
import requests

# request that works: http://api.shopstyle.com/api/v2/products?pid=uid2384-40566372-99&fts=red+dress&offset=0&limit=10
# note: sizes different from designer to designer; append to url
# note: color can be appended as a field as well

# r = requests.get("http://api.shopstyle.com/api/v2/products?pid=uid2384-40566372-99&fts=red+dress+small&offset=0&limit=3")
# shop_items = r.json()

# # print shop_items

# total_list = []
# for prop in shop_items["products"]: #each prop is dictionary of an item within shop_items LIST
#     shop_dict = {} 

#     # get values of available sizes


#     shop_dict["id"] = prop["id"]
#     shop_dict["name"] = prop["name"]
#     shop_dict["price"] = prop["priceLabel"]
#     shop_dict["image_url"] = prop["image"]["sizes"]["Best"]["url"]
#     shop_dict["url"] = prop["clickUrl"]
#     total_list.append(shop_dict)

# print total_list

def ShopStyleResults(c_concepts, c_color, size): # make sure to include size too; size is a str
    """Construct ShopStyle API request using concepts extrated from Clarifai & pinterest"""

    concept_set = set(c_concepts) # change into set, remove duplicates even if coming from color
    concept_set.add(c_color)
    #import pdb; pdb.set_trace()

    api_request_str = "http://api.shopstyle.com/api/v2/products?pid=uid2384-40566372-99&offset=0&limit=3&fts="
        #concept = concept.replace(' ', '+') # convert spaces into %20 for API request
        #concept = concept.replace("'s", '') # remove 's from strings
        #concept.del(' ')
    for concept in concept_set:
        api_request_str += concept + '+' #append all keywords to end of URL

    # if '++' in api_request_str:
    #     api_request_string.replace('++','+')

    api_request_str += size
    
    #api_request_str = api_request_str[:-1] # strip plus from end of API request str
    print api_request_str # debugging

    shop_request = requests.get(api_request_str)
    shop_data = shop_request.json()

    total_list = []
    for prop in shop_data["products"]: #create the shop dictionary here
        shop_dict = {}

        shop_dict["id"] = prop["id"]
        shop_dict["name"] = prop["name"]
        shop_dict["price"] = prop["priceLabel"]
        shop_dict["image_url"] = prop["image"]["sizes"]["Best"]["url"]
        shop_dict["url"] = prop["clickUrl"]
        total_list.append(shop_dict)
    
    print total_list #returns list of dictionaries associated with shopstyle item

# def ShopStyleResults(c_concepts, c_color, size): # make sure to include size too
#     """Construct ShopStyle API request using concepts extrated from Clarifai & pinterest"""
#     # sample concept list retured from Clarfai Results function: [u'Bodysuit', u'Midi Skirt', u"Women's Shorts"]
#     # r = api.get('https://openapi.etsy.com/v2/listings/active?fields=listing_id,title,url&keywords=wedding,ring,ruby')
#     api_request_str = "http://api.shopstyle.com/api/v2/products?pid=uid2384-40566372-99&offset=0&limit=3&fts=" #+ c_color + "+"
#     for concept in c_concepts:
#         #concept = concept.replace(' ', '+') # convert spaces into %20 for API request
#         concept = concept.replace("'s", '') # remove 's from strings
#         api_request_str += concept + '+' #append all keywords to end of URL
    
#     api_request_str = api_request_str[:-1] # strip plus from end of API request str
#     print api_request_str # debugging
#     shop_request = requests.get(api_request_str)
#     shop_data = shop_request.json()

#     total_list = []
#     for prop in shop_data["products"]: #create the shop dictionary here
#         shop_dict = {}

#         shop_dict["id"] = prop["id"]
#         shop_dict["name"] = prop["name"]
#         shop_dict["price"] = prop["priceLabel"]
#         shop_dict["image_url"] = prop["image"]["sizes"]["Best"]["url"]
#         shop_dict["url"] = prop["clickUrl"]
#         total_list.append(shop_dict)
    
#     return total_list

test = ShopStyleResults(['heels','electric'], 'blue','7') # need to process spaces, colons, commas
print test
# list_dict = test['results'] # gives a list of dictionaries

