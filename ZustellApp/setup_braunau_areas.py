"""
Script to setup Braunau am Inn delivery areas and master routes.
Clears existing delivery data and populates with specific Braunau examples.
"""
from database import Database
from geocoding import Geocoder
import time
import os

def setup_braunau_():
    # Ensure we are in the right directory to find the db
    db = Database("zustellapp.db")
    geocoder = Geocoder()
    
    print("Clearing old delivery data...")
    db.clear_all_data()
    
    # Define Braunau Areas
    areas = {
        "Braunau Stadtplatz": [
            "Stadtplatz 1, 5280 Braunau am Inn",
            "Stadtplatz 10, 5280 Braunau am Inn",
            "Salzburger Vorstadt 1, 5280 Braunau am Inn",
            "Linzer Straße 1, 5280 Braunau am Inn",
        ],
        "Braunau Laab": [
            "Laabstraße 1, 5280 Braunau am Inn",
            "Laabstraße 20, 5280 Braunau am Inn",
            "Friedhofstraße 5, 5280 Braunau am Inn",
        ],
        "Braunau Haselbach": [
            "Haselbachstraße 1, 5280 Braunau am Inn",
            "Haselbachstraße 50, 5280 Braunau am Inn",
            "Industriestraße 1, 5280 Braunau am Inn",
        ]
    }
    
    print("Setting up areas and master routes...")
    for area_name, addresses in areas.items():
        area_id = db.add_delivery_area(area_name)
        print(f"Area: {area_name} (ID: {area_id})")
        
        for i, addr in enumerate(addresses):
            db.add_master_route_entry(area_id, addr, i + 1)
            print(f"  Added master stop {i+1}: {addr}")
            
    # Add initial sample packages in Braunau
    demo_packages = [
        ("Stadtplatz 5, 5280 Braunau am Inn", "Stadtplatz", "Päckchen", "Wichtig"),
        ("Stadtplatz 1, 5280 Braunau am Inn", "Stadtplatz", "Brief", "Eilt"),
        ("Laabstraße 1, 5280 Braunau am Inn", "Laab", "Paket", "Unterschrift"),
        ("Inntalstraße 10, 5280 Braunau am Inn", None, "Paket", "Unbekannter Bereich"),
    ]
    
    print("\nAdding demo packages in Braunau...")
    for addr, area_hint, p_type, notes in demo_packages:
        pkg_id = db.add_package(addr, type=p_type, notes=notes)
        print(f"Added package {pkg_id}: {addr}")
        
        # Geocode
        print(f"  Geocoding {addr}...")
        coords = geocoder.geocode(addr)
        if coords:
            db.update_package_coordinates(pkg_id, coords[0], coords[1])
            print(f"  ✓ Geocoded")
        else:
            print(f"  ✗ Geocoding failed")
        time.sleep(1) # Be nice to API

    db.close()
    print("\n✓ Braunau setup complete!")

if __name__ == "__main__":
    setup_braunau_()
