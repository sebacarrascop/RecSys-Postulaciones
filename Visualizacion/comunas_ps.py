import json
import pandas as pd

print("Leyendo datos geojson...")
with open('comunas_ps.geojson', encoding='utf-8') as f:
  datos = json.load(f)
  print("Datos Leídos")

postulaciones_por_establecimiento = {}
postulaciones_totales = 0

print("Leyendo archivo csv...")
archivo = pd.read_csv('postulaciones.csv', encoding='utf-8')
print("Archivo leído")

print("Contando postulaciones por establecimiento...")
for fila in archivo.iterrows():
    establecimiento = fila[1]['rbd']
    if establecimiento not in postulaciones_por_establecimiento:
        postulaciones_por_establecimiento[establecimiento] = 0
    postulaciones_por_establecimiento[establecimiento] += 1
    postulaciones_totales += 1
print("Conteo finalizado")

oferta_por_establecimientos = {}
vacantes_totales = 0

print("Leyendo archivo csv...")
archivo = pd.read_csv('Oferta.csv', encoding='utf-8', sep=';')
archivo = archivo[archivo['rbd'].isin(postulaciones_por_establecimiento.keys())]
print("Archivo leído")

print("Contando oferta por establecimiento...")
for fila in archivo.iterrows():
    establecimiento = fila[1]['rbd']
    if establecimiento not in oferta_por_establecimientos:
        oferta_por_establecimientos[establecimiento] = 0
    oferta_por_establecimientos[establecimiento] += fila[1]['vacantes']
    vacantes_totales += fila[1]['vacantes']
print("Conteo finalizado")

suma_proporciones_vacantes = 0
suma_proporciones_postulaciones = 0
print("Agregando información por establecimiento...")
establecimientos = pd.read_csv('informacion_establecimientos.csv', encoding='utf-8')  
for row in establecimientos.iterrows():
    rbd = row[1]['RBD']
    if rbd in postulaciones_por_establecimiento:
        establecimientos.loc[row[0], 'n_postulaciones'] = postulaciones_por_establecimiento[rbd]
        establecimientos.loc[row[0], 'n_postulaciones_p'] = postulaciones_por_establecimiento[rbd]/postulaciones_totales
        suma_proporciones_postulaciones += postulaciones_por_establecimiento[rbd]/postulaciones_totales
    if rbd in oferta_por_establecimientos:
        establecimientos.loc[row[0], 'vacantes'] = oferta_por_establecimientos[rbd]
        establecimientos.loc[row[0], 'vacantes_p'] = oferta_por_establecimientos[rbd]/vacantes_totales
        suma_proporciones_vacantes += oferta_por_establecimientos[rbd]/vacantes_totales
  
establecimientos.to_csv('informacion_establecimientos.csv', index=False)
print("Información agregada")
print("Suma de proporciones de vacantes: ", suma_proporciones_vacantes)
print("Suma de proporciones de postulaciones: ", suma_proporciones_postulaciones)


vacantes_por_comuna = {}

print("Leyendo archivo csv...")
archivo = pd.read_csv('informacion_establecimientos.csv', encoding='utf-8')
print("Archivo leído")

print("Contando postulaciones por comuna...")
for fila in archivo.iterrows():
    comuna = fila[1]['NOM_COM_RBD']
    if comuna not in vacantes_por_comuna:
        vacantes_por_comuna[comuna] = 0
    vacantes_por_comuna[comuna] += fila[1]['vacantes']
print("Conteo finalizado")
   
establecimientos_por_comuna = {}

print("Leyendo archivo csv...")
archivo = pd.read_csv('informacion_establecimientos.csv', encoding='utf-8')
print("Archivo leído")

print("Contando establecimientos por comuna...")
for fila in archivo.iterrows():
    comuna = fila[1]['NOM_COM_RBD']
    if comuna not in establecimientos_por_comuna:
        establecimientos_por_comuna[comuna] = 0
    establecimientos_por_comuna[comuna] += 1
print("Conteo finalizado")

postulaciones_por_comuna = {}

print("Leyendo archivo csv...")
archivo = pd.read_csv('informacion_establecimientos.csv', encoding='utf-8')
print("Archivo leído")

print("Contando postulaciones por comuna...")
for fila in archivo.iterrows():
    comuna = fila[1]['NOM_COM_RBD']
    if comuna not in postulaciones_por_comuna:
        postulaciones_por_comuna[comuna] = 0
    postulaciones_por_comuna[comuna] += fila[1]['n_postulaciones']
print("Conteo finalizado")

print("Agregando información por comuna...")
for comuna in datos['features']:
    nombre_comuna = comuna['properties']['COMUNA']
  
    if nombre_comuna in establecimientos_por_comuna:
        comuna['properties']['n_establecimientos'] = establecimientos_por_comuna[nombre_comuna]
  
    if nombre_comuna in postulaciones_por_comuna:
        comuna['properties']['n_postulaciones'] = postulaciones_por_comuna[nombre_comuna]
        comuna['properties']['n_postulaciones_p'] = postulaciones_por_comuna[nombre_comuna]/postulaciones_totales
    
    if nombre_comuna in vacantes_por_comuna:
        comuna['properties']['vacantes'] = vacantes_por_comuna[nombre_comuna]
        comuna['properties']['vacantes_p'] = vacantes_por_comuna[nombre_comuna]/vacantes_totales
print("Información agregada")


print("Generando archivo geojson modificado...")
with open('comunas_ps.geojson', 'w') as f:
  json.dump(datos, f, indent=4)
  print('Archivo generado con éxito!')