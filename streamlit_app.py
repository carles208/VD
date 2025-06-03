import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
import json
from streamlit_folium import st_folium
from branca.colormap import linear

# --- Cargar geometría ---
provincias = gpd.read_file('TrabajoAcadémico\\datasets')  # Shapefile o GeoJSON
provincias = provincias.to_crs("EPSG:4326")  # Reproyectar para folium
provincias = provincias[['NAMEUNIT', 'geometry']]
provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})
gdf = gpd.GeoDataFrame(provincias, crs="EPSG:4326")

# --- Cargar y preparar datos de población ---
pob_file_path = 'TrabajoAcadémico\\datasets\\PobHomb.xlsx'
pob_df_raw = pd.read_excel(pob_file_path, sheet_name=0, skiprows=6)
pob_df_raw.columns.values[0] = 'Provincia'
pob_df_raw['Provincia'] = pob_df_raw['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()
pob_df_raw.set_index('Provincia', inplace=True)
pob_df_raw.index = pob_df_raw.index.str[3:]
pob_df_raw.index = pob_df_raw.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)
pob_df_raw.index = pob_df_raw.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

# --- Unir con geometría ---
gdf = gdf.merge(pob_df_raw, on='Provincia', how='left')
gdf.fillna(0, inplace=True)

# --- Simplificar geometría para mejorar velocidad ---
gdf["geometry"] = gdf["geometry"].simplify(200)

# --- Detectar columnas de población ---
data_columns = gdf.select_dtypes(include=['float64', 'int']).columns.tolist()

# --- Interfaz Streamlit ---
st.title("Mapa interactivo de población por provincia")
selected_column = st.selectbox("Selecciona una fecha", data_columns)
st.write(f"Mostrando datos para: **{selected_column}**")

# --- Crear colormap común ---
vmin = gdf[data_columns].min().min()
vmax = gdf[data_columns].max().max()
colormap = linear.viridis.scale(vmin, vmax)
colormap.caption = f"Población ({selected_column})"

# --- Crear mapa base claro y rápido ---
m = folium.Map(location=[40.4, -3.7], zoom_start=6, tiles="CartoDB positron")

# --- Convertir gdf a GeoJSON
geojson_data = json.loads(gdf.to_json())

# --- Añadir capa de provincias
folium.GeoJson(
    geojson_data,
    name="Provincias",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"][selected_column]) if feature["properties"][selected_column] else "#ffffff",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Provincia", selected_column],
        aliases=["Provincia:", "Población:"],
        localize=True
    )
).add_to(m)

# --- Añadir leyenda de color ---
colormap.add_to(m)

# --- Mostrar en Streamlit ---
st_folium(m, width=800, height=600)
