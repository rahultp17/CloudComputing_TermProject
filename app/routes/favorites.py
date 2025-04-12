# app/routes/favorites.py
# This file handles API endpoints related to managing a user's favorite locations.
# It uses JWT authentication to ensure that only authenticated users (those providing a valid token)
# can add, view, or remove their favorite locations.

from flask import Blueprint, request, jsonify
from app.models import FavoriteLocation
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a blueprint for favorites-related endpoints.
favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/', methods=['POST'])
@jwt_required()  # Requires a valid JWT token to access this endpoint.
def add_favorite():
    """
    Add a new favorite location for the authenticated user.
    
    Workflow:
      1. Retrieve the user's ID from the JWT token.
      2. Parse the JSON request body to obtain the 'city' value.
      3. Validate that the 'city' field is provided.
      4. Create a new FavoriteLocation record in the database using the user ID and city.
      5. Commit the new record to the database.
      6. Return a success response including the new favorite's details.
    """
    user_id = get_jwt_identity()  # Retrieve the authenticated user's ID from the token.
    data = request.get_json()
    city = data.get('city')
    
    if not city:
        return jsonify({'error': 'City field is required.'}), 400

    favorite = FavoriteLocation(user_id=user_id, city=city)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite location added successfully.', 'favorite': favorite.as_dict()}), 201

@favorites_bp.route('/', methods=['GET'])
@jwt_required()  # Requires a valid JWT token to access this endpoint.
def get_favorites():
    """
    Retrieve all favorite locations for the authenticated user.
    
    Workflow:
      1. Retrieve the user's ID from the JWT token.
      2. Query the database for favorite locations where the user_id matches the authenticated user's ID.
      3. Convert each favorite location record into a dictionary.
      4. Return the list of favorite locations.
    """
    user_id = get_jwt_identity()
    favorites = FavoriteLocation.query.filter_by(user_id=user_id).all()
    favorites_list = [fav.as_dict() for fav in favorites]
    return jsonify(favorites_list)

@favorites_bp.route('/<int:favorite_id>', methods=['DELETE'])
@jwt_required()  # Endpoint requires a valid JWT token to proceed.
def delete_favorite(favorite_id):
    """
    Remove an existing favorite location for the authenticated user.
    
    Workflow:
      1. Retrieve the authenticated user's ID from the JWT token.
      2. Retrieve the favorite location by its ID.
      3. Ensure the favorite location belongs to the authenticated user.
      4. If found and authorized, delete the record from the database.
      5. Return a success or error response based on the outcome.
      
    URL Parameter:
      favorite_id (int): The ID of the favorite location to be removed.
    """
    user_id = get_jwt_identity()  # Retrieve the user's ID from the token.
    
    # Find the favorite location in the database using its ID.
    favorite = FavoriteLocation.query.get(favorite_id)
    
    # Check if the favorite location exists and belongs to the authenticated user.
    if not favorite or favorite.user_id != user_id:
        return jsonify({'error': 'Favorite not found or unauthorized'}), 404
    
    # Remove the favorite location from the database.
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite location removed successfully.'}), 200
