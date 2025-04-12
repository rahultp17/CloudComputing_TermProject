# app/models.py
# This file defines the database models using SQLAlchemy for the Weather Application.
# We are using Google account authentication exclusively, so the User model stores the user's email as a unique identifier.
# The FavoriteLocation model links favorite cities to the user via a foreign key relationship.

from .extensions import db

class User(db.Model):
    """
    User model represents an application user authenticated via their Google account.

    Attributes:
        id (int): Primary key identifier.
        email (str): Unique email address of the user obtained from Google OAuth.
        favorites (list): A list of FavoriteLocation records associated with this user.
    """
    __tablename__ = 'users'
    
    # Unique identifier for the user.
    id = db.Column(db.Integer, primary_key=True)
    # Email field: used as the unique identifier for Google-authenticated users.
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Establish a one-to-many relationship with FavoriteLocation.
    favorites = db.relationship('FavoriteLocation', backref='user', lazy=True)
    
    def as_dict(self):
        """
        Convert the User model instance to a dictionary.
        
        Returns:
            dict: A dictionary containing the user's id and email.
        """
        return {"id": self.id, "email": self.email}

class FavoriteLocation(db.Model):
    """
    FavoriteLocation model stores a user's favorite weather search locations.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key linking to a User (references users.id).
        city (str): The name of the city the user has marked as a favorite.
    """
    __tablename__ = 'favorite_locations'
    
    # Unique identifier for the favorite location.
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key linking to the User model; ensures that each favorite is associated with a valid user.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # City name of the favorite location.
    city = db.Column(db.String(50), nullable=False)
    
    def as_dict(self):
        """
        Convert the FavoriteLocation model instance to a dictionary.
        
        Returns:
            dict: A dictionary containing the id, user_id, and city.
        """
        return {"id": self.id, "user_id": self.user_id, "city": self.city}
