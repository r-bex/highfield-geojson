A quick and dirty utility script for generating wordpress shortcodes for the (Leaflet Map wordpress plugin)[https://github.com/bozdoz/wp-plugin-leaflet-map].

## Usage

Running `python main.py` will take all the geojson files in the script's directory and print out the needed shortcodes including one for the map.

e.g. if you have two geojson files, one with a polygon and a point, and one with a line, you might expect output like this...

```
[leaflet-map fitbounds]
[leaflet-polygon latlngs="...]
[leaflet-circle ...]
[leaflet-line latlngs="..."]
```

Supported types:
* Polygon -> leaflet-polygon
* LineString -> leaflet-line
* Point -> leaflet-circle

To generate the geojson I recommend using https://geojson.io, then saving the resulting geojson into a file in this directory.

## Caveats

This script currently expects a valid geojson file path as the only argument and expects that geojson to be a feature collection. Each feature needs a minimum of one set of coordinates, with any more than one being ignored.

It ignores all styling provided. Basic styling is hardcoded per supported feature type.

This was hastily written for personal use so please don't shout at me.