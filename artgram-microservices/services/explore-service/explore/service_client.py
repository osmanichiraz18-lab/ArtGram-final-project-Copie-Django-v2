"""
Service Client for Inter-Service Communication
This file demonstrates how services communicate with each other using HTTP requests
"""

import requests
import json
from django.conf import settings

class ArtworkServiceClient:
    """Client to communicate with Artwork Service"""
    
    def __init__(self):
        self.base_url = "http://artwork-service:8002/api/artworks/"
    
    def get_all_artworks(self):
        """Get all artworks from artwork service"""
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling artwork service: {e}")
            return None
    
    def get_artwork_by_id(self, artwork_id):
        """Get specific artwork by ID"""
        try:
            response = requests.get(f"{self.base_url}{artwork_id}/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling artwork service: {e}")
            return None
    
    def get_artworks_by_category(self, category):
        """Get artworks filtered by category"""
        try:
            response = requests.get(f"{self.base_url}?category={category}")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling artwork service: {e}")
            return None

class UserServiceClient:
    """Client to communicate with User Service"""
    
    def __init__(self):
        self.base_url = "http://user-service:8001/api/users/"
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            response = requests.get(f"{self.base_url}{user_id}/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling user service: {e}")
            return None
    
    def get_user_profile(self, username):
        """Get user profile by username"""
        try:
            response = requests.get(f"{self.base_url}profile/{username}/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling user service: {e}")
            return None

# Example usage in views.py:
"""
from explore.service_client import ArtworkServiceClient, UserServiceClient

def explore_home_with_api_calls(request):
    artwork_client = ArtworkServiceClient()
    user_client = UserServiceClient()
    
    # Get artworks from artwork service
    artworks = artwork_client.get_all_artworks()
    
    # Enhance artworks with user information
    if artworks:
        for artwork in artworks:
            user_info = user_client.get_user_by_id(artwork['artist'])
            if user_info:
                artwork['artist_name'] = user_info['username']
                artwork['artist_display_name'] = user_info.get('display_name', user_info['username'])
    
    return render(request, 'explore/home.html', {'artworks': artworks})
"""
