from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app, check_clothing_type, ShopStyleResults, ClarifaiResults, ShopStyle_Retry
from flask import session

"""Unit tests to test non-API dependent helper functions"""

class CheckClothingType(TestCase):
    """Check if clothing type detection detects the right piece of clothing"""

    def test_check_clothing_type(self):
        assert check_clothing_type(['blue','boot']) == 'shoe'

    def test_check_clothing_type_2(self):
        #self.assertEqual(server.check_clothing_type((['ripped','jean']), 'pant')
        assert check_clothing_type(['ripped','jean']) == 'pant'

    def test_check_clothing_type_3(self):
        self.assertEqual(check_clothing_type(['dress','red']), 'top')
        #assert server.check_clothing_type(['dress','red']) == 'top'

"""Integration tests to test API calls for helper functions"""

# mock API calls for helper functions

class CheckShopStyleRetry(TestCase):
    """Check ShopStyle retry logic using API mocking"""
    
    def setUp(self):

        def _mock_ClarifaiResults(image_URL, pin_description=""):
            """mocking Clarifai results output, which is a list of concepts"""
            return ["women","leather","skirt","black"]

        def _mock_ShopStyleResults(c_concepts, c_color='', size=''):
            """mocking ShopStyle results output, which is a list of items for sale"""
            return [{'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=687703189&pid=uid2384-40566372-99', 'price': '$180', 'image_url': 'https://img.shopstyle-cdn.com/pim/a4/cb/a4cbcaad922f74d9f3bf9a4a586b20e1_best.jpg', 'id': 687703189, 'name': 'Foxiedox Cosimia Burnout Velvet Midi Dress'}, {'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=683000134&pid=uid2384-40566372-99', 'price': '$73', 'image_url': 'https://img.shopstyle-cdn.com/pim/bc/6c/bc6cc5dd97703aafa2a91736b00d92a0_best.jpg', 'id': 683000134, 'name': 'Anama Open Back Midi Dress'}]

        ClarifaiResults = _mock_ClarifaiResults
        ShopStyleResults = _mock_ShopStyleResults


    def test_ShopStyle_Retry(self): # test_ShopStyle_Retry() takes exactly 3 arguments (1 given) error -- check back on this
        """Check if shopstyle retry returns results if length of results != 0"""
        self.assertEqual(ShopStyle_Retry(['women','midi','kimono'], 'Gray','Small'), [{'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=687703189&pid=uid2384-40566372-99', 'price': '$180', 'image_url': 'https://img.shopstyle-cdn.com/pim/a4/cb/a4cbcaad922f74d9f3bf9a4a586b20e1_best.jpg', 'id': 687703189, 'name': 'Foxiedox Cosimia Burnout Velvet Midi Dress'}, {'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=683000134&pid=uid2384-40566372-99', 'price': '$73', 'image_url': 'https://img.shopstyle-cdn.com/pim/bc/6c/bc6cc5dd97703aafa2a91736b00d92a0_best.jpg', 'id': 683000134, 'name': 'Anama Open Back Midi Dress'}])


"""Flask integration tests to test log in, log out, and session logic"""

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self): # is setUp and tearDown part of the test framework
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_user_search(self):
        """Test search images / pins page - for all users (logged in & logged out)"""

        result = self.client.get("/search") 
        self.assertIn("Search by Image URL", result.data)

    def test_show_results(self): #ERROR
        """Test ShopStyle results page."""
        #results = "[{'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=687703189&pid=uid2384-40566372-99', 'price': '$180', 'image_url': 'https://img.shopstyle-cdn.com/pim/a4/cb/a4cbcaad922f74d9f3bf9a4a586b20e1_best.jpg', 'id': 687703189, 'name': 'Foxiedox Cosimia Burnout Velvet Midi Dress'}, {'url': 'https://api.shopstyle.com/action/apiVisitRetailer?id=683000134&pid=uid2384-40566372-99', 'price': '$73', 'image_url': 'https://img.shopstyle-cdn.com/pim/bc/6c/bc6cc5dd97703aafa2a91736b00d92a0_best.jpg', 'id': 683000134, 'name': 'Anama Open Back Midi Dress'}]"
        result = self.client.get("/results?results=%5B%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698366465%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24241%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F58%2F93%2F589376167053d9d293cbfed0a955b3e9_best.jpg%22%2C+%22id%22%3A+698366465%2C+%22name%22%3A+%22WEEKEND+MAX+MARA+Pepli+skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D656266677%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24111%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F59%2Ff3%2F59f354d25d13247d8c3a7b2d87e9d00d_best.jpg%22%2C+%22id%22%3A+656266677%2C+%22name%22%3A+%22Lace+and+Beads+Lace+%26+Beads+Tierred+Tulle+Skirt+With+Embellished+Waistband%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D612286827%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2451%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F30%2Fa9%2F30a9a2677ff94622fa23ff10dbe98b71_best.jpg%22%2C+%22id%22%3A+612286827%2C+%22name%22%3A+%22boohoo+Boutique+Lola+Thigh+Split+Sequin+Maxi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D693704164%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24745%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F13%2F7a%2F137aab8bffe864861c2487f2849e4f94_best.jpg%22%2C+%22id%22%3A+693704164%2C+%22name%22%3A+%22Marc+Jacobs+Sequined+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D619673906%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24151%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F19%2Fd5%2F19d55fa2adcc69973d971a2109bf3ea0_best.jpg%22%2C+%22id%22%3A+619673906%2C+%22name%22%3A+%22Lovedrobe+Luxe+Cap+Sleeve+Floral+Embellished+Dress+With+Tulle+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D622877964%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2488%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fc3%2Fdf%2Fc3dfc11f9e227347a14ea3e606365107_best.jpg%22%2C+%22id%22%3A+622877964%2C+%22name%22%3A+%22Dance+%26+Marvel+Silver+Fox+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D535496972%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2489%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fb0%2Fc8%2Fb0c87392310a8da784d6215771c3c3e7_best.jpg%22%2C+%22id%22%3A+535496972%2C+%22name%22%3A+%22Truly+You+Embellished+Midi+Skirt+Co-Ord%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D663844092%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C175%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F33%2F39%2F33392110223ec43b0475469a6de0e2a2_best.jpg%22%2C+%22id%22%3A+663844092%2C+%22name%22%3A+%22Marc+Jacobs+Sequin+Silk+Skirt+w%2F+Tags%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D657428339%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24135%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F95%2F1c%2F951c1f8f56ee6cc94b608d88bc32514c_best.jpg%22%2C+%22id%22%3A+657428339%2C+%22name%22%3A+%22Maya+Plus+Cap+Sleeve+V+Neck+Midi+Dress+With+Tonal+Delicate+Sequins%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698047894%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2417.99%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fad%2F1e%2Fad1ebd1edd3f1d5bcb4d1c3149a74171_best.jpg%22%2C+%22id%22%3A+698047894%2C+%22name%22%3A+%22A+New+Day+Women%27s+Short+Sleeve+Sequin+T-Shirt+-+A+New+Day+Light+Heather+Gray%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698253561%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C595%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F21%2Fb8%2F21b8909bff57575683e45914c2dc5bf9_best.jpg%22%2C+%22id%22%3A+698253561%2C+%22name%22%3A+%22St.+John+Collection+Sequin+Knit+Midi+Dress%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D683805926%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2475%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F83%2F5a%2F835a69e3e58ff53913159b1545af21a7_best.jpg%22%2C+%22id%22%3A+683805926%2C+%22name%22%3A+%22Elizabeth+and+James+Floral+Print+Sleeveless+Dress%22%7D%5D")
        self.assertIn("PinShop Results", result.data)

    # def test_login(self): # ERROR -- MESSAGE CLASS TO SEE WHO HAS DONE THIS PROPERLY
    #     """Test login page."""

    #     result = self.client.post("/login",
    #                               data={email":"ann@test.com", "password": "123"}, #invalid salt?
    #                               follow_redirects=True)
    #     self.assertIn("Bookmarks", result.data) # can flash messages be used here


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session -- scenario with no pinterest username provided"""
    
    def tearDown(self): # is setUp and tearDown part of the test framework
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def setUp(self):
        """Stuff to do before every test."""
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_user_search_1(self): #ERROR WITH CREATIN TEST DB; "relation "users" does not exist"
        """Test user search for logged in user (no pinterest username provided)"""

        result = self.client.get("/search")
        self.assertIn("Bookmarks", result.data) # may need to find higher fidelity keyword; can we check "Logged In flash message?"
        self.assertNotIn("Search your pins", result.data)

    def test_show_results(self): #ERROR -- should be fixed
        """Test ShopStyle results page for logged in users; only logged in users can save items"""

        result = self.client.get("/results?results=%5B%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698366465%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24241%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F58%2F93%2F589376167053d9d293cbfed0a955b3e9_best.jpg%22%2C+%22id%22%3A+698366465%2C+%22name%22%3A+%22WEEKEND+MAX+MARA+Pepli+skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D656266677%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24111%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F59%2Ff3%2F59f354d25d13247d8c3a7b2d87e9d00d_best.jpg%22%2C+%22id%22%3A+656266677%2C+%22name%22%3A+%22Lace+and+Beads+Lace+%26+Beads+Tierred+Tulle+Skirt+With+Embellished+Waistband%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D612286827%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2451%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F30%2Fa9%2F30a9a2677ff94622fa23ff10dbe98b71_best.jpg%22%2C+%22id%22%3A+612286827%2C+%22name%22%3A+%22boohoo+Boutique+Lola+Thigh+Split+Sequin+Maxi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D693704164%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24745%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F13%2F7a%2F137aab8bffe864861c2487f2849e4f94_best.jpg%22%2C+%22id%22%3A+693704164%2C+%22name%22%3A+%22Marc+Jacobs+Sequined+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D619673906%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24151%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F19%2Fd5%2F19d55fa2adcc69973d971a2109bf3ea0_best.jpg%22%2C+%22id%22%3A+619673906%2C+%22name%22%3A+%22Lovedrobe+Luxe+Cap+Sleeve+Floral+Embellished+Dress+With+Tulle+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D622877964%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2488%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fc3%2Fdf%2Fc3dfc11f9e227347a14ea3e606365107_best.jpg%22%2C+%22id%22%3A+622877964%2C+%22name%22%3A+%22Dance+%26+Marvel+Silver+Fox+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D535496972%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2489%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fb0%2Fc8%2Fb0c87392310a8da784d6215771c3c3e7_best.jpg%22%2C+%22id%22%3A+535496972%2C+%22name%22%3A+%22Truly+You+Embellished+Midi+Skirt+Co-Ord%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D663844092%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C175%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F33%2F39%2F33392110223ec43b0475469a6de0e2a2_best.jpg%22%2C+%22id%22%3A+663844092%2C+%22name%22%3A+%22Marc+Jacobs+Sequin+Silk+Skirt+w%2F+Tags%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D657428339%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24135%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F95%2F1c%2F951c1f8f56ee6cc94b608d88bc32514c_best.jpg%22%2C+%22id%22%3A+657428339%2C+%22name%22%3A+%22Maya+Plus+Cap+Sleeve+V+Neck+Midi+Dress+With+Tonal+Delicate+Sequins%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698047894%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2417.99%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fad%2F1e%2Fad1ebd1edd3f1d5bcb4d1c3149a74171_best.jpg%22%2C+%22id%22%3A+698047894%2C+%22name%22%3A+%22A+New+Day+Women%27s+Short+Sleeve+Sequin+T-Shirt+-+A+New+Day+Light+Heather+Gray%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698253561%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C595%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F21%2Fb8%2F21b8909bff57575683e45914c2dc5bf9_best.jpg%22%2C+%22id%22%3A+698253561%2C+%22name%22%3A+%22St.+John+Collection+Sequin+Knit+Midi+Dress%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D683805926%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2475%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F83%2F5a%2F835a69e3e58ff53913159b1545af21a7_best.jpg%22%2C+%22id%22%3A+683805926%2C+%22name%22%3A+%22Elizabeth+and+James+Floral+Print+Sleeveless+Dress%22%7D%5D")
        self.assertIn("Save", result.data)

    def test_view_bookmarks(self): #ERROR
        """Test bookmark viewing page for logged in users"""

        result = self.client.get("/bookmarks")
        self.assertIn("Bookmarks", result.data)

class FlaskTestsLoggedIn_withPin(TestCase):
    """Flask tests with user logged in to session -- scenario WITH pinterest username provided"""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2


        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_user_search_2(self): #ERROR WITH CREATIN TEST DB; "relation "users" does not exist"
        """Test user search for logged in user with pinterest username"""

        result = self.client.get("/search")
        self.assertIn("Bookmarks", result.data) # may need to find higher fidelity keyword; can we check "Logged In flash message?"
        self.assertNotIn("Filter by specific board", result.data)

    def test_show_results_2(self): #ERROR -- should be fixed
        """Test ShopStyle results page for logged in users; only logged in users can save items"""
            
        result = self.client.get("/results?results=%5B%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698366465%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24241%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F58%2F93%2F589376167053d9d293cbfed0a955b3e9_best.jpg%22%2C+%22id%22%3A+698366465%2C+%22name%22%3A+%22WEEKEND+MAX+MARA+Pepli+skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D656266677%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24111%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F59%2Ff3%2F59f354d25d13247d8c3a7b2d87e9d00d_best.jpg%22%2C+%22id%22%3A+656266677%2C+%22name%22%3A+%22Lace+and+Beads+Lace+%26+Beads+Tierred+Tulle+Skirt+With+Embellished+Waistband%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D612286827%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2451%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F30%2Fa9%2F30a9a2677ff94622fa23ff10dbe98b71_best.jpg%22%2C+%22id%22%3A+612286827%2C+%22name%22%3A+%22boohoo+Boutique+Lola+Thigh+Split+Sequin+Maxi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D693704164%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24745%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F13%2F7a%2F137aab8bffe864861c2487f2849e4f94_best.jpg%22%2C+%22id%22%3A+693704164%2C+%22name%22%3A+%22Marc+Jacobs+Sequined+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D619673906%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24151%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F19%2Fd5%2F19d55fa2adcc69973d971a2109bf3ea0_best.jpg%22%2C+%22id%22%3A+619673906%2C+%22name%22%3A+%22Lovedrobe+Luxe+Cap+Sleeve+Floral+Embellished+Dress+With+Tulle+Midi+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D622877964%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2488%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fc3%2Fdf%2Fc3dfc11f9e227347a14ea3e606365107_best.jpg%22%2C+%22id%22%3A+622877964%2C+%22name%22%3A+%22Dance+%26+Marvel+Silver+Fox+Skirt%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D535496972%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2489%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fb0%2Fc8%2Fb0c87392310a8da784d6215771c3c3e7_best.jpg%22%2C+%22id%22%3A+535496972%2C+%22name%22%3A+%22Truly+You+Embellished+Midi+Skirt+Co-Ord%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D663844092%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C175%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F33%2F39%2F33392110223ec43b0475469a6de0e2a2_best.jpg%22%2C+%22id%22%3A+663844092%2C+%22name%22%3A+%22Marc+Jacobs+Sequin+Silk+Skirt+w%2F+Tags%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D657428339%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%24135%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F95%2F1c%2F951c1f8f56ee6cc94b608d88bc32514c_best.jpg%22%2C+%22id%22%3A+657428339%2C+%22name%22%3A+%22Maya+Plus+Cap+Sleeve+V+Neck+Midi+Dress+With+Tonal+Delicate+Sequins%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698047894%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2417.99%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2Fad%2F1e%2Fad1ebd1edd3f1d5bcb4d1c3149a74171_best.jpg%22%2C+%22id%22%3A+698047894%2C+%22name%22%3A+%22A+New+Day+Women%27s+Short+Sleeve+Sequin+T-Shirt+-+A+New+Day+Light+Heather+Gray%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D698253561%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%241%2C595%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F21%2Fb8%2F21b8909bff57575683e45914c2dc5bf9_best.jpg%22%2C+%22id%22%3A+698253561%2C+%22name%22%3A+%22St.+John+Collection+Sequin+Knit+Midi+Dress%22%7D%2C+%7B%22url%22%3A+%22https%3A%2F%2Fapi.shopstyle.com%2Faction%2FapiVisitRetailer%3Fid%3D683805926%26pid%3Duid2384-40566372-99%22%2C+%22price%22%3A+%22%2475%22%2C+%22image_url%22%3A+%22https%3A%2F%2Fimg.shopstyle-cdn.com%2Fpim%2F83%2F5a%2F835a69e3e58ff53913159b1545af21a7_best.jpg%22%2C+%22id%22%3A+683805926%2C+%22name%22%3A+%22Elizabeth+and+James+Floral+Print+Sleeveless+Dress%22%7D%5D")
        self.assertIn("Save", result.data)

    def test_view_bookmarks(self): #ERROR -- not sure if 148-154 tests are needed since already tested in first user login flow
        """Test bookmark viewing page for logged in users"""

        result = self.client.get("/bookmarks")
        self.assertIn("Bookmarks", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged out of session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_user_search(self):
        """Test that user can't see important page when logged out."""

        result = self.client.get("/search")
        self.assertNotIn("Search your pins", result.data)
        self.assertIn("Search sample pins", result.data)



































if __name__ == '__main__':
    # If called like a script, run our tests
    import unittest
    unittest.main()
