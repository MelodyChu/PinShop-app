"""Models and database functions for PinShop app project."""

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

#####################################################################
# Model definitions

class User(db.Model):
    """User of PinShop app; likely to implement user functionality fully in v2. For now, pin token is pin username"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False) #PW hashed
    gender = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True) # can consider storing as strings
    size = db.Column(db.String(64), nullable=True) #selector for XS, small, medium, large
    pant_size = db.Column(db.Integer, nullable=True) #in inches; may be an extra column
    shoe_size = db.Column(db.Float, nullable=True) #US shoe sizes
    pinterest_token = db.Column(db.String(100), nullable=True) #REPURPOSE to be pinterest username

    bookmarks = db.relationship('Bookmark') #relationship to bookmark

  
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id,
                                               self.email)



class Bookmark(db.Model): #rename to bookmarks intermediary table / association
    """Table of all user *saved* listings returned by Etsy"""

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
   
    etsy_listing_id = db.Column(db.Integer, db.ForeignKey('etsyresults.etsy_listing_id'), nullable=False) #list of listings saved

    user = db.relationship('User') #edit
    etsyresult = db.relationship('EtsyResult') #edit CHANGE THIS TO ETSY_RESULT

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Bookmark bookmark_id={} etsy_listing_id={}".format(self.bookmark_id,
                                                            self.etsy_listing_id)

class EtsyResult(db.Model): #rename to bookmarks intermediary table / association
    """Table of all Etsy items saved; will not have duplicate listings/items"""

    __tablename__ = "etsyresults"

    etsy_listing_id = db.Column(db.Integer, primary_key=True) #not auto incrementing; Etsy provides unique primary keys
    # db.ForeignKey('bookmarks.etsy_listing_id')

    listing_title = db.Column(db.String(2000), nullable=False)

    listing_url = db.Column(db.String(2000), nullable=False)
    listing_image = db.Column(db.String(2000), nullable=False) #image URL of etsy image
    listing_price = db.Column(db.Float, nullable=True)


    bookmarks = db.relationship('Bookmark') 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Etsy etsy_listing_id={} listing_title={}".format(self.etsy_listing_id, self.listing_title)


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    #User.query.delete()

    ann = User(email='ann@test.com', password='123', gender='Female', age=25, size='Small', pant_size=26, shoe_size=6) 
    bo = User(email='bo@test.com', password='456', gender='Female', age=20, size='Medium', pant_size=28, shoe_size=7, pinterest_token='booboo') 


    db.session.add_all([ann,bo])
    db.session.commit()

#####################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///pintest'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pintest'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
