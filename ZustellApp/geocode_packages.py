"""
Helper script to geocode all packages in the database
"""
from database import Database
from geocoding import Geocoder
import time

def geocode_all_packages():
    """Geocode all packages that don't have coordinates yet"""
    db = Database()
    geocoder = Geocoder()
    
    # Get all packages
    packages = db.get_packages()
    
    geocoded_count = 0
    failed_count = 0
    
    for pkg in packages:
        pkg_id, address, status, pkg_type, notes, lat, lon, timestamp = pkg
        
        # Skip if already geocoded
        if lat is not None and lon is not None:
            print(f"Package {pkg_id} already geocoded: {address}")
            continue
        
        print(f"Geocoding package {pkg_id}: {address}")
        
        # Geocode the address
        coords = geocoder.geocode(address)
        
        if coords:
            lat, lon = coords
            db.update_package_coordinates(pkg_id, lat, lon)
            print(f"  ✓ Success: ({lat}, {lon})")
            geocoded_count += 1
        else:
            print(f"  ✗ Failed to geocode")
            failed_count += 1
        
        # Be nice to the API - add a small delay
        time.sleep(1)
    
    db.close()
    
    print(f"\nGeocoding complete!")
    print(f"Successfully geocoded: {geocoded_count}")
    print(f"Failed: {failed_count}")

if __name__ == "__main__":
    geocode_all_packages()
