# This module handles user authentication using Google OAuth.
# Instead of local registration and login, we only allow users to authenticate with their Google account.
# The client will send an 'id_token' obtained from Google Sign-In to this endpoint for verification.
# Upon successful verification, the system either creates a new user (if not already registered)
# or retrieves the existing user, then generates a JWT token for secure access.

from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

# Create a blueprint for authentication endpoints.
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    """
    Authenticate a user using Google OAuth.

    Workflow:
      1. Extract the 'id_token' from the JSON payload sent by the client.
      2. Retrieve the Google Client ID from environment variables.
      3. Verify the provided id_token with Google's OAuth2 services.
      4. Extract the user's email from the verified token payload.
      5. Check if the user exists in our database (using email as the unique identifier).
         - If not, create a new user record.
      6. Generate a JWT access token for the authenticated user.
      7. Return the JWT token and user information.

    Expects:
      {
         "id_token": "<Google_ID_token_here>"
      }
    """
    # Parse the incoming JSON payload.
    data = request.get_json()
    token = data.get('id_token')
    
    # Ensure the token was provided.
    if not token:
        return jsonify({'error': 'id_token is required'}), 400

    # Retrieve Google client ID from environment variables.
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', None)
    if not google_client_id:
        return jsonify({'error': 'Google Client ID is not configured'}), 500

    try:
        # Verify the token using Google's verification service.
        # The verify_oauth2_token method will ensure the token's integrity,
        # check its audience (against the provided client ID) and expiration.
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), google_client_id)
    except ValueError:
        # If token verification fails, return an error.
        return jsonify({'error': 'Invalid id_token'}), 401

    # Extract the user's email from the token payload. Google includes the email if requested.
    email = id_info.get('email')
    if not email:
        return jsonify({'error': 'Email not available in token'}), 400

    # Check if a user with this email exists in our database.
    # For simplicity, we are using the 'username' field to store the email.
    user = User.query.filter_by(username=email).first()
    if not user:
        # If the user does not exist, create a new user record.
        user = User(username=email)
        db.session.add(user)
        db.session.commit()

    # Generate a JWT access token. The token's identity is set to the user's ID.
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user': user.as_dict()}), 200
