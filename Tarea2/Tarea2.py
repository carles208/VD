import matplotlib.pyplot as plt
from matplotlib import colors
import geopandas as gpd
import pandas as pd

def parse_age(col):
    return 100 if '100' in col else int(col.split()[0])

''' 
    -------------------------------------------------------------------
    |                                                                 |
    |                        Cargado de datasets                      |
    |                                                                 |
    -------------------------------------------------------------------
'''


provincias = gpd.read_file('./Datos')
provincias = provincias.to_crs("EPSG:25830")
provincias = provincias[['NAMEUNIT', 'geometry']]
provincias = provincias.rename(columns={'NAMEUNIT': 'Provincia'})

gdf_2022 = gpd.GeoDataFrame(provincias, crs="EPSG:25830")
gdf_1971 = gpd.GeoDataFrame(provincias, crs="EPSG:25830")

pob_2022 = pd.read_excel(
    'Datos/Población_por_provincias_2022.xlsx',
    sheet_name=0,
    skiprows=8,
    usecols=[0,1],
    names=['Provincia','Poblacion']
)

pob_1971 = pd.read_excel(
    'Datos/Población_por_provincias_1971.xlsx',
    sheet_name=0,
    skiprows=8,
    usecols=[0,1],
    names=['Provincia','Poblacion']
)

defu_2022 = pd.read_excel(
    'Datos/Defunciones_2022.xlsx',
    sheet_name=0,
    skiprows=7,
    usecols=[0,1],
    names=['Provincia','Defunciones']
)

naci_2022 = pd.read_excel(
    'Datos/Nacimientos_2022.xlsx',
    sheet_name=0,
    skiprows=7,
    usecols=[0,1],
    names=['Provincia','Nacimientos']
)

edades_2022 = pd.read_excel(
    'Datos/Edades_2022.xlsx',
    sheet_name=0,
    skiprows=8,
)

edades_1971 = pd.read_excel(
    'Datos/Edades_1971.xlsx',
    sheet_name=0,
    skiprows=8,
)

''' 
    -------------------------------------------------------------------
    |                                                                 |
    |                      Tratamiento de dataset                     |
    |                                                                 |
    -------------------------------------------------------------------
'''

''' Análisis poblacional '''
pob_2022['Provincia'] = pob_2022['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

pob_2022.set_index('Provincia', inplace=True)
pob_2022.index = pob_2022.index.str[3:]

pob_2022.index = pob_2022.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

pob_2022.index = pob_2022.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

gdf_2022 = gdf_2022.merge(pob_2022, on='Provincia', how='left')
gdf_2022.fillna(0, inplace=True)
gdf_2022 = gdf_2022.dropna(subset=['Poblacion']).copy()


# Población España 1971
pob_1971['Provincia'] = pob_1971['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

pob_1971.set_index('Provincia', inplace=True)
pob_1971.index = pob_1971.index.str[3:]

pob_1971.index = pob_1971.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

pob_1971.index = pob_1971.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

gdf_1971 = gdf_1971.merge(pob_1971, on='Provincia', how='left')
gdf_1971.fillna(0, inplace=True)
gdf_1971 = gdf_1971.dropna(subset=['Poblacion']).copy()
''' Fin de análisis poblacional '''

''' Inicio análisis Mortalidad'''
# Población España 1971
defu_2022['Provincia'] = defu_2022['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

defu_2022.set_index('Provincia', inplace=True)

defu_2022.index = defu_2022.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

defu_2022.index = defu_2022.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

gdf_2022 = gdf_2022.merge(defu_2022, on='Provincia', how='left')
gdf_2022.fillna(0, inplace=True)
''' Fin de mortalidad '''

''' Inicio de natalidad '''
# Población España 1971
naci_2022['Provincia'] = naci_2022['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

naci_2022.set_index('Provincia', inplace=True)

naci_2022.index = naci_2022.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

naci_2022.index = naci_2022.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

gdf_2022 = gdf_2022.merge(naci_2022, on='Provincia', how='left')
gdf_2022.fillna(0, inplace=True)
''' Fin de natalidad '''

''' Medias de edad 2022 '''
first = edades_2022.columns[0]
edades_2022 = edades_2022.rename(columns={ first: "Provincia" })

edades_2022['Provincia'] = edades_2022['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()
edades_2022.set_index('Provincia', inplace=True)

edades_2022.index = edades_2022.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

edades_2022.index = edades_2022.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)


age_map = {col: parse_age(col) for col in edades_2022.columns}
numerator   = edades_2022.mul(pd.Series(age_map)).sum(axis=1)
denominator = edades_2022.sum(axis=1)

edades_2022['Edad_Media'] = (numerator / denominator).round().astype(int)

medias_edades_20022 = edades_2022[['Edad_Media']].copy()

gdf_2022 = gdf_2022.merge(medias_edades_20022, on='Provincia', how='left')
gdf_2022.fillna(0, inplace=True)

''' Medias de edad 2022 '''
first = edades_1971.columns[0]
edades_1971 = edades_1971.rename(columns={ first: "Provincia" })

edades_1971['Provincia'] = edades_1971['Provincia'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

edades_1971.set_index('Provincia', inplace=True)

edades_1971.index = edades_1971.index.map(
    lambda x: '/'.join(x.split('/')[::-1]) if '/' in x else x
)

edades_1971.index = edades_1971.index.map(
    lambda x: ' '.join(x.split(', ')[::-1]) if ', ' in x else x
)

age_map = {col: parse_age(col) for col in edades_1971.columns}

numerator   = edades_1971.mul(pd.Series(age_map)).sum(axis=1)
denominator = edades_1971.sum(axis=1)

edades_1971['Edad_Media'] = (numerator / denominator).round().astype(int)

medias_edades_1971 = edades_1971[['Edad_Media']].copy()

gdf_1971 = gdf_1971.merge(medias_edades_1971, on='Provincia', how='left')
gdf_1971.fillna(0, inplace=True)

'''Inicio cálculo de personas ≥ 65 años por provincia'''
age_cols_2022 = [c for c in edades_2022.columns if c.endswith('años')]
age_cols_1971 = [c for c in edades_1971.columns if c.endswith('años')]

age_map_2022 = {col: parse_age(col) for col in age_cols_2022}
age_map_1971 = {col: parse_age(col) for col in age_cols_1971}

cols_65_2022 = [col for col, age in age_map_2022.items() if age >= 65]
cols_65_1971 = [col for col, age in age_map_1971.items() if age >= 65]

mayores_65_2022 = edades_2022[cols_65_2022].sum(axis=1).rename('Mayores_65')
mayores_65_1971 = edades_1971[cols_65_1971].sum(axis=1).rename('Mayores_65')

gdf_2022 = gdf_2022.merge(
    mayores_65_2022.reset_index(), on='Provincia', how='left'
)
gdf_1971 = gdf_1971.merge(
    mayores_65_1971.reset_index(), on='Provincia', how='left'
)

for gdf in (gdf_2022, gdf_1971):
    gdf['Mayores_65'] = gdf['Mayores_65'].fillna(0).astype(int)
''' Fin cálculo de personas ≥ 65 años'''

''' 
    -------------------------------------------------------------------
    |                                                                 |
    |                        Dibujado de graficas                     |
    |                                                                 |
    -------------------------------------------------------------------
'''
''' Análisis poblacional '''
# Población España por provincias 2022
vals = gdf_2022['Poblacion']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)

fig, ax = plt.subplots(figsize=(12, 12))
gdf_2022.to_crs(epsg=4326).plot(
    column='Poblacion',
    cmap='plasma',     
    legend=True,
    norm=norm,
    legend_kwds={         
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Población por provincia (2022) – Degradado continuo')
ax.axis('off')
fig.savefig(
    "Imagenes/Población_2022.png",   
    dpi=300,                   
    bbox_inches="tight"        
)

vals = gdf_1971['Poblacion']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)

fig, ax = plt.subplots(figsize=(12, 12))
gdf_1971.to_crs(epsg=4326).plot(
    column='Poblacion',
    cmap='YlOrBr',          
    legend=True,
    norm= norm,
    legend_kwds={         
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Población por provincia (1971) – Degradado continuo')
ax.axis('off')
fig.savefig(
    "Imagenes/Población_1971.png",  
    dpi=300,                  
    bbox_inches="tight"        
)
''' Fin de análisis poblacional '''


''' Defunciones '''
vals = gdf_2022['Defunciones']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)
fig, ax = plt.subplots(figsize=(12, 12))
gdf_2022.to_crs(epsg=4326).plot(
    column='Defunciones',
    cmap='OrRd',         
    legend=True,
    norm= norm,
    legend_kwds={         
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Defunciones por provincia 2022')
ax.axis('off')
fig.savefig(
    "Imagenes/Defunciones_2022.png",  
    dpi=300,                   
    bbox_inches="tight"        
)
''' Fin de defunciones '''

''' Nacimientos '''
vals = gdf_2022['Nacimientos']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)

fig, ax = plt.subplots(figsize=(12, 12))
gdf_2022.to_crs(epsg=4326).plot(
    column='Nacimientos',
    cmap='BuGn',         
    legend=True,
    norm=norm,
    legend_kwds={         
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Nacimientos por provincia 2022')
ax.axis('off')

fig.savefig(
    "Imagenes/nacimientos_2022.png",  
    dpi=300,                   
    bbox_inches="tight"        
)

''' Fin de nacimientos '''

''' Inicio de saldo vegetativo '''
gdf_2022['Saldo_Vegetativo'] = gdf_2022['Nacimientos'] - gdf_2022['Defunciones']

gdf_plot_2022 = gdf_2022.to_crs(epsg=4326)
gdf_plot_1971 = gdf_1971.to_crs(epsg=4326)

sv = gdf_plot_2022['Saldo_Vegetativo']
cmax = max(abs(sv.min()), abs(sv.max()))

fig, ax = plt.subplots(figsize=(12, 12))
gdf_plot_2022.plot(
    column='Saldo_Vegetativo',
    cmap='RdBu',
    vmin=-cmax,
    vmax= cmax,
    legend=True,
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)

ax.set_title('Saldo vegetativo por provincia (2022)')
ax.axis('off')

fig.savefig(
    "Imagenes/saldo_vegetativo_2022.png",  
    dpi=300,                  
    bbox_inches="tight"        
)
''' Fin de saldo vegetativo '''

''' Inicio edad media 2022 '''
fig, ax = plt.subplots(figsize=(12, 12))
gdf_2022.to_crs(epsg=4326).plot(
    column='Edad_Media',
    cmap='viridis',
    legend=True,
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)

for _, row in gdf_plot_2022.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        int(row['Edad_Media']),      # type: ignore
        ha='center', va='center',
        fontsize=10,
        color='black'
    )
ax.set_title('Edad media por provincia (2022)')
ax.axis('off')
fig.savefig(
    "Imagenes/edad_media_2022.png",   
    dpi=300,                  
    bbox_inches="tight"        
)
''' Fin edad media 2022 '''

''' Inicio edad media 1971 '''
fig, ax = plt.subplots(figsize=(12, 12))
gdf_1971.to_crs(epsg=4326).plot(
    column='Edad_Media',
    cmap='viridis',
    legend=True,
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)

for _, row in gdf_plot_1971.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        int(row['Edad_Media']),      # type: ignore
        ha='center', va='center',
        fontsize=10,
        color='black'
    )
ax.set_title('Edad media por provincia (1971)')
ax.axis('off')
fig.savefig(
    "Imagenes/edad_media_1971.png",   
    dpi=300,                   
    bbox_inches="tight"        
)
''' Fin edad media 1971 '''

''' Inicio de mayores de 65 '''
vals = gdf_1971['Mayores_65']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)

fig, ax = plt.subplots(figsize=(12, 12))
gdf_1971.to_crs(epsg=4326).plot(
    column='Mayores_65',
    cmap='viridis',         
    legend=True,
    #norm=norm,
    legend_kwds={         
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Mayores de 65 (1971)')
ax.axis('off')
fig.savefig(
    "Imagenes/mayores_65_1971.png",   
    dpi=300,                   
    bbox_inches="tight"       
)

vals = gdf_2022['Mayores_65']
positive = vals[vals > 0]  

norm = colors.LogNorm(
    vmin=positive.min(),
    vmax=positive.max()
)
fig, ax = plt.subplots(figsize=(12, 12))
gdf_2022.to_crs(epsg=4326).plot(
    column='Mayores_65',
    cmap='viridis',          
    legend=True,
    #norm=norm,
    legend_kwds={        
        'label': "Población",
        'shrink': 0.5
    },
    edgecolor='black',
    linewidth=0.3,
    ax=ax
)
ax.set_title('Mayores de 65 (2022)')
ax.axis('off')
fig.savefig(
    "Imagenes/mayores_65_2022.png",   
    dpi=300,                  
    bbox_inches="tight"        
)
''' Fin de mayores de 65 '''

plt.show()