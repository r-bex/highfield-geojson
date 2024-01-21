import json
import os
import sys

# TODO: process featurecollections properly with shapely etc
# TODO: process features in order polygon -> line -> point

POLYGON_STYLE = " ".join([
    "fillColor=\"#f3c285\"",
    "color=\"#f3b261\"", # border colour
    "fillOpacity=\"0.8\""
])

LINE_STYLE = " ".join([
    "weight=\"8\"",
    "color=\"#5190f7\"",
    "opacity=\"0.8\""
])

POINT_STYLE = " ".join([
    "color=\"#fc4933\"",
    "fillOpacity=\"0.8\"",
])

STYLES = {
    "Polygon": POLYGON_STYLE,
    "LineString": LINE_STYLE,
    "Point": POINT_STYLE,
}

def extract_features(path):
    with open(path) as f:
        obj = json.load(f)

    try:
        return obj["features"]
    except:
        raise Exception("Couldn't extract features from %s", path)
    
def convert_coords_to_latlngs(feature):
    coords = feature["geometry"]["coordinates"][0]
    return "; ".join(f"{lat}, {lng}" for [lng, lat] in coords)
    
def generate_feature_shortcode(feature):
    geometry_type = feature["geometry"]["type"]
    if geometry_type == "Point":
        [lng, lat] = feature["geometry"]["coordinates"]
        return f"[leaflet-circle lat={lat} lng={lng} radius=10 {STYLES[geometry_type]}]"
    
    # polygon and line share same shortcode format, different to circle
    if geometry_type == "Polygon":
        leaflet_type = "polygon"
    elif geometry_type == "LineString":
        leaflet_type = "line"
    else:
        raise Exception("Feature type %s not supported", geometry_type)
    
    return f"[leaflet-{leaflet_type} latlngs=\"{convert_coords_to_latlngs(feature)}\" {STYLES[geometry_type]}]"

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        paths = [filename]
    except:
        # no specific file passed, process all
        paths = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".geojson")]
    
    feature_shortcodes = [
        generate_feature_shortcode(feature)
        for path in paths
        for feature in extract_features(path)
    ]
    feature_shortcodes.insert(0, "[leaflet-map fitbounds]")
    print("\n".join(feature_shortcodes))

