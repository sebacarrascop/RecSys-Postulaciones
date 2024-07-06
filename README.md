# RecSys-Postulaciones
Este repositorio cuenta con todos los archivos generados para el proyecto de Recomendación de Postulaciones a Establecimientos Educacionales.

Existen cuatro carpetas:

## Datasets
Contiene los dataset utilizados, un jupyter notebook que procesa y analiza estos datos y una carpeta donde se guardan los datos procesados.

## ALS_LightFM_Random_MP
Contiene 3 jupyter notebooks en los que se implementan Filtrado Colaborativo (ALS.ipynb), Máquina de Factorización (LightFM.ipynb) y Random y Most Popular (RandomMostPopular.ipynb). Para ejecutar los notebooks se deben copiar los datos procesados en la misma carpeta.

## Visualizacion
Contiene tres carpetas: src contiene archivos html, css y js para crear la visualización del mapa de la provincia de Santiago. Para utilizarlo se debe utilizar un servidor, se recomienda usar la extensión de vscode "Live Share". Para cambiar entre visualizaciones se debe cambiar el nombre del archivo del script que está al final del documento. "utils" tiene los programas de python que procesan los archivos para arreglar el geojson y crear los csv necesarios. En "data" se guardan los archivos necesarios que deben ser procesados y que ya están procesados.

## LightGCN-PyTorch
Se utilizo la implementación de LightGCN en pytorch del paper SIGIR 2020:
>SIGIR 2020. Xiangnan He, Kuan Deng ,Xiang Wang, Yan Li, Yongdong Zhang, Meng Wang(2020). LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation, [Paper in arXiv](https://arxiv.org/abs/2002.02126).
Author: Prof. Xiangnan He (staff.ustc.edu.cn/~hexn/)

# Pasos para la correcta utilización (desde 0):
1. Guardar en DataRaw los documentos necesarios si no están guardados ya.
2. Ejecutar datasets.ipynb.
3. Copiar en "ALS_LightFM_Random_MP" y "LightGCN-PyTorch/data/recsys" los datasets necesarios.
4. Ejecutar los jupyter notebooks que se encuentran en "ALS_LightFM_Random_MP".
5. Ejecutar el programa que se encuentra en "LightGCN-PyTorch/data/recsys" y luego el archivo main.py en "LightGCN-PyTorch/cod".
6. Copiar en "Visualización/data" los dataset necesarios y ejecutar los programas en "Visualización/utils".
7. Abrir index.html en "Visualizacion/src" con Live Server.

También se puede saltar todos los pasos que tiene que ver con el procesamiento de datos si se descomprimmen los archivos zip que se encuentran en el repositorio.