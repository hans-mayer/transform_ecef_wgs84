
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

Examples: 

# transform_ecef_wgs84.py -h
Usage: transform_ecef_wgs84.py <v1> <v2> <v3>

# transform_ecef_wgs84.py 48.14928606302 16.28383433228 286.40506914692
4092523.6549 1195484.3519 4728180.7406

# transform_ecef_wgs84.py 4092523.6549 1195484.3519 4728180.7406
48.1492860629 16.2838343330 286.4050

See also some of my experiments with u-blox GNSS receivers 
[Comparison Precise Point Positioning (PPP) and RTK Methods](https://blog.mayer.tv/2026/03/16/Comparison-Precise-Point-Positioning-PPP-Methods.html){:target="_blank"} 


