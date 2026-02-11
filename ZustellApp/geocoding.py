"""
Geocoding module for converting addresses to coordinates
"""
import requests
from typing import Tuple, Optional

class Geocoder:
    """Geocode addresses using Nominatim (OpenStreetMap)"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'ZustellApp/1.0'
        }
    
    def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert an address to coordinates (latitude, longitude)
        
        Args:
            address: The address string to geocode
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
            
            return None
            
        except Exception as e:
            print(f"Geocoding error for '{address}': {e}")
            return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """
        Convert coordinates to an address
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Address string or None if not found
        """
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            if 'display_name' in data:
                return data['display_name']
            
            return None
            
        except Exception as e:
            print(f"Reverse geocoding error for ({lat}, {lon}): {e}")
            return None
