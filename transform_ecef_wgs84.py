#!/usr/bin/env python 

"""
PROGRAM DESCRIPTION:
This script provides a utility for bidirectional conversion between Geodetic 
coordinates (Latitude, Longitude, Altitude - LLA) and Cartesian coordinates 
(Earth-Centered, Earth-Fixed - ECEF). 

It utilizes the WGS84 (World Geodetic System 1984) ellipsoid model, which is 
the standard for GPS and ETRS89. The conversion from ECEF to LLA is implemented 
using Bowring's algorithm, a highly accurate closed-form solution that avoids 
the need for iterative approximations. 

The script features an automatic input detection logic: if the provided 
arguments fall within valid geographic ranges (Latitude ±90°, Longitude ±180°), 
it performs an LLA-to-ECEF conversion. Otherwise, it treats the inputs as 
ECEF coordinates and converts them to LLA.
"""

import math
import sys

class GNSSConverter:
    def __init__(self):
        """
        Initializes the WGS84 ellipsoid parameters.
        Initialisiert die Parameter des WGS84-Ellipsoids.
        """
        # Semi-major axis (equatorial radius in meters)
        # Große Halbachse (Äquatorradius in Metern)
        self.a = 6378137.0 
        
        # Flattening of the Earth (Reciprocal)
        # Abplattung der Erde (Kehrwert)
        self.f = 1 / 298.257223563 
        
        # Semi-minor axis (polar radius)
        # Kleine Halbachse (Polradius)
        self.b = self.a * (1 - self.f) 
        
        # First numerical eccentricity squared: e² = (a² - b²) / a²
        # Erste numerische Exzentrizität im Quadrat: e² = (a² - b²) / a²
        self.e2 = (self.a**2 - self.b**2) / self.a**2
        
        # Second numerical eccentricity squared: e'² = (a² - b²) / b²
        # Zweite numerische Exzentrizität im Quadrat: e'² = (a² - b²) / b²
        self.ep2 = (self.a**2 - self.b**2) / self.b**2

    def ecef_to_lla(self, x, y, z):
        """
        Converts ECEF (X, Y, Z) to Geodetic (Lat, Lon, Alt) using Bowring's algorithm.
        Konvertiert ECEF (X, Y, Z) in geodätische Koordinaten (Breite, Länge, Höhe) 
        mittels Bowring-Algorithmus.
        """
        # Distance from the Z-axis (rotation axis of the Earth)
        # Abstand von der Z-Achse (Rotationsachse der Erde)
        p = math.sqrt(x**2 + y**2)
        
        # Special case: The poles (X and Y are near zero)
        # Sonderfall: Die Pole (X und Y sind dort nahezu Null)
        if p < 1e-10:
            # Latitude is 90° (North) or -90° (South)
            # Breitengrad ist 90° (Nord) oder -90° (Süd)
            lat = math.pi/2 if z > 0 else -math.pi/2
            lon = 0 # Longitude is undefined at the poles; set to 0
            alt = abs(z) - self.b
        else:
            # Auxiliary angle for Bowring's calculation
            # Hilfswinkel für die Berechnung nach Bowring
            th = math.atan2(self.a * z, self.b * p)
            
            # Longitude: Simple angle in the XY plane
            # Längengrad: Einfacher Winkel in der XY-Ebene
            lon = math.atan2(y, x)
            
            # Latitude: Accounts for Earth's curvature/flattening
            # Breitengrad: Berücksichtigt die Erdkrümmung/Abplattung
            lat = math.atan2(z + self.ep2 * self.b * (math.sin(th)**3), 
                             p - self.e2 * self.a * (math.cos(th)**3))
            
            # Prime vertical radius of curvature (N)
            # Querkrümmungshalbmesser (N)
            n = self.a / math.sqrt(1 - self.e2 * (math.sin(lat)**2))
            
            # Ellipsoidal height: distance above the theoretical ellipsoid
            # Ellipsoidische Höhe: Abstand über dem theoretischen Ellipsoid
            alt = p / math.cos(lat) - n
            
        return math.degrees(lat), math.degrees(lon), alt

    def lla_to_ecef(self, lat_deg, lon_deg, alt):
        """
        Converts Geodetic (Lat, Lon, Alt) to ECEF (X, Y, Z).
        Konvertiert geodätische Koordinaten (Breite, Länge, Höhe) in ECEF (X, Y, Z).
        """
        # Convert decimal degrees to radians
        # Umrechnung von Dezimalgrad in Bogenmaß (Radiant)
        lat = math.radians(lat_deg)
        lon = math.radians(lon_deg)
        
        # Calculate the prime vertical radius of curvature
        # Querkrümmungshalbmesser berechnen
        n = self.a / math.sqrt(1 - self.e2 * (math.sin(lat)**2))
        
        # Calculation of X, Y, Z components
        # Berechnung der X, Y, Z Komponenten
        x = (n + alt) * math.cos(lat) * math.cos(lon)
        y = (n + alt) * math.cos(lat) * math.sin(lon)
        z = (n * (1 - self.e2) + alt) * math.sin(lat)
        
        return x, y, z

if __name__ == "__main__":
    # Check if exactly 3 arguments (values) were provided
    # Prüfung, ob genau 3 Argumente (Zahlen) übergeben wurden
    if len(sys.argv) != 4:
        print("Usage: transform_ecef_wgs84.py <v1> <v2> <v3>")
        sys.exit(1)

    # Convert arguments from string to floating point numbers
    # Argumente von Text in Fließkommazahlen umwandeln
    try:
        v1, v2, v3 = map(float, sys.argv[1:])
    except ValueError:
        print("Error: Please enter numbers only. ")
        sys.exit(1)

    conv = GNSSConverter()

    # --- Logic for detecting the input type ---
    # --- Logik zur Erkennung des Input-Typs ---
    # Check against physical WGS84 limits:
    # 1. Latitude (v1) must be between -90 and 90
    # 2. Longitude (v2) must be between -180 and 180
    # 3. Altitude (v3) must be plausible (here up to 100km for aviation/UAV)
    
    # Prüfung gegen die physikalischen Grenzen von WGS84:
    # 1. Breitengrad (v1) muss zwischen -90 und 90 liegen
    # 2. Längengrad (v2) muss zwischen -180 und 180 liegen
    # 3. Höhe (v3) muss plausibel sein (hier bis 100km für Luftfahrt/UAV)
    is_lla = abs(v1) <= 90 and abs(v2) <= 180 and abs(v3) <= 100000

    if is_lla:
        # Input is LLA -> Result is X, Y, Z
        # Input ist Breite, Länge, Höhe -> Ergebnis ist X, Y, Z
        res = conv.lla_to_ecef(v1, v2, v3)
        # Output with 4 decimal places (sufficient for 0.1mm precision)
        # Ausgabe mit 4 Nachkommastellen (reicht für 0.1mm Präzision)
        print(f"{res[0]:.4f} {res[1]:.4f} {res[2]:.4f}")
    else:
        # Input is ECEF -> Result is LLA
        # Input ist X, Y, Z -> Ergebnis ist Breite, Länge, Höhe
        res = conv.ecef_to_lla(v1, v2, v3)
        # Output Lat/Lon with 10 decimal places for highest precision
        # Ausgabe Breite/Länge mit 10 Stellen für höchste Präzision
        print(f"{res[0]:.10f} {res[1]:.10f} {res[2]:.4f}")


