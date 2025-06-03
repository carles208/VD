import geopandas as gpd

# Cargar shapefile
gdf = gpd.read_file('TrabajoAcadémico\\datasets')

# (Opcional) Seleccionar columnas necesarias
gdf = gdf[['NAMEUNIT', 'geometry']]
gdf = gdf.rename(columns={'NAMEUNIT': 'Provincia'})

# Convertir CRS a WGS84 para web (requerido por folium)
gdf = gdf.to_crs("EPSG:4326")

# Guardar como GeoJSON
gdf.to_file('TrabajoAcadémico\\datasets\\provincias.geojson', driver='GeoJSON')