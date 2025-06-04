import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
import json
import numpy as np
from streamlit_folium import st_folium
from branca.colormap import linear, LinearColormap

# --- Cargar geometría ---
provincias = gpd.read_file('TrabajoAcademico/datasets')
provincias = provincias.to_crs("EPSG:4326")
provincias = provincias[['NAMEUNIT', 'geometry']]
provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})
gdf = gpd.GeoDataFrame(provincias, crs="EPSG:4326")

# --- Función de limpieza de índices ---
def limpiar_indices(df):
    df.columns.values[0] = 'Provincia'
    df['Provincia'] = df['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()
    df.set_index('Provincia', inplace=True)
    df.index = df.index.str[3:]
    df.index = df.index.map(lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x)
    df.index = df.index.map(lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x)
    return df

# --- Cargar datos población ---
pob_homb_df = limpiar_indices(pd.read_excel('TrabajoAcademico/datasets/PobHomb.xlsx', sheet_name=0, skiprows=6))
pob_muj_df  = limpiar_indices(pd.read_excel('TrabajoAcademico/datasets/PobMuj.xlsx',  sheet_name=0, skiprows=6))
pob_tot_df  = limpiar_indices(pd.read_excel('TrabajoAcademico/datasets/PobTot.xlsx',  sheet_name=0, skiprows=6))

# --- Interfaz Streamlit ---
st.title("Mapa interactivo de población por provincia")
st.sidebar.header("Filtros")
 
# --- Mostrar primero el selector de fecha ---
data_columns = pob_tot_df.select_dtypes(include=['float64', 'int']).columns.tolist()
selected_column = st.sidebar.selectbox("Selecciona una fecha", data_columns)

# --- Luego el selector de grupo poblacional ---
genero = st.sidebar.radio("Selecciona grupo poblacional", ["Total", "Hombres", "Mujeres"], index=0)

# --- Seleccionar DataFrame según opción ---
if genero == "Hombres":
    pob_df = pob_homb_df
elif genero == "Mujeres":
    pob_df = pob_muj_df
else:
    pob_df = pob_tot_df

# --- Unir con geometría ---
gdf_gen = gdf.merge(pob_df, on='Provincia', how='left')
gdf_gen.fillna(1, inplace=True)  # Evitar log(0) o nulos

# --- Confirmar que la columna seleccionada existe ---
if selected_column not in gdf_gen.columns:
    st.warning(f"La columna '{selected_column}' no existe para {genero.lower()}.")
    st.stop()

st.write(f"Mostrando datos para: **{selected_column}** ({genero})")

# --- Calcular vmin y vmax para leyenda ---
vmin = float(gdf_gen[selected_column].min())
vmax = float(gdf_gen[selected_column].max())

# --- Crear colormap personalizado ---
viridis_colors = linear.viridis.colors
caption = f"Población de {genero.lower()} en {selected_column}"
colormap = LinearColormap(
    colors=viridis_colors,
    vmin=vmin,
    vmax=vmax,
    caption=caption,
    tick_labels=[vmin, vmax]
)

# --- Simplificación ligera (opcional) ---
gdf_gen['geometry'] = gdf_gen['geometry'].simplify(0.001, preserve_topology=True)

# --- Crear y centrar mapa ---
m = folium.Map(zoom_start=6)
bounds = gdf_gen.total_bounds
m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

# --- Convertir a GeoJSON ---
geojson_data = json.loads(gdf_gen.to_json())

# --- Añadir capa GeoJson ---
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

# --- Añadir leyenda ---
colormap.options = {"position": "bottomleft"}
colormap.add_to(m)

# --- Mostrar mapa ---
st_folium(m, use_container_width=True, height=600, returned_objects=[])
