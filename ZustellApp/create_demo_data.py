"""
Demo script to populate the database with sample packages
"""
from database import Database
from geocoding import Geocoder
import time

def create_demo_data():
    """Create sample packages for testing"""
    db = Database()
    geocoder = Geocoder()
    
    # Sample addresses in Vienna, Austria
    sample_addresses = [
        "Stephansplatz 1, 1010 Wien, Österreich",
        "Mariahilfer Straße 1, 1060 Wien, Österreich",
        "Prater 1, 1020 Wien, Österreich",
        "Schönbrunner Schlossstraße 47, 1130 Wien, Österreich",
        "Rathausplatz 1, 1010 Wien, Österreich",
        "Naschmarkt 1, 1060 Wien, Österreich",
        "Donauinsel, 1220 Wien, Österreich",
    ]
    
    print("Creating demo packages...")
    
    for i, address in enumerate(sample_addresses):
        # Add package to database
        pkg_type = "package" if i % 2 == 0 else "letter"
        notes = f"Demo {pkg_type} #{i+1}"
        
        pkg_id = db.add_package(address, type=pkg_type, notes=notes)
        print(f"Added package {pkg_id}: {address}")
        
        # Geocode the address
        print(f"  Geocoding...")
        coords = geocoder.geocode(address)
        
        if coords:
            lat, lon = coords
            db.update_package_coordinates(pkg_id, lat, lon)
            print(f"  ✓ Geocoded: ({lat:.6f}, {lon:.6f})")
        else:
            print(f"  ✗ Geocoding failed")
        
        # Be nice to the API
        time.sleep(1)
    
    # Add some address notes
    db.add_address_note("Stephansplatz 1, 1010 Wien, Österreich", "Haupteingang verwenden")
    db.add_address_note("Mariahilfer Straße 1, 1060 Wien, Österreich", "Klingel defekt, anrufen")
    
    db.close()
    
    print("\n✓ Demo data created successfully!")
    print("You can now run the app with: python main.py")

if __name__ == "__main__":
    create_demo_data()
