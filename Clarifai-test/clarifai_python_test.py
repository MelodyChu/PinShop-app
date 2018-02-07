from clarifai.rest import ClarifaiApp
import json
import pprint

c_app = ClarifaiApp()

c_model = c_app.models.get('apparel')

# response = model.predict_by_url(url='https://img1.etsystatic.com/188/0/14557766/il_340x270.1395901375_qa6z.jpg')

# pprint.pprint(response)

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
    concepts = c_response['outputs'][0]['data']['concepts']
        
    for concept in concepts: # for each mini dictionary in concepts
        if concept['value'] > 0.5:
            c_concepts.append(concept['name'])
    print c_concepts
    return c_concepts 

ClarifaiResults('https://i.pinimg.com/736x/f5/70/8c/f5708c5e1ffc548adaa33c28c116461b--date-night-dresses-date-night-outfits.jpg')