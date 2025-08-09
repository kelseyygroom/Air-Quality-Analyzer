# Air-Quality-Analyzer


## Overview
A Python tool that finds nearby areas with unhealthy air quality. Utilizes PurpleAir sensor data and Nominatim geocoding.

Given:
* A center location
* Search radius (miles)
* Minimum AQI threshold
* Max # results

It returns the worst air quality locations within that range, sorted by AQI.

## How It Works

1. Geocode center locations -> coordinates (via Nominatim or saved JSON)
2. Get PM2.5 data from PurpleAir API (or local file)
3. Convert PM2.5 to AQI using US standards
4. Filter by distance, AQI threshold and max results
5. Reverse geocode matching points -> readable addresses
6. Output results

## Input Format
This program is run from the command-line. Provide six lines in this order:

```shell
CENTER NOMINATIM <location>   # or CENTER FILE <file>
RANGE <miles>
THRESHOLD <AQI>
MAX <count>
AQI PURPLEAIR                 # or AQI FILE <file>
REVERSE NOMINATIM             # or REVERSE FILES <file1> <file2> ...
```
