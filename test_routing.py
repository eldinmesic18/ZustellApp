from ZustellApp.geocoding import Geocoder
from ZustellApp.routing import RouteOptimizer

def test_routing():
    geocoder = Geocoder()
    optimizer = RouteOptimizer()
    
    # Add some dummy addresses (Assumes Internet connection for Geocoding)
    # Using specific landmarks or well-known streets in a city (e.g., Berlin)
    addresses = [
        "Alexanderplatz, Berlin",
        "Brandenburger Tor, Berlin",
        "Potsdamer Platz, Berlin",
        "Checkpoint Charlie, Berlin"
    ]

    print("Geocoding addresses...")
    coords = []
    geocoded_addresses = []
    
    for addr in addresses:
        loc = geocoder.geocode(addr)
        if loc:
            print(f" - {addr}: {loc}")
            coords.append(loc)
            geocoded_addresses.append(addr)
        else:
            print(f" - Failed to geocode {addr}")

    if len(coords) < 2:
        print("Not enough coordinates to optimize route.")
        return

    print("\nOptimizing Route (Nearest Neighbor)...")
    route_indices = optimizer.optimize_route(coords, start_index=0)
    
    print("\nOptimized Order:")
    for i, idx in enumerate(route_indices):
        print(f"{i+1}. {geocoded_addresses[idx]}")
    
    total_dist = optimizer.calculate_route_distance(coords, route_indices)
    print(f"\nTotal estimated distance: {total_dist:.2f} km")

if __name__ == "__main__":
    test_routing()
