import json
import pandas as pd

with open('recomendaciones_als.json') as file:
    recomendaciones_als = json.load(file)

with open('recomendaciones_lightfm.json') as file:
    recomendaciones_lightfm = json.load(file)

with open('recomendaciones_mp.json') as file:
    recomendaciones_mp = json.load(file)


with open('recomendaciones_random.json') as file:
    recomendaciones_random = json.load(file)

df_postulantes = pd.read_csv('Postulantes.csv', encoding='utf-8', sep=';')
df_establecimientos = pd.read_csv('informacion_establecimientos.csv', encoding='utf-8', sep=',')
df_establecimientos = df_establecimientos[['RBD', 'LATITUD', 'LONGITUD']]

df_postulantes['mrun'] = df_postulantes['mrun'].astype(str)

df_postulantes = df_postulantes[df_postulantes['mrun'].isin(recomendaciones_lightfm.keys())][['mrun', 'lat_con_error', 'lon_con_error']]

df_postulantes['lat_con_error'] = df_postulantes['lat_con_error'].apply(lambda x: x.replace(',', '.'))
df_postulantes['lon_con_error'] = df_postulantes['lon_con_error'].apply(lambda x: x.replace(',', '.'))
df_postulantes['lat_con_error'] = df_postulantes['lat_con_error'].astype(float)
df_postulantes['lon_con_error'] = df_postulantes['lon_con_error'].astype(float)

df_postulantes['recomendaciones_als'] = df_postulantes['mrun'].apply(lambda x: recomendaciones_als[x])
df_postulantes['recomendaciones_lightfm'] = df_postulantes['mrun'].apply(lambda x: recomendaciones_lightfm[x])
df_postulantes['recomendaciones_mp'] = df_postulantes['mrun'].apply(lambda x: recomendaciones_mp[x])
df_postulantes['recomendaciones_random'] = df_postulantes['mrun'].apply(lambda x: recomendaciones_random[x])

colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4']
colors_dict = {}
for i, mrun in enumerate(df_postulantes['mrun']):
    colors_dict[mrun] = colors[i]

ubicaciones_als = {}
ubicaciones_lightfm = {}
ubicaciones_postulante = {}
ubicaciones_mp = {}
ubicaciones_random = {}
x = 0
for postulante in df_postulantes['mrun']:
    i = 0
    ubicaciones_postulante[postulante] = {
        'color': colors_dict[postulante],
        'lat': list(df_postulantes[df_postulantes['mrun'] == postulante]['lat_con_error'])[0],
        'lon': list(df_postulantes[df_postulantes['mrun'] == postulante]['lon_con_error'])[0],
    }

    for recomendacion in list(df_postulantes[df_postulantes['mrun'] == postulante]['recomendaciones_als'])[0]:
        ubicacion = df_establecimientos[df_establecimientos['RBD'] == recomendacion][['LATITUD','LONGITUD']].values[0].tolist()
        ubicaciones_als[x+i] = {
            'color': colors_dict[postulante],
            'lat': ubicacion[0],
            'lon': ubicacion[1],
        }
        i += 1
    i = 0
    for recomendacion in list(df_postulantes[df_postulantes['mrun'] == postulante]['recomendaciones_lightfm'])[0]:
        ubicacion = df_establecimientos[df_establecimientos['RBD'] == recomendacion][['LATITUD','LONGITUD']].values[0].tolist()
        ubicaciones_lightfm[x+i] = {
            'color': colors_dict[postulante],
            'lat': ubicacion[0],
            'lon': ubicacion[1],
        }
        i += 1
    i = 0
    for recomendacion in list(df_postulantes[df_postulantes['mrun'] == postulante]['recomendaciones_mp'])[0]:
        ubicacion = df_establecimientos[df_establecimientos['RBD'] == recomendacion][['LATITUD','LONGITUD']].values[0].tolist()
        ubicaciones_mp[x+i] = {
            'color': colors_dict[postulante],
            'lat': ubicacion[0],
            'lon': ubicacion[1],
        }
        i += 1
    i = 0
    for recomendacion in list(df_postulantes[df_postulantes['mrun'] == postulante]['recomendaciones_random'])[0]:
        ubicacion = df_establecimientos[df_establecimientos['RBD'] == recomendacion][['LATITUD','LONGITUD']].values[0].tolist()
        ubicaciones_random[x+i] = {
            'color': colors_dict[postulante],
            'lat': ubicacion[0],
            'lon': ubicacion[1],
        }
        i += 1
    x += i
df_ubicaciones_als = pd.DataFrame(ubicaciones_als).T
df_postulantes = pd.DataFrame(ubicaciones_postulante).T
df_ubicaciones_lightfm = pd.DataFrame(ubicaciones_lightfm).T
df_ubicaciones_mp = pd.DataFrame(ubicaciones_mp).T
df_ubicaciones_random = pd.DataFrame(ubicaciones_random).T
df_ubicaciones_lightfm.to_csv('recomendaciones_lightfm.csv', encoding='utf-8', sep=',', index=False)
df_ubicaciones_als.to_csv('recomendaciones_als.csv', encoding='utf-8', sep=',', index=False)
df_postulantes.to_csv('ubicacion_postulantes.csv', encoding='utf-8', sep=',', index=False)
df_ubicaciones_mp.to_csv('recomendaciones_mp.csv', encoding='utf-8', sep=',', index=False)
df_ubicaciones_random.to_csv('recomendaciones_random.csv', encoding='utf-8', sep=',', index=False)
