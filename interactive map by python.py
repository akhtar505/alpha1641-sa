import folium
import geopandas as gpd
import random

# Create a map centered at a specific location
mymap = folium.Map(location=[34.71357797744717, -86.75053781986492], zoom_start=10)

# Add a marker to the map
folium.Marker([34.71357797744717, -86.75053781986492], popup='Madison').add_to(mymap)

# Specify the path to your shapefiles
shapefile_paths = ['E:/test/aaa/al_madison.shp']

# Read the shapefile using GeoPandas
gdf = gpd.read_file(shapefile_paths[0])

# Get unique zone codes
unique_zone_codes = gdf['zone_code'].unique()

# Define a color map for zone codes
zone_color_map = {zone_code: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for zone_code in unique_zone_codes}

# Define a style function to assign random colors based on zone code
def style_function(feature):
    zone_code = feature['properties']['zone_code']
    return {
        'fillColor': zone_color_map.get(zone_code, '#ffffff'),  # Default to white if zone code not found
        'color': '#000000',
        'weight': 2,
        'fillOpacity': 0.5
    }

# Convert GeoDataFrame to GeoJSON
geojson = gdf.__geo_interface__

# Add GeoJSON to map with hover options and assign it to a layer
geojson_layer = folium.GeoJson(
    geojson,
    style_function=style_function,
    tooltip=folium.features.GeoJsonTooltip(fields=['zone_code', 'zone_name'], labels=True, sticky=False)
)

geojson_layer.add_to(mymap)

# Create legend HTML
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; border-radius: 5px; padding: 10px;">
    <p><strong>Zone Code Legend</strong></p>
    {}
</div>
'''

# Add legend items
legend_items_html = ''
for zone_code, color in zone_color_map.items():
    legend_items_html += '<p><span style="background-color: {}; width: 20px; height: 20px; display: inline-block;"></span> {}</p>'.format(color, zone_code)

# Add legend HTML to map
mymap.get_root().html.add_child(folium.Element(legend_html.format(legend_items_html)))

# Add layer control to toggle the GeoJSON layer
folium.LayerControl().add_to(mymap)

# Specify the directory path where you want to save the HTML file
directory_path = 'E:/test/aaa/'

# Save the map to an HTML file in the specified directory
mymap.save(directory_path + 'map_with_legend_and_layer_control.html')
