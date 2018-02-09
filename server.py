"""PinShop App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from clarifai.rest import ClarifaiApp
import json
import pprint

from etsy_py.api import EtsyAPI

from model import connect_to_db, db, User, EtsyResult 

import os
ETSY_KEY = os.environ.get('ETSY_KEY')

etsy_api = EtsyAPI(api_key=ETSY_KEY)


c_app = ClarifaiApp() #put in app token!
c_model = c_app.models.get('apparel') #Clarifai apparel model
color_model = c_app.models.get('color') #Clarifai color model


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

############
# HELPER FUNCTIONS (to go into another file later)

def ClarifaiResults(image_URL):
    """Get list of concepts extracted from Clarifai API with <0.5 confidence coeff"""
    c_concepts = [] #empty list for concepts returned from Clarifai; put this into helper function
    c_response = c_model.predict_by_url(url=image_URL)
    concepts = c_response['outputs'][0]['data']['concepts']
        
    for concept in concepts: # for each mini dictionary in concepts
        if concept['value'] > 0.5:
            c_concepts.append(concept['name'])
    print c_concepts
    return c_concepts 

# GET MAIN IMAGE FROM ETSY: https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&keywords=Women%20Scarf&api_key=w31e04vuvggcsv6iods79ol7

def EtsyResults(c_concepts, c_color): # takes list from Clarifai results as an argument, and color
    """Construct Etsy API request using concepts extrated from Clarifai"""
    api_request_str = api_request_str = 'https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&color_accuracy=30&color=' + c_color + '&keywords='
    for concept in c_concepts: #iterating through list of concepts from Clarifai
        concept = concept.replace(' ', '%20') # convert spaces into %20 for API request
        concept = concept.replace("'s", '') # remove 's from strings
        api_request_str += concept + ',' #append all keywords to end of URL
    
    api_request_str = api_request_str[:-1] # strip comma from end of API request str
    print api_request_str # debugging
    etsy_request = etsy_api.get(api_request_str)
    etsy_data = etsy_request.json()

    try:
        etsy_data_list = etsy_data['results']
    except:
        print ("I got here OOOOOPSSSSSSSS")
    print etsy_data_list


    return etsy_data_list # returns a list of dictionaries associated with etsy results key

# Color query: https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&keywords=Women%20Scarf&color=0000FF&color_accuracy=30&api_key=w31e04vuvggcsv6iods79ol7

def ClarifaiColor(image_URL): # can optimize next week; need less for loops
    """function to return 2nd maximum color from Clarifai color model, controlling for background color"""
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

    for d in color_concepts:
        if d['value'] == max_2:
            print d['raw_hex'][1:]
            return d['raw_hex'][1:] #returns a string of 2nd highest hex value

def set_val_user_id(): #does this go here? this works
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

########################################################################
#ROUTES GO HERE

@app.route('/register', methods=['GET']) 
def register_form():
    """Show form for user signup."""

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def register_user():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    size = request.form["size"]
    pant_size = int(request.form["pant_size"])
    shoe_size = float(request.form["shoe_size"])

    pw_hash = bcrypt.generate_password_hash(password) #encrypting passowrds
    new_user = User(email=email, password=pw_hash, age=age, size=size, pant_size=pant_size, shoe_size=shoe_size)

    db.session.add(new_user) #specific to the DB session not flask session - to confirm
    db.session.commit()

    flash("User {} added.".format(email))
    return redirect("/search")


@app.route('/login', methods=['GET']) 
def login_form():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Oops! Please log in!")
        return redirect("/login")

    if bcrypt.check_password_hash(user.password, password) == False:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id # session ID will be BIG; includes Etsy payload below

    flash("Logged in")
    return redirect("/search".format(user.user_id))


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/search")


@app.route('/search', methods=['GET', 'POST']) # how to customize search URL per user?
def user_search():
    if request.method == 'GET': 
        # possibly clear previous session query here; every time user searches, clears previous Etsy sult payload
        # if session.my_etsy_list: # if there is something in my_etsy_list from a previous search
        #   session.pop('my_etsy_list', []) -- check this
        return render_template("search.html")
    if request.method == 'POST':
        imageURL = request.form.get('image_URL') # get image URL from the form
        clarifai_concepts = None
        # clarifai_color = None # adding clarifai color here as well
        try:
            clarifai_concepts = ClarifaiResults(imageURL)
        except:
            print ("Clarifai API failed to return concept results")
            flash("Clarifai API failed to return concept results")
        try: 
            clarifai_color = ClarifaiColor(imageURL) # pass in imageURL to clarifai color model
        except:
            print ("Clarifai API failed to return color result")
            flash("Clarifai API failed to return color result")
        if clarifai_concepts is not None and clarifai_color is not None: # if there is a concept list returned; pass those to the function
            try: 
                etsy_data = EtsyResults(clarifai_concepts, clarifai_color) ### is this redundant? 
                print type(etsy_data) #etsy_data is a list
                # session['my_etsy_list'] = etsy_data # try putting into session
                # # print "SEE SESSION HERE BELOW *********************************"
                # # print session
                # return redirect('/results') #if successful, go to results page
                return redirect(url_for('show_results', results=json.dumps(etsy_data)))

            except:
                print ("Etsy API failed to return results")
                flash("Clarifai API failed to return results")
        else:
            print ("Nothing returned o-noes")
            return redirect('/search')
    else:
        print ("No process could happen! SadFace :( ")
        return redirect('/search')

@app.route('/results', methods=['GET'])
def show_results(): 
    """display Etsy search results on the results page"""

    results = json.loads(request.args.get('results')) #changes to list of dicts
    #import pdb; pdb.set_trace()

    return render_template("results.html", results=results) 

@app.route('/add-bookmark.json', methods=['POST'])
def save_result():
    """handle users saving Etsy results""" 
    ### grab data from the saves and commit to EtsyResults table in DB
    # saved_items = request.args.get("[insert saved stuff here from HTML/JQUERY]")
    # put saved_items - entire object - into session
    # put saved_items listing ID into DB using a loop (but what if user un-saves?)
    pass


@app.route('/bookmarks', methods=['GET'])
def view_bookmarks():
    """display the Etsy search rsults that the user has saved"""
    # grab saved items from user session in Jinja
    # iterate through each item
    # return render_template
    pass 



## taking inputs from html form; 2 functions for clarifai API & Etsy API
# results page (get)
# results page - /bookmark (post) - put favorites in the database

# cases where API goes down; email case insensitive
















#############
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    

    app.run(host="0.0.0.0", port=5001)

