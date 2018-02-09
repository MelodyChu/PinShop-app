from clarifai import rest
from clarifai.rest import ClarifaiApp
import json
import pprint

c_app = ClarifaiApp(api_key=CLARIFAI_KEY)

c_model = c_app.models.get('apparel')
color_model = c_app.models.get('color')

#response = c_model.predict_by_url(url='https://img1.etsystatic.com/188/0/14557766/il_340x270.1395901375_qa6z.jpg')
#color_response = color_model.predict_by_url(url='https://joanieclothing.com/media_thing/uploads/2017/01/MATLIDA_FRONT_800x1100.jpg')
# pprint.pprint(response)
# pprint.pprint(color_response)

#color_concepts = color_response['outputs'][0]['data']['colors']

#pprint.pprint(color_concepts)

def ClarifaiColor(image_URL):
    """function to get 2nd maximum color from Clarifai color model"""
    color_response = color_model.predict_by_url(url=image_URL)
    color_concepts = color_response['outputs'][0]['data']['colors']
    max_color_val = color_concepts[0]['value']
    for color_dict in color_concepts: # for each color dictionary
        if color_dict['value'] > max_color_val:
            color_dict['value'] = max_color_val
             
    for color_dict_2 in color_concepts:
        if color_dict_2['value'] == max_color_val:
            color_concepts.remove(color_dict_2) # remove max val dict from list
            print color_concepts #debugging

    max_2 = color_concepts[0]['value']
    for c in color_concepts:
        if c['value'] > max_2:
            c['value'] = max_2

    print "THIS IS MAX 2!!!!!"
    print max_2

    for d in color_concepts:
        if d['value'] == max_2:
            print d
            print "CHECK BELOWWWWWWWWW"
            print d['raw_hex'][1:]
            # print str(d['raw_hex']) + ' ' + str(d['value'])
            # return d['raw_hex']

ClarifaiColor('https://joanieclothing.com/media_thing/uploads/2017/01/MATLIDA_FRONT_800x1100.jpg')
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

def ClarifaiResults(image_URL):
    c_concepts = [] #empty list for concepts returned from Clarifai; put this into helper function
    #image_url = request.form["image_url"] #take in image_URL provided by user
    c_response = c_model.predict_by_url(url=image_URL)
    #color_response = color_model.predict_by_url(url=image_URL)
    concepts = c_response['outputs'][0]['data']['concepts']
        
    for concept in concepts: # for each mini dictionary in concepts
        if concept['value'] > 0.5:
            c_concepts.append(concept['name'])
    # for loop: put highest confidence color into c_concepts list
    print c_concepts
    return c_concepts 

ClarifaiResults('https://img1.etsystatic.com/188/0/14557766/il_340x270.1395901375_qa6z.jpg')