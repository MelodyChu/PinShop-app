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
    """User of PinShop app; likely to implement user functionality fully in v2"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False) #ask about adding salt & hash passwords
    age = db.Column(db.Integer, nullable=True) # can consider storing as strings
    size = db.Column(db.String(64), nullable=True) #selector for XS, small, medium, large
    pant_size = db.Column(db.Integer, nullable=True) #in inches; may be an extra column
    shoe_size = db.Column(db.Float, nullable=True) #US shoe sizes
    pinterest_token = db.Column(db.String(100), nullable=True) #check pinterest user token formatting
    # consider adding gender


    # def hash_password(self, password_str): #check decorator methods
    #     self.password = hashlib.sha224(password_str).hexdigest()
    #     return self.password - using bcrypt instead
  
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id,
                                               self.email)

# class ImageSearch(db.Model):
#     """Table of image search queries. One user can only search for 1 image at a time"""

#     __tablename__ = "imagesearches"

#     search_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     user_id = db.Column(db.Integer,
#                          db.ForeignKey('users.user_id'))
#     image_path = db.Column(db.String(150), nullable=False) #need an image path to search

#     user = db.relationship("User", backref=db.backref("imagesearches", 
#                                                       order_by=search_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<ImageSearch search_id={} image_path={}>".format(self.image_id,
#                                                self.image_path)

# class ClarifaiResult(db.Model):
#     """Table of concept results returned from Clarifai Image Predict model"""

#     __tablename__ = "clarifairesults"

#     result_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     search_id = db.Column(db.Integer,
#                          db.ForeignKey('imagesearches.search_id'))

#     imagesearch = db.relationship("ImageSearch", backref=db.backref("clarifairesults", 
#                                                       order_by=result_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Clarifai result_id={} search_id={}>".format(self.result_id,
#                                                self.top_concepts)


class EtsyResult(db.Model):
    """Table of user *saved* listings returned by Etsy - will not be saving all listings returned by Etsy"""

    __tablename__ = "etsyresults"

    etsy_result_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
   
    etsy_listing_id = db.Column(db.Integer, nullable=False) #list of listings saved

    # user = db.relationship("User", backref=db.backref("users", 
    #                                                     order_by=user_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Etsy etsy_result_id={} etsy_listing_ID={}".format(self.etsy_result_id,
                                                            self.etsy_listing_ID)

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pintest'
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
