from clarifai import rest
from clarifai.rest import ClarifaiApp
import json
import pprint
import re

c_app = ClarifaiApp(api_key='e8cc6c3c0ff6429f8b3f903db3cd9931')

c_model = c_app.models.get('apparel')
color_model = c_app.models.get('color')

#response = c_model.predict_by_url(url='https://img1.etsystatic.com/188/0/14557766/il_340x270.1395901375_qa6z.jpg')
#color_response = color_model.predict_by_url(url='https://joanieclothing.com/media_thing/uploads/2017/01/MATLIDA_FRONT_800x1100.jpg')
# pprint.pprint(response)
# pprint.pprint(color_response)

#color_concepts = color_response['outputs'][0]['data']['colors']

#pprint.pprint(color_concepts)

# def ClarifaiColor(image_URL):
#     """function to get 2nd maximum color name from Clarifai color model, as a string"""
#     color_response = color_model.predict_by_url(url=image_URL)
#     color_concepts = color_response['outputs'][0]['data']['colors']

#     concept_sort = sorted(color_concepts, key=lambda k: k['value'])

#     #print new_concepts
#     """[{u'w3c': {u'hex': u'#000000', u'name': u'Black'}, u'raw_hex': u'#211611', u'value': 0.07}, 
#     {u'w3c': {u'hex': u'#d2b48c', u'name': u'Tan'}, u'raw_hex': u'#daa98f', u'value': 0.11275}, 
#     {u'w3c': {u'hex': u'#2f4f4f', u'name': u'DarkSlateGray'}, u'raw_hex': u'#264f3f', u'value': 0.298}, 
#     {u'w3c': {u'hex': u'#fff0f5', u'name': u'LavenderBlush'}, u'raw_hex': u'#eee5e6', u'value': 0.51925}]"""
    
#     #print new_concepts[-2]
#     #print type(new_concepts[-2])
#     color_name = concept_sort[-2]['w3c']['name'] #splice values of string until 1st upper case - go backwards
#      #"DarkSlateBlue"
#     for i in range(len(color_name)-1,-1,-1):
#         if color_name[i].isupper(): #if letter is uppercase
#             last_upper_index = i
#             print color_name[i]
#             print last_upper_index
#             break

#     print last_upper_index
#     print type(last_upper_index)

#     short_color = color_name[last_upper_index:]
#     print short_color
#     #print short_color

def ClarifaiColor(image_URL):
    """function to get 2nd maximum color name from Clarifai color model, as a string"""
    color_response = color_model.predict_by_url(url=image_URL)
    color_concepts = color_response['outputs'][0]['data']['colors']

    concept_sort = sorted(color_concepts, key=lambda k: k['value'])

    color_name = concept_sort[-2]['w3c']['name'] # take 2nd largest color value; index in to get the name

    for i in range(len(color_name)-1,-1,-1):
        if color_name[i].isupper(): #if letter is uppercase
            last_upper_index = i
            print color_name[i]
            print last_upper_index
            break

    short_color = color_name[last_upper_index:]

    print short_color # returns a string of the short name of the color

    
    # print last_upper_index
    # print color_name[last_upper_index] #should be B

    #color_short = [i:]
    #print color_short #should be Blue

    #print color_name
    #print new_concepts[:-1]['name']


             
    # for color_dict_2 in color_concepts:
    #     if color_dict_2['value'] == max_color_val:
    #         color_concepts.remove(color_dict_2) # remove max val dict from list
    #         print color_concepts #debugging

    # max_2 = color_concepts[0]['value']
    # color_name = color_concepts[0]['name']
    # for c in color_concepts:
    #     if c['value'] > max_2:
    #         c['value'] = max_2
    #         c['name'] = color_name

    # print "THIS IS MAX 2!!!!!"
    # print max_2
    # print color_name

    # for d in color_concepts:
    #     if d['value'] == max_2:
    #         print d
    #         print "CHECK BELOWWWWWWWWW"
    #         print d['raw_hex'][1:]
    #         # print str(d['raw_hex']) + ' ' + str(d['value'])
    #         # return d['raw_hex']

ClarifaiColor('http://picture-cdn.wheretoget.it/83fcxo-i.jpg')
            # print max_color_val
# print "Color: " + str(max_color_hex)
# print "Color value: " + str(max_color_val)

        #print "Color: " + color_dict['raw_hex']


# concepts = response['outputs'][0]['data']['concepts'] #gets me a list of dictionaries containing e/ concept & probability
# pprint.pprint(concepts)

# for concept in concepts: # for each mini dictionary in concepts
#     if concept['value'] > 0.5:
#         print "Concept: " + concept['name'] + ", Confidence: " + str(concept['value'])

# function version

# def ClarifaiResults(image_URL, pin_description=""): #pin descr is string
#     if len(pin_description) > 0:
#         c_concepts = pin_description.split(" ") #empty list for concepts returned from Clarifai; put this into helper function
#         c_concepts = c_concepts[:4] # no more than 4 keywords from pinterest
#     else:
#         c_concepts = []
#     #image_url = request.form["image_url"] #take in image_URL provided by user
#     c_response = c_model.predict_by_url(url=image_URL)
#     #color_response = color_model.predict_by_url(url=image_URL)
#     concepts = c_response['outputs'][0]['data']['concepts']
        
#     for concept in concepts: # for each mini dictionary in concepts
#         if concept['value'] > 0.1:
#             a = concept['name'].split()
#             c_concepts += a # now we have list of concepts

#     new_concept_list = [] #remove duplicates
#     for word in c_concepts:
#         word = word.replace("'s", '')
#         word = word.strip('-=&#~+,')
#         if word not in new_concept_list:
#             new_concept_list.append(word)

#     if len(new_concept_list) > 6:
#         new_concept_list = new_concept_list[:6]

#     print new_concept_list

# ClarifaiResults('https://i.pinimg.com/237x/ea/88/61/ea886171561fb2a883a47e7ec4efd92b.jpg',"Winter~~ women's spring, #spring")

"""[u'Romper', u'Midi Skirt', u'Blouse', u'Sarong', u'Kimonos', u'Skirt', u'Tunic',
 u'Knee Length Skirt', u'Kimono', u"Women's Shorts", u'Tube Top', u'Cardigan', 
 u'Maxi Skirt', u'Cocktail Dress', u'Dress', u'Halter Top', u"Women's Scarf", u'Jumpsuit']"""















