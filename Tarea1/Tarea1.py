import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
import locale

warnings.simplefilter(action='ignore', category=UserWarning) # No quiero warnings

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # Por errores que me ha dado al leer (igual era otra cosa pero por si acaso)

# Cargar datos

# Cargar datos del dataset de la población:
pob_file_path = 'datasets\\Población residente por fecha, sexo y edad1971.xlsx'
defun_file_path = 'datasets\\Defunciones1975.xlsx'
naci_file_path = 'datasets\\Nacimientos1975.xlsx'
inmig_file_path = 'datasets\\Flujo de inmigración procedente del extranjero por año, sexo y edad2008.xlsx'

pob_df_raw = pd.read_excel(pob_file_path, sheet_name=0, skiprows=5)
defun_df_raw = pd.read_excel(defun_file_path, sheet_name=0, skiprows=6)
naci_df_raw = pd.read_excel(naci_file_path, sheet_name=0, skiprows=6)
inmig_df_raw = pd.read_excel(inmig_file_path, sheet_name=0, skiprows=5)


''' 2. Tratamiento de datos'''

'''' 2.1. Obtención de datos de las tablas generales '''

''' 2.1.1. Defunciones '''
# Cortar las primeras columnas para ambos sexos
defun_df_raw = defun_df_raw.iloc[:, :50]

# Usar la primera fila como nombres de columnas
defun_df_raw.columns = defun_df_raw.iloc[0]

# Eliminar la fila de encabezados original
defun_df_raw = defun_df_raw.drop(index=0).reset_index(drop=True)

# Quedarse solo con la primera fila de contenido (la que tiene "Total")
defun_df_raw_g = defun_df_raw.iloc[[0]].reset_index(drop=True)

# Filtrar columnas que realmente representen años (4 dígitos numéricos)
valid_cols = [col for col in defun_df_raw_g.columns if str(col).strip().replace('.0', '').isdigit() and len(str(int(float(col)))) == 4]

# Filtrar el DataFrame a esas columnas
defun_df_raw_g = defun_df_raw_g[valid_cols]

# Convertir columnas a datetime
defun_df_raw_g.columns = pd.to_datetime([str(int(float(col))) for col in defun_df_raw_g.columns], format='%Y')

# Transponer y renombrar
defun_df_raw_g = defun_df_raw_g.T
defun_df_raw_g.columns = ['Total']
defun_df_raw_g.index.name = 'Años'

defun_df_raw_g.rename(columns={'Total': 'Defunciones'}, inplace=True)

print(f"\n--------------------\nTabla de defunciones: \n")
print(defun_df_raw_g.head())

''' 2.1.2. Nacimientos '''
naci_df_raw = naci_df_raw.iloc[:, :50]

# Usar la primera fila como nombres de columnas
naci_df_raw.columns = naci_df_raw.iloc[0]

# Eliminar la fila de encabezados original
naci_df_raw = naci_df_raw.drop(index=0).reset_index(drop=True)

# Quedarse solo con la primera fila de contenido (la que tiene "Total")
naci_df_raw_g = naci_df_raw.iloc[[0]].reset_index(drop=True)

# Filtrar columnas que realmente representen años (4 dígitos numéricos)
valid_cols = [col for col in naci_df_raw_g.columns if str(col).strip().replace('.0', '').isdigit() and len(str(int(float(col)))) == 4]

# Filtrar el DataFrame a esas columnas
naci_df_raw_g = naci_df_raw_g[valid_cols]

# Convertir columnas a datetime
naci_df_raw_g.columns = pd.to_datetime([str(int(float(col))) for col in naci_df_raw_g.columns], format='%Y')

# Transponer y renombrar
naci_df_raw_g = naci_df_raw_g.T
naci_df_raw_g.columns = ['Total']
naci_df_raw_g.index.name = 'Años'

naci_df_raw_g.rename(columns={'Total': 'Nacimientos'}, inplace=True)

print(f"\n--------------------\nTabla de nacimientos: \n")
print(naci_df_raw_g.head())

''' 2.1.3. Tabla de inmigraciones '''

# Extraer fechas de la fila 0
fechas = inmig_df_raw.iloc[0, 1:].tolist()
inmig_df_raw.columns = ['Sexo/Grupo de edad'] + fechas

fechas_inmg = inmig_df_raw.iloc[0, 1:].tolist()

inmig_df_raw.columns = ['Sexo/Grupo de edad'] + fechas_inmg

# Eliminar las filas de encabezado innecesarias
inmig_df_raw = inmig_df_raw.drop(index=[0, 1]).reset_index(drop=True)

# Extraer filas por posición (Ambos sexos, Hombres, Mujeres)
img_df_filtered_g = inmig_df_raw.iloc[0:1].copy()

# Transponer y renombrar
img_df_transpuesto_g = img_df_filtered_g.set_index('Sexo/Grupo de edad').transpose().reset_index()
img_df_transpuesto_g.columns = ['Años', 'Inmigrantes']

# Intentar convertir la columna de fecha a datetime
img_df_transpuesto_g['Años'] = pd.to_datetime(img_df_transpuesto_g['Años'].astype(float).astype(int).astype(str), format='%Y')

# Establecer 'Años' como índice
img_df_transpuesto_g = img_df_transpuesto_g.set_index('Años')

# Mostrar resultado
print(f"\n--------------------\nTabla de inmigraciones: \n")
print(img_df_transpuesto_g.head())

''' 2.1.4. Tabla de población '''
# Extraer fechas de la fila 0
fechas = pob_df_raw.iloc[0, 1:].tolist()
pob_df_raw.columns = ['Sexo/Grupo de edad'] + fechas

fechas_defun = defun_df_raw.iloc[0, 1:].tolist()
defun_df_raw.columns = ['Sexo/Grupo de edad'] + fechas_defun

# Eliminar las filas de encabezado innecesarias
pob_df_raw = pob_df_raw.drop(index=[0, 1]).reset_index(drop=True)

# Extraer filas por posición (Ambos sexos, Hombres, Mujeres)
pob_df_filtered_g = pob_df_raw.iloc[0:3].copy()

# Transponer y renombrar
pob_df_transpuesto_g = pob_df_filtered_g.set_index('Sexo/Grupo de edad').transpose().reset_index()
pob_df_transpuesto_g.columns = ['Años', 'Ambos sexos', 'Hombres', 'Mujeres']

# Intentar convertir la columna de fecha a datetime
pob_df_transpuesto_g['Años'] = pd.to_datetime(pob_df_transpuesto_g['Años'], format='%d de %B de %Y', errors='coerce')

# Establecer 'Años' como índice
pob_df_transpuesto_g = pob_df_transpuesto_g.set_index('Años')
# Mostrar resultado
print(f"\n--------------------\nTabla de poblaciones: \n")
print(pob_df_transpuesto_g.head())

''' 2.2.1. Unión de Nacimientos y defunciones de ambos sexos'''
df_NaDef_combinado = pd.concat([defun_df_raw_g, naci_df_raw_g], axis=1)
print(f"\n--------------------\nTabla general de nacimientos y defunciones de ambos sexos: \n")
print(df_NaDef_combinado.head())

''' 2.2.2. Unión de Nacimientos y defunciones de ambos sexos con inmigrantes'''
df_NaDefInm_combinado = pd.concat([df_NaDef_combinado, img_df_transpuesto_g], axis=1)
df_NaDefInm_combinado['Inmigrantes'] = df_NaDefInm_combinado['Inmigrantes'].fillna(0)
print(f"\n--------------------\nTabla general de nacimientos, defunciones y inmigración de ambos sexos: \n")
print(df_NaDefInm_combinado.head())

''' 2.2.3. Unión de Nacimientos, defunciones y población de ambos sexos'''
df_NaDefPob_combinado = pd.concat([df_NaDef_combinado, pob_df_transpuesto_g], axis=1)
df_NaDefPob_combinado['Ambos sexos'] = df_NaDefPob_combinado['Ambos sexos'].fillna(0)

# Descartamos los datos anteriores a 1975 para que la población empieze a la vez que los demás datasets
df_NaDefPob_combinado = df_NaDefPob_combinado[df_NaDefPob_combinado.index >= '1975']

# Eliminamos las tablas de hombres y mujeres
df_NaDefPob_combinado = df_NaDefPob_combinado.drop(columns=['Hombres', 'Mujeres'], errors='ignore')

# Cambio de nombre de columna de ambos sexos a población
df_NaDefPob_combinado = df_NaDefPob_combinado.rename(columns={'Ambos sexos': 'Población'})

# Arreglo de los NaN de Defunciones en Julio
df_NaDefPob_combinado.index = pd.to_datetime(df_NaDefPob_combinado.index)

# Identificar las filas de julio
julio_mask = df_NaDefPob_combinado.index.month == 7

# Copiar el valor de la fila anterior en esas filas, sólo en la columna "Defunciones"
df_NaDefPob_combinado.loc[julio_mask, 'Defunciones'] = df_NaDefPob_combinado['Defunciones'].shift(1)[julio_mask]

# Arreglo de los NaN de los Nacimientos en Julio
df_NaDefPob_combinado.loc[julio_mask, 'Nacimientos'] = df_NaDefPob_combinado['Nacimientos'].shift(1)[julio_mask]

# Último valor de población igual que el penúltimo (No hay datos de población en 2023)
col_idx = df_NaDefPob_combinado.columns.get_loc('Población')

# Copiar el valor de la penúltima fila a la última
df_NaDefPob_combinado.iloc[-1, col_idx] = df_NaDefPob_combinado.iloc[-2, col_idx]

print(f"\n--------------------\nTabla general de nacimientos, defunciones y población de ambos sexos: \n")
print(df_NaDefPob_combinado.head())

''' 2.2.4. Unión de todas las tablas anteriores'''
df_all_combinado = pd.concat([df_NaDefPob_combinado, img_df_transpuesto_g], axis=1)
df_all_combinado['Inmigrantes'] = df_all_combinado['Inmigrantes'].fillna(0)
print(f"\n--------------------\nTabla general de nacimientos y defunciones de ambos sexos: \n")
print(df_all_combinado)

''' 3. Creación e impresión de las gráficas '''

''' 3.1.1. Line plot de los nacimientos '''
# Resetear el índice para que "Años" sea una columna
df_plot = naci_df_raw_g.reset_index()

plt.figure(figsize=(12, 5))
sns.lineplot(data=df_plot, x='Años', y='Nacimientos', marker='o')
plt.title('Nacimientos por Año')
plt.xlabel('Año')
plt.ylabel('Cantidad de Nacimientos')
plt.grid(True)

# Mostrar ticks cada 4 años
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(4))  # Cada 4 años
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.savefig('images/nacimientos_por_anio.png', dpi=300)
#plt.show()

''' 3.1.2. Pastel de nacimientos cada 10 años '''
# Aplicar estilo Seaborn
sns.set_theme(style="whitegrid")

# Crear columna con la década
df_decadas = naci_df_raw_g.copy()
df_decadas['Década'] = df_decadas.index.year // 10 * 10

# Agrupar por década
df_agrupado = df_decadas.groupby('Década')['Nacimientos'].sum()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
plt.pie(
    df_agrupado,
    labels=[f"{dec}s" for dec in df_agrupado.index],
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(edgecolor='w')
)
plt.title('Distribución de Nacimientos por Década')
plt.tight_layout()
plt.savefig('images/pastel_nacimientos_decadas.png', dpi=300)
#plt.show()

''' 3.2.1. Line plot de las defunciones '''
# Resetear el índice para que "Años" sea una columna
df_plot = defun_df_raw_g.reset_index()

plt.figure(figsize=(12, 5))
sns.lineplot(data=df_plot, x='Años', y='Defunciones', marker='o', color='orange')
plt.title('Defunciones por Año')
plt.xlabel('Año')
plt.ylabel('Cantidad de Defunciones')
plt.grid(True)

# Mostrar ticks cada 4 años
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(4))  # Cada 4 años
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.savefig('images/defunciones_por_anio.png', dpi=300)
#plt.show()

''' 3.1.2. Pastel de defunciones cada 10 años '''
# Aplicar estilo Seaborn
sns.set_theme(style="whitegrid")

# Crear columna con la década
df_decadas = defun_df_raw_g.copy()
df_decadas['Década'] = df_decadas.index.year // 10 * 10

# Agrupar por década
df_agrupado = df_decadas.groupby('Década')['Defunciones'].sum()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
plt.pie(
    df_agrupado,
    labels=[f"{dec}s" for dec in df_agrupado.index],
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(edgecolor='w')
)
plt.title('Distribución de Defunciones por Década')
plt.tight_layout()
plt.savefig('images/pastel_defunciones_decadas.png', dpi=300)
#plt.show()

# Aplicar estilo Seaborn
sns.set_theme(style="whitegrid")

# Asegurarse de que los datos son numéricos
pob_df_transpuesto_g = pob_df_transpuesto_g.astype(float)

# Crear gráfico
plt.figure(figsize=(12, 6))
plt.stackplot(
    pob_df_transpuesto_g.index,
    pob_df_transpuesto_g['Hombres'],
    pob_df_transpuesto_g['Mujeres'],
    labels=['Hombres', 'Mujeres'],
    colors=['#1f77b4', '#ff7f0e'],
    alpha=0.8
)

# Eje X: mostrar cada 4 años
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Eje Y: formato numérico sin notación científica
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.')))

plt.title('Evolución de la Población por Sexo')
plt.xlabel('Año')
plt.ylabel('Población')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('images/poblation_stacked_plot.png', dpi=300)
#plt.show()

''' 3.2.1. Gráfica de area rellena de dos ejes de población, nacimientos y defunciones '''
# Crear gráfico
fig, ax1 = plt.subplots(figsize=(14, 7))

# Eje 1 (Nacimientos y Defunciones)
ax1.set_xlabel('Año')
ax1.set_ylabel('Nacimientos / Defunciones', color='tab:blue')
ax1.plot(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Nacimientos'], label='Nacimientos', color='orange')
ax1.fill_between(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Nacimientos'], alpha=0.2, color='orange')

ax1.plot(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Defunciones'], label='Defunciones', color='red')
ax1.fill_between(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Defunciones'], alpha=0.2, color='red')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Eje 2 (Población)
ax2 = ax1.twinx()
ax2.set_ylabel('Población', color='tab:green')
ax2.plot(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Población'], label='Población', color='green')
ax2.fill_between(df_NaDefPob_combinado.index, df_NaDefPob_combinado['Población'], alpha=0.2, color='green')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Eje X cada 4 años
ax1.xaxis.set_major_locator(mdates.YearLocator(4))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

# Comentario alineado verticalmente con el eje Y izquierdo
ax1.text(
    -0.09, 0.5,
    '(en miles de personas)',
    transform=ax1.transAxes,
    fontsize=10,
    color='tab:blue',
    rotation=90,
    va='center',
    ha='right'
)

# Comentario alineado verticalmente con el eje Y derecho
ax2.text(
    1.05, 0.5,
    '(en decenas de millones)',
    transform=ax2.transAxes,
    fontsize=10,
    color='tab:green',
    rotation=90,
    va='center',
    ha='left'
)

# INMIGRACIÓN
# Título y leyendas
plt.title('Nacimientos, Defunciones y Población (ejes separados)')
fig.tight_layout()
plt.savefig('images/relación_pobnacdef.png', dpi=300)
#plt.show()

# Estilo
sns.set_theme(style="whitegrid")

img_df_ordenado = img_df_transpuesto_g.sort_index()

# Crear figura y axes
fig, ax = plt.subplots(figsize=(12, 6))

# Gráfico de barras apiladas (una serie)
img_df_ordenado.plot(
    kind='bar',
    stacked=True,
    color='tab:purple',
    legend=False,
    width=0.8,
    ax=ax
)

ax.set_xticklabels([d.year for d in img_df_ordenado.index], rotation=45)

# Etiquetas y título
ax.set_title('Inmigración por Año')
ax.set_xlabel('Año')
ax.set_ylabel('Número de Inmigrantes')

plt.tight_layout()
plt.savefig('images/stacked_bar_inmigrantes_ordenado.png', dpi=300)
#plt.show()

# PASTEL INMIGRACIÓN

# Asegurar que el índice sea datetime y los valores sean numéricos
img_df_transpuesto_g = img_df_transpuesto_g.astype(float)

# Crear columna con la década
df_inmig_decadas = img_df_transpuesto_g.copy()
df_inmig_decadas['Década'] = df_inmig_decadas.index.year // 10 * 10 # 10 para la década

# Agrupar por década
df_inmig_agrupado = df_inmig_decadas.groupby('Década')['Inmigrantes'].sum()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
plt.pie(
    df_inmig_agrupado,
    labels=[f"{dec}s" for dec in df_inmig_agrupado.index],
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(edgecolor='w')
)
plt.title('Distribución de Inmigración por Década')
plt.tight_layout()
plt.savefig('images/pastel_inmigracion_decadas.png', dpi=300)
#plt.show()

# Agrupar por año
df_heatmap = df_all_combinado.copy().astype(float)
df_heatmap['Año'] = df_heatmap.index.year
df_heatmap = df_heatmap.groupby('Año').mean()

# Transponer para tener indicadores como filas
df_heatmap_T = df_heatmap.T

# Normalizar cada fila (indicador) entre 0 y 1 (Sinó salía bastante mal)
df_heatmap_normalized = (df_heatmap_T - df_heatmap_T.min(axis=1).values[:, None]) / (df_heatmap_T.max(axis=1).values[:, None] - df_heatmap_T.min(axis=1).values[:, None])

# Crear heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(df_heatmap_normalized, cmap='YlOrBr', linewidths=0.5, linecolor='white', annot=False)

plt.title('Heatmap de Indicadores Demográficos por Año (Normalizado)')
plt.xlabel('Año')
plt.ylabel('Indicador')
plt.tight_layout()
plt.savefig('images/heatmap_indicadores_normalizado.png', dpi=300)
#plt.show()

# Gráfico de burbujas
# Preparar DataFrame agrupado por año
df_bubble = df_all_combinado.copy()
df_bubble['Año'] = df_bubble.index.year

# Agrupar por año y calcular media
df_bubble = df_bubble.groupby('Año').mean().reset_index()

# Filtrar desde 2002
df_bubble = df_bubble[df_bubble['Año'] >= 2005]

# Calcular la diferencia entre natalidad y defunciones
df_bubble['Saldo Natural'] = df_bubble['Nacimientos'] - df_bubble['Defunciones']

# Crear bubble chart
plt.figure(figsize=(14, 8))
scatter = plt.scatter(
    x=df_bubble['Año'],
    y=df_bubble['Población'],
    s=df_bubble['Inmigrantes'] / 100, 
    c=df_bubble['Saldo Natural'],
    cmap='coolwarm',
    alpha=0.7,
    edgecolors='k'
)

# Ejes y título
plt.xlabel('Año')
plt.ylabel('Población')
plt.title('Bubble Chart: Población vs Año (Tamaño = Inmigración, Color = Saldo Natural)')
plt.colorbar(scatter, label='Saldo Natural (Nacimientos - Defunciones)')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/bubble_chart_poblacion_desde_2002.png', dpi=300)
#plt.show()

# FINAL ---------> Pirámide poblacional
# Rutas de los archivos
pir1971_file_path = 'datasets\\EdadPob1971-PAños.xlsx'
pir2024_file_path = 'datasets\\EdadPob2024-PAños.xlsx'

# Leer los archivos
pir1971_raw = pd.read_excel(pir1971_file_path, sheet_name=0, skiprows=8)
pir2024_raw = pd.read_excel(pir2024_file_path, sheet_name=0, skiprows=8)

print(pir1971_raw)

# Renombrar columnas del archivo 1971 y limpiar NaNs
pir1971_raw.columns = ['Edad', 'Hombres', 'Mujeres']
pir1971_raw = pir1971_raw.fillna(0)
pir1971_raw['Hombres'] = pd.to_numeric(pir1971_raw['Hombres'], errors='coerce')
pir1971_raw['Mujeres'] = pd.to_numeric(pir1971_raw['Mujeres'], errors='coerce')

# Renombrar columnas del archivo 2024 y limpiar NaNs
pir2024_raw.columns = ['Edad', 'Hombres', 'Mujeres']
pir2024_raw = pir2024_raw.fillna(0)
pir2024_raw['Hombres'] = pd.to_numeric(pir2024_raw['Hombres'], errors='coerce')
pir2024_raw['Mujeres'] = pd.to_numeric(pir2024_raw['Mujeres'], errors='coerce')

# Función para agrupar edades por franjas de 5 años
def agrupar_por_franjas_separado(df, columna):
    df = df.copy()
    df = df[df['Edad'].astype(str).str.contains('año')] 
    df['Edad_num'] = df['Edad'].str.extract(r'(\d+)').astype(float)
    df['Grupo_inicio'] = (df['Edad_num'] // 5 * 5).astype(int)
    df['Grupo'] = df['Grupo_inicio'].astype(str) + '-' + (df['Grupo_inicio'] + 4).astype(str)
    grouped = df.groupby(['Grupo_inicio', 'Grupo'], as_index=False)[columna].sum()
    return grouped.drop(columns='Grupo_inicio')

# Agrupar los tres datasets
pir1971_hombres = agrupar_por_franjas_separado(pir1971_raw, 'Hombres')
pir1971_mujeres = agrupar_por_franjas_separado(pir1971_raw, 'Mujeres')

pir2024_hombres = agrupar_por_franjas_separado(pir2024_raw, 'Hombres')
pir2024_mujeres = agrupar_por_franjas_separado(pir2024_raw, 'Mujeres')

pir1971_concat = pd.merge(pir1971_hombres, pir1971_mujeres, on='Grupo')
pir2024_concat = pd.merge(pir2024_hombres, pir2024_mujeres, on='Grupo')

print(pir1971_concat)
print(pir2024_concat)

pir2024_concat_sorted = pir2024_concat.copy()
hombres = -pir2024_concat_sorted['Hombres']
mujeres = pir2024_concat_sorted['Mujeres']
grupos = pir2024_concat_sorted['Grupo']

# Crear figura con barras horizontales
fig = go.Figure()

fig.add_trace(go.Bar(
    y=grupos,
    x=hombres,
    name='Hombres',
    orientation='h',
    marker=dict(color='steelblue')
))

fig.add_trace(go.Bar(
    y=grupos,
    x=mujeres,
    name='Mujeres',
    orientation='h',
    marker=dict(color='salmon')
))

# Personalización del layout
fig.update_layout(
    title='Pirámide Poblacional España 2024',
    xaxis=dict(title='Población', tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
               ticktext=['2M', '1M', '0', '1M', '2M']),
    yaxis=dict(title='Edad'),
    barmode='relative',
    bargap=0.1,
    plot_bgcolor='white',
    template='simple_white'
)


#fig.write_image("images/piramide_poblacional_2024.png", width=900, height=600, scale=2)

# Crear versiones negativas para los hombres (pirámide a la izquierda) SEGUNDA PIRÁMIDE <<----------
pir1971_concat_sorted = pir1971_concat.copy()
hombres = -pir1971_concat_sorted['Hombres']
mujeres = pir1971_concat_sorted['Mujeres']
grupos = pir1971_concat_sorted['Grupo']

# Crear figura con barras horizontales
fig = go.Figure()

fig.add_trace(go.Bar(
    y=grupos,
    x=hombres,
    name='Hombres',
    orientation='h',
    marker=dict(color='steelblue')
))

fig.add_trace(go.Bar(
    y=grupos,
    x=mujeres,
    name='Mujeres',
    orientation='h',
    marker=dict(color='salmon')
))

# Personalización del layout
fig.update_layout(
    title='Pirámide Poblacional España 1971',
    xaxis=dict(title='Población', tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
               ticktext=['2M', '1M', '0', '1M', '2M']),
    yaxis=dict(title='Edad'),
    barmode='relative',
    bargap=0.1,
    plot_bgcolor='white',
    template='simple_white'
)

fig.show()
#fig.write_image("images/piramide_poblacional_1971.png")

## Tengo comentados los write image por que me dice que no existe una librería que utiliza esa función y si que la tengo.
## Las imágenes las he conseguido capturando la pantalla (sé que no es lo óptimo pero no me funciona la función)

