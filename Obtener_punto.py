import geopandas as gpd
import fiona
import random
from shapely.geometry import Point

# Path to the GeoPackage
gpkg_path = './carpeta_stacks/muestras_training.gpkg'

n_points_per_polygon = 100 # Number of random points to generate per polygon

# List all polygon layers (assumes they start with 'poly_YYYY-MM-DD')
polygon_layers = [layer for layer in fiona.listlayers(gpkg_path) 
                  if layer.startswith('poly_')]

for poly_layer in polygon_layers:
    print(f"Processing polygon layer: {poly_layer}")
    
    # Load the polygon layer
    polys = gpd.read_file(gpkg_path, layer=poly_layer)
    
    # Container for generated points
    samples = []
    # Extract date from the layer name (after 'poly_')
    date_str = poly_layer.split('poly_')[1]
    
    # For each polygon, generate random points inside it
    for _, row in polys.iterrows():
        bbox = row.geometry.bounds  # (minx, miny, maxx, maxy)
        label = row['label']
        count = 0
        while count < n_points_per_polygon:
            x = random.uniform(bbox[0], bbox[2])
            y = random.uniform(bbox[1], bbox[3])
            p = Point(x, y)
            if row.geometry.contains(p):
                samples.append({
                    'geometry': p,
                    'label': label,
                    'date': date_str
                })
                count += 1
    
    # Build a GeoDataFrame of the points
    pts_gdf = gpd.GeoDataFrame(samples, crs=polys.crs)
    
    # Write the points to a new layer named 'pts_YYYY-MM-DD'
    pts_layer = f"pts_{date_str}"
    pts_gdf.to_file(gpkg_path, layer=pts_layer, driver='GPKG')
    print(f"Saved {len(pts_gdf)} points to layer '{pts_layer}'\n")
