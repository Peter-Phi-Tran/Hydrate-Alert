import streamlit as st
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import json
import os

# Google OAuth Configuration
# You'll need to set these up in Google Cloud Console
GOOGLE_CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID", "your-client-id.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", "your-client-secret")
REDIRECT_URI = "http://localhost:8501"

class GoogleAuth:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
                "issuer": "https://accounts.google.com",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
            }
        }
        
    def get_authorization_url(self):
        """Generate Google OAuth authorization URL"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=[
                'openid',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'
            ],
            redirect_uri=REDIRECT_URI
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return auth_url
    
    def verify_token(self, token):
        """Verify Google OAuth token and return user info"""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                google.auth.transport.requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            # Extract user information
            user_info = {
                'email': idinfo.get('email'),
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture'),
                'verified_email': idinfo.get('email_verified', False)
            }
            
            return user_info
            
        except ValueError as e:
            st.error(f"Token verification failed: {e}")
            return None
    
    def authenticate_user(self, authorization_code):
        """Exchange authorization code for user information"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=[
                    'openid',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email'
                ],
                redirect_uri=REDIRECT_URI
            )
            
            # Exchange authorization code for access token
            flow.fetch_token(code=authorization_code)
            
            # Get user info using the access token instead of ID token
            credentials = flow.credentials
            
            # Use the access token to get user info from Google's API
            import requests
            
            # Get user info from Google's userinfo endpoint
            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {credentials.token}'}
            )
            
            if user_info_response.status_code == 200:
                user_data = user_info_response.json()
                
                user_info = {
                    'email': user_data.get('email'),
                    'name': user_data.get('name'),
                    'picture': user_data.get('picture'),
                    'verified_email': user_data.get('verified_email', False)
                }
                
                return user_info
            else:
                st.error(f"Failed to get user info: {user_info_response.status_code}")
                return None
            
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            # Clear query params to prevent repeated errors
            st.query_params.clear()
            return None

def is_google_auth_configured():
    """Check if Google OAuth is properly configured"""
    return (
        GOOGLE_CLIENT_ID != "your-client-id.apps.googleusercontent.com" and
        GOOGLE_CLIENT_SECRET != "your-client-secret" and
        GOOGLE_CLIENT_ID and
        GOOGLE_CLIENT_SECRET
    )
