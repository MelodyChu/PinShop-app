import json
import pprint
import requests

## REFERENCES
# Pins with known username & board name: https://api.pinterest.com/v3/pidgets/boards/[username]/[board_name]/pins/
# Pins with known username: https://api.pinterest.com/v3/pidgets/users/[username]/pins/
# Get info about particular pin: http://api.pinterest.com/v3/pidgets/pins/info/?pin_ids=521150988102375972,10133167885969245

# r = requests.get("https://api.pinterest.com/v3/pidgets/boards/melodychuchu/fashion/pins/")
# melody_pins = r.json()

# smaller_r = requests.get("https://api.pinterest.com/v3/pidgets/pins/info/?pin_ids=338121884515377315,338121884509661444")
# small = smaller_r.json()

# # print small["data"]
# pin_list = [] #list of all pin dictionaries
# pin_dict = {} #each pin will be individual dictionary
# for pin in small["data"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
#     pin_dict["id"] = pin["id"]
#     pin_dict["description"] = pin["description"] 
#     pin_dict["dominant_color"] = pin["dominant_color"]
#     pin_dict["link"] = pin["link"]
#     pin_dict["image"] = pin["images"]["237x"]["url"]
#     pin_list.append(pin_dict) #append created filtered dictionaries into list

# print pin_list

#process pinterest dict to just give me response fields that I need; then pass to jinja to iterate

#HELPER FUNCTION DRAFT ############################################
# def get_melody_pins():
#     """Make request to Pinterest to get my pins specifically; process to get to fields I need. Returns list of dictionaries"""
#     r = requests.get("https://api.pinterest.com/v3/pidgets/boards/melodychuchu/fashion/pins/") # get my pins from fashion board
#     melody_pins = r.json()

#     # print melody_pins
#     # """{"status": "success", "message": "ok", "code": 0, "data": {"pins": [{"domain": "berta.com", 
#     # "attribution": null, "description": "Berta 2018", "pinner": {"about": "", "location": "", "full_name": "Melody's Blog", "follower_count": 1619, "image_small_url": "https://i.pinimg.com/30x30_RS/0f/cf/01/0fcf01710424da0fa38d686f1ef19510.jpg", "pin_count": 1630, "id": "338122021932110831", "profile_url": "http://www.pinterest.com/melodychuchu/"}, "repin_count": 7, "aggregated_pin_data": {"aggregated_stats": {"saves": 25359, "done": 3}}, "dominant_color": "#ba9a8a", "link": "http://www.berta.com/evening/collection/", "images": {"237x": {"url": "https://i.pinimg.com/237x/45/e3/bf/45e3bf06ed783740633fc4dde87779d1.jpg", "width": 237, "height": 663}}, "embed": null, "is_video": false, "id": "338121884515377315"},"""

#     pin_list = [] #list of all pin dictionaries
#     for pin in melody_pins["data"]["pins"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
#         pin_dict = {} #each pin will be individual dictionary
#         pin_dict["id"] = pin["id"]
#         pin_dict["description"] = pin["description"] 
#         pin_dict["dominant_color"] = pin["dominant_color"]
#         pin_dict["link"] = pin["link"]
#         pin_dict["image"] = pin["images"]["237x"]["url"]
#         pin_list.append(pin_dict) #append created filtered dictionaries into list

#     print "HERE IS PIN LIST!!!!!******************************"
#     print pin_list # will change to return

# get_melody_pins()

# same logic for get user pins. 2 functions - 1 for just username; 1 for board input

def get_user_pins_given_board(p_username, board): # may need to get pinterest username from DB. need to do board name conversion
    """Make request ot Pinterest to get **user** pins with provided board; process to get fields. Returns list of dictionaries where e/ dict is pin obejct"""
    print board
    board = board.replace(' ', '-')
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

    print pin_list # will change to return

get_user_pins_given_board('melodychuchu', 'Hair')

# get_user_pins_given_board('melodychuchu', 'Hair') #need to properly process name; change spaces to dashes -

# def get_user_pins_no_board(p_username): # may need to get pinterest username from DB. need to do board name conversion
#     """Make request ot Pinterest to get **user** pins with provided board; process to get fields. Returns list of dictionaries where e/ dict is pin obejct"""
#     pin_request_str = "https://api.pinterest.com/v3/pidgets/users/" + str(p_username) + "/pins/" # get my pins from fashion board
#     r = requests.get(pin_request_str)
#     user_pins = r.json()

#     pin_list = [] #list of all pin dictionaries
    
#     for pin in user_pins["data"]["pins"]: #data is a list of dictionaries; each pin is a dictionary containinin all info about pin
#         pin_dict = {} #each pin will be individual dictionary
#         pin_dict["id"] = pin["id"]
#         pin_dict["description"] = pin["description"] 
#         pin_dict["dominant_color"] = pin["dominant_color"]
#         pin_dict["link"] = pin["link"]
#         pin_dict["image"] = pin["images"]["237x"]["url"]
#         pin_list.append(pin_dict) #append created filtered dictionaries into list

#     return pin_list # will change to return

# get_user_pins_no_board('melodychuchu')

# def clean_board_name(boardname): #boardname is a string; often with spaces
#     """Format user entered Pinterest board name properly to append to API request"""
#     board = boardname.replace(' ', '-') # replace space with a dash
#     print board

# clean_board_name("Killer Makeup")
