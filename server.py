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
        c_concepts = pin_description.split() #empty list for concepts returned from Clarifai; put this into helper function
        print "***CLARIFAI RESULTS FIRST PRINT C_CONCEPTS***"
        print c_concepts
        #c_concepts = pin_description.split("-")
        #c_concepts = c_concepts.strip()
        #import pdb; pdb.set_trace()
        # c_concepts = pin_description.strip()
        c_concepts = c_concepts[:4] # no more than 4 keywords from pinterest

    else:
        c_concepts = []

    c_response = c_model.predict_by_url(url=image_URL)
    concepts = c_response['outputs'][0]['data']['concepts']

    concept_sort = sorted(concepts, key=lambda k: k['value'])
    top_concept = concept_sort[-1]['name'].split() #find max top concept to put into search query
    print "***TOP CONCEPT FROM CLARIFAI MODEL***"
    print top_concept
    c_concepts += top_concept
    print "***CLARIFAI RESULTS 2nd PRINT C_CONCEPTS WITH TOP PREDICT CONCEPTS"
    print c_concepts #debug
        
    new_concept_list = [] #remove duplicates & clean the concepts list
    for word in c_concepts:
        word = word.replace("'s", '')
        word = word.strip('|-=&#~+/,0123456789.')
        # word = word.split(" ")
        word = word.lower()
        if word not in new_concept_list: # remove unneccessary spaces after the strip
            new_concept_list.append(word)

        # if type(word) == list:
        #     new_concept_list.extend(word)
    
    # remove spaces
    # new_concept_list.remove("and")
    # new_concept_list.remove(" ")

    if len(new_concept_list) > 5: #make sure total search list not greater than 6 keywords
        new_concept_list = new_concept_list[:5]

    print "***CLARIFAI RESULTS 3rd PRINT C_CONCEPTS WITH CLEANED CONCEPTS"
    print new_concept_list #debugging
    return new_concept_list

def check_clothing_type(clarifai_concepts):
    """Identify concepts in clarifai concepts to grab user size for appropriate clothing piece"""
    pant_concepts = set(['jeans','pant','shorts','slacks','capris','trousers'])
    shoe_concepts = set(['shoe', 'boot', 'bootie', 'sneaker', 'slipper', 'heel', 'sandals','moccasin','toe','loafers','flats','oxford','platform', 'pumps'])

    for concept in clarifai_concepts:
        if concept in pant_concepts or (concept + 's') in pant_concepts:
            print 'pant'
            return 'pant'
        elif concept in shoe_concepts or (concept + 's') in shoe_concepts:
            print 'shoe'
            return 'shoe'
    
    print 'top'
    return 'top'

def ShopStyleResults(c_concepts, c_color='', size=''): # make sure to include size too # make c_color & size have default values
    """Construct ShopStyle API request using concepts extrated from Clarifai & Pinterest"""

    concept_set = set(c_concepts) # change into set, remove duplicates even if coming from color
    concept_set.add(c_color)
    #import pdb; pdb.set_trace()
    print "***SHOPSTYLE CONCEPT_SET FIRST PRINT ***"

    api_request_str = "http://api.shopstyle.com/api/v2/products?pid=uid2384-40566372-99&offset=0&limit=20&sort=Popular&fts="

    for concept in concept_set:
        api_request_str += concept + '+' #append all keywords to end of URL

    api_request_str += size #append size to end of the list

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
    
    return total_list #returns list of dictionaries associated with shopstyle item

# Color query: https://openapi.etsy.com/v2/listings/active?includes=MainImage(url_170x135)&fields=listing_id,title,url,mainimage&keywords=Women%20Scarf&color=0000FF&color_accuracy=30&api_key=w31e04vuvggcsv6iods79ol7

def ShopStyle_Retry(c_concepts, c_color, size):
    """Implement retry logic in case shopstyle API doesn't return any results with initial query"""
    results = ShopStyleResults(c_concepts, c_color, size) #results will be a list of dictionaries; if populated
    print results
    retry_count = 0
    original_length = len(c_concepts)
    while len(results) == 0 and retry_count <= (original_length + 2): #len(c_concepts): # if API returns 0 
        if retry_count == 0:
            results = ShopStyleResults(c_concepts, c_color)
            retry_count += 1
            print retry_count
        elif retry_count == 1:
            results = ShopStyleResults(c_concepts)
            retry_count += 1
            print retry_count
        elif retry_count > 1:
            c_concepts = c_concepts[0:-1] #splice off last word in c_concepts each time
            print c_concepts
            results = ShopStyleResults(c_concepts)
            retry_count += 1
            print retry_count

    print retry_count
    return results

def ClarifaiColor(image_URL):
    """function to get 2nd maximum color name from Clarifai color model, as a string"""
    color_response = color_model.predict_by_url(url=image_URL)
    color_concepts = color_response['outputs'][0]['data']['colors']

    concept_sort = sorted(color_concepts, key=lambda k: k['value'])

    color_name = concept_sort[-2]['w3c']['name'] # take 2nd largest color value; index in to get the name

    for i in range(len(color_name)-1,-1,-1):
        if color_name[i].isupper(): #if letter is uppercase
            last_upper_index = i
            break

    short_color = color_name[last_upper_index:].lower()
    print short_color

    return short_color # returns a string of the short name of the color

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
    del session["board"]
    flash("Logged Out.")
    return redirect("/search")


@app.route('/search', methods=['GET', 'POST']) # how to customize search URL per user?
def user_search():
    if request.method == 'GET': 
        # regardless of whether orn ot there is user in session, give option to select size
        if session.get("user_id"): # if there is a user in the session
            user_id = session.get("user_id")
            user = User.query.filter_by(user_id=user_id).first() #create user object
            # user_size = user.size - can get these in Jinja
            # pant_size = user.pant_size
            # shoe_size = user.shoe_size

            if not session.get("pin_username"): #if user has not provided a pinterest username
                melody_pins = get_melody_pins() # this is a list of dicts; will customize once i implement user pin pulls
                
                return render_template("search.html", melody_pins=melody_pins, user=user) # pass melody_pins to jinja
            if session.get("pin_username"): # if user has pin username
                try:
                    board = request.args.get("board-name") 
                    if not board: # if no board inputted in form
                        board = session.get('board')
                        user_pins = get_user_pins_given_board(session["pin_username"], board)
                    else: # if a board IS indeed inputted in form
                        session['board'] = board # add board into session dictionary
                        user_pins = get_user_pins_given_board(session["pin_username"], board)

                    # if session.get('board'): # if board is in session and user is in session
                    #     board = session.get('board')
                    #     user_pins = get_user_pins_given_board(session["pin_username"], board)
    
                    
                except:
                    user_pins = get_user_pins_no_board(session["pin_username"]) #pulls all pins for that user
                    
                return render_template("search.html", melody_pins=user_pins, user=user) # check melody pins which one this == 

        else: #if no user ID in session
            melody_pins = get_melody_pins()
            return render_template("search.html", melody_pins=melody_pins)

                

    if request.method == 'POST':
        # try:
        imageURL = request.form.get('image_URL') # get image URL from the form
        pin_description = request.form.get("image_desc") 
        print "***********PIN DESCRIPTION********************"
        json.dumps(pin_description)
        print pin_description
        print type(pin_description) #SHOULD BE STRING!
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
            clarifai_color = ClarifaiColor(imageURL) # pass in imageURL to clarifai color model; get string of color name back
        except:
            print ("Clarifai API failed to return color result")
            flash("Clarifai API failed to return color result")
        if clarifai_concepts is not None and clarifai_color is not None: # if there is a concept list returned; pass those to the function
            # write a function that checks contents of clarifai concepts to see whether or not item is pant or shoe or something else
            user_size = request.form.get("size") # grab elemnts from the search html form
            user_pant_size = request.form.get("pant_size")
            user_shoe_size = request.form.get("shoe_size")
            clothing_type = check_clothing_type(clarifai_concepts) # pass in clarifai concepts to check the type

            if clothing_type == "pant":
                size = user_pant_size
            elif clothing_type == "shoe":
                size = user_shoe_size
            else:
                size = user_size

            try: 
                shop_data = ShopStyle_Retry(clarifai_concepts, clarifai_color, size) # this will call 2nd helper function (ShopStyleResults)
                #shop_data = ShopStyleResults(clarifai_concepts, clarifai_color, size) ### line of original, non-retry code. 
                print "*****SHOP DATA RETRY RESULTS HERE ******************"
                print shop_data
                print type(shop_data) #etsy_data is a list
                return redirect(url_for('show_results', results=json.dumps(shop_data)))

            except:
                print ("Shopstyle API failed to return results")
                flash("ShopStyle API failed to return results")
        else:
            print ("Nothing returned o-noes")
            return redirect('/search')
    else:
        print ("No process could happen! SadFace :( ")
        return redirect('/search')


@app.route('/results', methods=['GET']) #'make GET & POST conditional'
def show_results(): 
    """display Etsy search results on the results page"""

    results = json.loads(request.args.get('results')) #changes to list of dicts

    return render_template("results.html", results=results) #This works for shopstyle! YAY!

@app.route('/get-item-info', methods=['GET'])
def get_info():
    """Uses Etsy listing ID of saved item to make API call to get the rest of Etsy's info"""
    listing_info = request.args.get('listing_data') #get listing data from ID
    print listing_info
    request_str = 'http://api.shopstyle.com/api/v2/products/' + str(listing_info) + '?pid=uid2384-40566372-99'
    print request_str
    shop_api_data = requests.get(request_str) #not sure if redundant
    shop_api_data = shop_api_data.json()
    print "SHOP API DATA HEREEEE!!!!!! FROM GET ITEM INFO"
    print shop_api_data #CHECK & debug
    # print type(etsy_api_data)
    # print type(etsy_api_data['results'][0]) #debugging
    # print (etsy_api_data['results'][0])
    #return redirect(url_for('save_result', listing_info=jsonify(etsy_api_data['results']))) # now need to get this into add bookmark route
    return jsonify(shop_api_data) #['results'][0])

@app.route('/add-bookmark.json', methods=['POST'])
def save_result():
    """handle users saving Etsy results, with JSON data from get-item-info route""" 
    # print request
    listing_data = request.get_json() #should get JSON blob back for shopstyle API item info
    print "CHECK OUT LISTING DATA TYPE HERE _______________!!!!!!!!!!!!!!!! SHOULD BE JSON OBJECT"
    print type(listing_data) #should be string; it is type UNICODE
    print listing_data
    
    shop_id = listing_data['id']

    #Check if listing already in DB?
    listing = EtsyResult.query.filter(EtsyResult.etsy_listing_id == shop_id).first()
    print "SEE LISTING HERE***********************"
    print listing

    #if listing it's not there in EtsyResult, create it!
    if not listing:
        listing = EtsyResult(etsy_listing_id=listing_data["id"],
                            listing_title=listing_data["name"],
                            listing_url=listing_data["clickUrl"],
                            listing_image=listing_data["image"]["sizes"]["Best"]["url"],
                            listing_price=listing_data["price"]) # not going to use price $ label here
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

