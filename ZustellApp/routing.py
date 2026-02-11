"""
Route optimization module using TSP (Traveling Salesman Problem) solver
"""
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import math

class RouteOptimizer:
    """Optimize delivery routes using various algorithms"""
    
    def __init__(self):
        pass
    
    def calculate_distance_matrix(self, coords):
        """
        Calculate distance matrix between all coordinate pairs
        
        Args:
            coords: List of (lat, lon) tuples
            
        Returns:
            Distance matrix as numpy array
        """
        # Convert to radians for haversine
        coords_rad = np.radians(coords)
        
        # Use haversine distance
        distances = np.zeros((len(coords), len(coords)))
        
        for i in range(len(coords)):
            for j in range(len(coords)):
                if i != j:
                    lat1, lon1 = coords_rad[i]
                    lat2, lon2 = coords_rad[j]
                    
                    dlat = lat2 - lat1
                    dlon = lon2 - lon1
                    
                    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
                    
                    # Earth radius in km
                    R = 6371
                    distances[i][j] = R * c
        
        return distances
    
    def optimize_route(self, coords, start_index=0):
        """
        Optimize route using nearest neighbor algorithm
        
        Args:
            coords: List of (lat, lon) tuples
            start_index: Index of starting location (default 0)
            
        Returns:
            List of indices representing optimized route order
        """
        if not coords or len(coords) < 2:
            return list(range(len(coords)))
        
        # Calculate distance matrix
        dist_matrix = self.calculate_distance_matrix(coords)
        
        # Nearest neighbor algorithm
        n = len(coords)
        unvisited = set(range(n))
        route = [start_index]
        unvisited.remove(start_index)
        current = start_index
        
        while unvisited:
            # Find nearest unvisited location
            nearest = min(unvisited, key=lambda x: dist_matrix[current][x])
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return route
    
    def calculate_route_distance(self, coords, route):
        """
        Calculate total distance of a route
        
        Args:
            coords: List of (lat, lon) tuples
            route: List of indices representing route order
            
        Returns:
            Total distance in km
        """
        if len(route) < 2:
            return 0.0
        
        dist_matrix = self.calculate_distance_matrix(coords)
        total_distance = 0.0
        
        for i in range(len(route) - 1):
            total_distance += dist_matrix[route[i]][route[i+1]]
        
        return total_distance

