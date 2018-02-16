"""PinShop App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from clarifai.rest import ClarifaiApp
import json
import pprint

import requests #check this

from etsy_py.api import EtsyAPI

from model import connect_to_db, db, User, EtsyResult, Bookmark
from helper import ClarifaiResults, EtsyResults, ClarifaiColor, set_val_user_id

import os
ETSY_KEY = os.environ.get('ETSY_KEY')

# etsy_api = EtsyAPI(api_key=ETSY_KEY)
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

def ClarifaiResults(image_URL, pin_description=""): #pin descr is string
    """Get list of concepts from Clarifai *combined with Pinterest description; returns LIST of concepts"""
    if len(pin_description) > 0:
        c_concepts = pin_description.split(" ") #empty list for concepts returned from Clarifai; put this into helper function
        c_concepts = c_concepts[:4] # no more than 4 keywords from pinterest
    else:
        c_concepts = []

    c_response = c_model.predict_by_url(url=image_URL)
    concepts = c_response['outputs'][0]['data']['concepts']
        
    for concept in concepts: # for each mini dictionary in concepts
        if concept['value'] > 0.5:
            a = concept['name'].split()
            c_concepts += a # now we have list of concepts

    new_concept_list = [] #remove duplicates
    for word in c_concepts:
        word = word.replace("'s", '')
        word = word.strip('-=&#~+')
        if word not in new_concept_list:
            new_concept_list.append(word)

    if len(new_concept_list) > 6: #make sure total search list not greater than 6 keywords
        new_concept_list = new_concept_list[:6]

    return new_concept_list

# GET MAIN IMAGE FROM ETSY: https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&keywords=Women%20Scarf&api_key=w31e04vuvggcsv6iods79ol7
# ADD PRICE TO API CALL
def EtsyResults(c_concepts, c_color): # takes list from Clarifai results as an argument, and color
    """Construct Etsy API request using concepts extrated from Clarifai"""
    api_request_str = 'https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,price,mainimage&color_accuracy=30&color=' + c_color + '&keywords='
    for concept in c_concepts: #iterating through list of concepts from Clarifai
        concept = concept.replace(' ', '%20') # convert spaces into %20 for API request
        #concept = concept.replace("'s", '') # remove 's from strings
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

def get_melody_pins():
    """Make request to Pinterest to get my pins specifically; process to get to fields I need. Returns list of dictionaries"""
    r = requests.get("https://api.pinterest.com/v3/pidgets/boards/melodychuchu/fashion/pins/") # get my pins from fashion board
    melody_pins = r.json()

    pin_list = [] # 

    for pin in melody_pins["data"]["pins"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
        pin_dict = {} #each pin will be individual dictionary
        pin_dict["id"] = pin["id"]
        pin_dict["description"] = pin["description"] 
        pin_dict["dominant_color"] = pin["dominant_color"]
        pin_dict["link"] = pin["link"]
        pin_dict["image"] = pin["images"]["237x"]["url"]
        pin_list.append(pin_dict) #append created filtered dictionaries into list

    return pin_list # will change to return

def get_user_pins_no_board(p_username): # may need to get pinterest username from DB. need to do board name conversion
    """Make request ot Pinterest to get **user** pins with provided board; process to get fields. Returns list of dictionaries where e/ dict is pin obejct"""
    pin_request_str = "https://api.pinterest.com/v3/pidgets/users/" + str(p_username) + "/pins/" # get my pins from fashion board
    r = requests.get(pin_request_str)
    user_pins = r.json()

    pin_list = [] #list of all pin dictionaries
    
    for pin in user_pins["data"]["pins"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
        pin_dict = {} #each pin will be individual dictionary
        pin_dict["id"] = pin["id"]
        pin_dict["description"] = pin["description"] 
        pin_dict["dominant_color"] = pin["dominant_color"]
        pin_dict["link"] = pin["link"]
        pin_dict["image"] = pin["images"]["237x"]["url"]
        pin_list.append(pin_dict) #append created filtered dictionaries into list

    return pin_list # will change to return

def get_user_pins_given_board(p_username, board): # may need to get pinterest username from DB. need to do board name conversion
    """Make request ot Pinterest to get **user** pins with provided board; process to get fields. Returns list of dictionaries where e/ dict is pin obejct"""
    board = board.replace(' ', '-') #replace spaces with dashes
    pin_request_str = "https://api.pinterest.com/v3/pidgets/boards/" + str(p_username) + "/" + str(board) + "/pins/" # get my pins from fashion board
    r = requests.get(pin_request_str)
    user_pins = r.json()

    pin_list = [] #list of all pin dictionaries
    
    for pin in user_pins["data"]["pins"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
        pin_dict = {} #each pin will be individual dictionary
        pin_dict["id"] = pin["id"]
        pin_dict["description"] = pin["description"] 
        pin_dict["dominant_color"] = pin["dominant_color"]
        pin_dict["link"] = pin["link"]
        pin_dict["image"] = pin["images"]["237x"]["url"]
        pin_list.append(pin_dict) #append created filtered dictionaries into list

    return pin_list # will change to return


def set_val_user_id(): #does this go here? this works
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

#ROUTES GO HERE ###########################

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
    pinterest_token = request.form["pin-username"] #using Pinterest username as stand-in for token w/o OAuth
    age = int(request.form["age"])
    gender = request.form["gender"]
    size = request.form["size"]
    pant_size = int(request.form["pant_size"])
    shoe_size = float(request.form["shoe_size"])

    pw_hash = bcrypt.generate_password_hash(password) #encrypting passowrds
    new_user = User(email=email, password=pw_hash, pinterest_token=pinterest_token, age=age, gender=gender, size=size, pant_size=pant_size, shoe_size=shoe_size)

    db.session.add(new_user) #specific to the DB session not flask session - to confirm
    db.session.commit()

    session["user_id"] = User.query.filter_by(email=new_user.email).first().user_id #CHECK THIS; make sure user gets into session once they register
    session["pin_username"] = User.query.filter_by(email=new_user.email).first().pinterest_token 
    print "SEE SESSION HERE!!!!!  **********************"
    print session # to debug
    # <SecureCookieSession {u'pin_username': u'melodychuchu', u'user_id': 10}>

    flash("User {} added.".format(email))
    return redirect("/search")


@app.route('/login', methods=['GET']) 
def login_form():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""
    # OAUTH NOTES: URL that works for pinterest: 
    # https://api.pinterest.com/oauth/?state=768uyFys&scope=read_public&client_id=4946875117467610426&redirect_uri=http://localhost:5001/search&response_type=code


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
    session["pin_username"] = user.pinterest_token
    print session #debugging
    # need to put this in registration as well

    flash("Logged in")
    return redirect("/search".format(user.user_id))


@app.route('/logout')
def logout():
    """Log out user."""
    print session["pin_username"]
    del session["user_id"]
    #import pdb; pdb.set_trace()
    del session["pin_username"] # <SecureCookieSession {'user_id': 10, u'pin_username': u'melodychuchu'}>
    flash("Logged Out.")
    return redirect("/search")


@app.route('/search', methods=['GET', 'POST']) # how to customize search URL per user?
def user_search():
    if request.method == 'GET': 
        if not session.get("pin_username"): #if user has not provided a pinterest username
            melody_pins = get_melody_pins() # this is a list of dicts; will customize once i implement user pin pulls
            print "******LOOK HERE FOR PINS!!!!!!!!!!*********************************"
            # print melody_pins
            # print session 
            # import pdb; pdb.set_trace()
            return render_template("search.html", melody_pins=melody_pins) # pass melody_pins to jinja
        else: # if user has pin username
            
            try:
                board = request.args.get("board-name") #use request.args to get board name from input HTML
                user_pins = get_user_pins_given_board(session["pin_username"], board)
                print "***********ROUTE 1 *******************"
            except:
                user_pins = get_user_pins_no_board(session["pin_username"]) #pulls all pins for that user
                print "***********ROUTE 2 *******************"
            return render_template("search.html", melody_pins=user_pins) # check melody pins which one this == 
            

    if request.method == 'POST':
        # try:
        imageURL = request.form.get('image_URL') # get image URL from the form
        pin_description = request.form.get("image_desc") 
        print "***********PIN DESCRIPTION********************"
        print pin_description
        # except:
        #     imageURL = request.args.get('image') # get image URL from selected pin image radio button
        #     print "***********IMAGE URL 2********************"
        clarifai_concepts = None
        # clarifai_color = None # adding clarifai color here as well
        try:
            clarifai_concepts = ClarifaiResults(imageURL, pin_description) #put pin_description in once it works; currently returns none
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

@app.route('/get-item-info', methods=['GET'])
def get_info():
    """Uses Etsy listing ID of saved item to make API call to get the rest of Etsy's info"""
    listing_info = request.args.get('listing_data') #get listing data from ID
    etsy_api_data = etsy_api.get('https://openapi.etsy.com/v2/listings/' + str(listing_info) + '/?includes=MainImage(url_170x135)&fields=listing_id,title,url,price,mainimage') #not sure if redundant
    # https://openapi.etsy.com/v2/listings/114325374/?api_key=w31e04vuvggcsv6iods79ol7 <-- successful call
    etsy_api_data = etsy_api_data.json()
    print etsy_api_data
    print type(etsy_api_data)
    print type(etsy_api_data['results'][0]) #debugging
    print (etsy_api_data['results'][0])
    #return redirect(url_for('save_result', listing_info=jsonify(etsy_api_data['results']))) # now need to get this into add bookmark route
    return jsonify(etsy_api_data['results'][0])

@app.route('/add-bookmark.json', methods=['POST'])
def save_result():
    """handle users saving Etsy results, with JSON data from get-item-info route""" 
    print request
    listing_data = request.get_json()  #shouldn't need to load because listing_data should be json object
    # listing_url = request.args.get("url")
    print "CHECK OUT LISTING DATA TYPE HERE _______________!!!!!!!!!!!!!!!! SHOULD BE JSON OBJECT"
    print type(listing_data) #should be string; it is type UNICODE
    print listing_data
    # import pdb; pdb.set_trace()


    #etsy_id = listing_data_3['u\'listing_id\''] # grab etsy_ID from JSON object of listing data
    etsy_id = listing_data['listing_id']

    #Check if listing already in DB?
    listing = EtsyResult.query.filter(EtsyResult.etsy_listing_id == etsy_id).first()
    print "SEE LISTING HERE***********************"
    print listing

    #if listing it's not there in EtsyResult, create it!
    if not listing:
        listing = EtsyResult(etsy_listing_id=listing_data["listing_id"],
                            listing_title=listing_data["title"],
                            listing_url=listing_data["url"],
                            listing_image=listing_data["MainImage"]['url_170x135'],
                            listing_price=listing_data["price"])
        db.session.add(listing)
        db.session.commit()

    #add the bookmark to bookmark table - regardless of whether or not listing has already been bookmarked
    bookmark = Bookmark(etsy_listing_id=listing.etsy_listing_id,
                        user_id=session["user_id"])
    db.session.add(bookmark)
    db.session.commit()

    return redirect('/bookmarks') #what does the viewfunction actually return here


@app.route('/bookmarks', methods=['GET'])
def view_bookmarks():
    """display the Etsy search rsults that the user has saved"""
    user_id = session.get('user_id') #grab user ID from session
    user_bookmarks = Bookmark.query.filter_by(user_id=user_id).all() #get all bookmarks for 1 user
    print user_bookmarks
    
    listing_list = [] #dictionary of listings, with listing_ID as key and other attributes like price as values
    for item in user_bookmarks:
        item_id = item.etsy_listing_id
        listing_list.append(EtsyResult.query.filter_by(etsy_listing_id=item_id).first()) #put each full Etsy object into lilsting_list
        #listing_dict[item_id] = EtsyResult.query.filter_by(etsy_listing_id=item_id).first() #should gete list of full etsy result back as a list

    return render_template('bookmarks.html',listing_list=listing_list) #pass list of etsy objects to jinja


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

