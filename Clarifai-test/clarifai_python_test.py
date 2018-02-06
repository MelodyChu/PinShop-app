from clarifai.rest import ClarifaiApp
import json
import pprint

app = ClarifaiApp()

model = app.models.get('apparel')

response = model.predict_by_url(url='https://img1.etsystatic.com/188/0/14557766/il_340x270.1395901375_qa6z.jpg')

pprint.pprint(response)

concepts = response['outputs'][0]['data']['concepts'] #gets me a list of dictionaries containing e/ concept & probability
pprint.pprint(concepts)

for concept in concepts: # for each mini dictionary in concepts
    if concept['value'] > 0.5:
        print "Concept: " + concept['name'] + ", Confidence: " + str(concept['value'])
