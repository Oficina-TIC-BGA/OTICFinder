#!/usr/bin/env python
# -*- coding: utf-8 -*-

############ import libraries #########################
# To handle the arguments
import sys
import time
import argparse
import configparser
# To handle the geographical positioning
import geopy
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import ArcGIS, MapBox, GoogleV3
# To handle polygons
import shapely.wkt
import shapely.speedups
from shapely.geometry import Point, Polygon 
# To handle numerical data
import numpy as np 
# To handle regular expressions
import re
import regex
# import our own functions
from identifiers import regex_identifier
from address_cleaner import regex_cleaner
from helpers import get_score, get_city, get_neighbourhood, search_neighbourhood, search_nearby
# To handle other processes
import warnings
warnings.filterwarnings('ignore')
import unicodedata
from functools import partial
from collections import defaultdict
from tqdm import tqdm, tqdm_notebook
# Temporal: Only for use in notebooks
tqdm.pandas()

#################### main.py ###################
def main():
    start_time = time.time()
    print('Ejecutando script ...')
    # parameter reading
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    addresses_path = config['paths']['path_direcciones']
    path_pol = config['paths']['path_division_politica_AMB']
    path_poligonos_bucaramanga = config['paths']['path_poligonos_bucaramanga']
    path_poligonos_giron = config['paths']['path_poligonos_giron']
    path_poligonos_piedecuesta = config['paths']['path_poligonos_piedecuesta']
    path_poligonos_floridablanca = config['paths']['path_poligonos_floridablanca']
    path_poligonos_mun_santander = config['paths']['path_municipios_santander']
    # reading the names of the neighbourhoods in each city
    division_politica_bucaramanga = pd.read_excel(path_pol, sheet_name='DIVISION_POLITICA_BUCARAMANGA')
    division_politica_giron = pd.read_excel(path_pol, sheet_name='DIVISION_POLITICA_GIRON')
    #division_politica_piedecuesta = pd.read_excel(path_pol, sheet_name='DIVISION_POLITICA_PIEDECUESTA')
    division_politica_general = pd.read_excel(path_pol, sheet_name='CIUDADES')
    division_politica_floridablanca = pd.read_excel(path_pol, sheet_name='DIVISION_POLITICA_FLORIDABLANCA')
    # reading shapes files
    data_bucaramanga = pd.read_csv(path_poligonos_bucaramanga)
    bucaramanga_data_shp = data_bucaramanga[data_bucaramanga.CATEGORIA.isin(['BARRIO', 
                                                                             'VEREDA',
                                                                             'A. URBANO', 
                                                                             'A. RURAL'])]
    data_floridablanca = pd.read_csv(path_poligonos_floridablanca)
    # en floridablanca solo se va a considerar barrios
    floridablanca_data_shp = data_floridablanca[data_floridablanca.CATEGORIA.isin(['BARRIO', 
                                                                                   'VEREDA'])]                                                                              

    # concatenate all polygon files
    data_shp = pd.concat([bucaramanga_data_shp, floridablanca_data_shp], ignore_index=True)
    # concatenate all city files to search COMUNA
    todos_div_pol = pd.concat([division_politica_bucaramanga, 
                               division_politica_floridablanca], ignore_index=True)

    # reading the address file to process
    df_addresses = pd.read_excel(addresses_path, sheet_name='Hoja1')
    # Execute the address cleaning function
    print('Paso 1. Limpiando direcciones ....')
    df_addresses['dir_filtradas'] = df_addresses.dir_res_.apply(lambda x: regex_cleaner(x)).values
    
    # Execute the function to identify where the direction is from.
    print('Paso 2. Identificando de donde es cada dirección')
    # pattern to consider other cities of the country
    pattern_general_ = re.compile(r'|'.join(division_politica_general.CIUDADES.values.tolist()+['floridablanca', 'bucaramanga', 'giron']), re.IGNORECASE)
    # Ejecutar la función para aplicar todos los filtros para tratar de identificar en que ciudad podria estar
    #print(df_addresses.dir_filtradas)
    df_addresses['dir_filtradas'] = df_addresses.dir_filtradas.apply(regex_identifier, args=(df_addresses.to_dict('index'),
                                                                                        division_politica_bucaramanga.to_dict('index'),
                                                                                        division_politica_floridablanca.to_dict('index'),
                                                                                        division_politica_giron.to_dict('index'),
                                                                                        pattern_general_)).values

    ## Search coords
    print('Paso 3. Geoposicionando ...')
    # select the empty records
    tem = df_addresses[~df_addresses.dir_filtradas.isna()] 
    # select records with text
    tem_2 = df_addresses[df_addresses.dir_filtradas.isna()]
    # creates the geocoder and the function to handle thee queries
    geolocator = ArcGIS(username=None, 
                        password=None, 
                        user_agent=addresses_path.split('/')[-1],
                        timeout=10)
                        
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    tem['location'] = tem['dir_filtradas'].apply(geocode)
    tem['longitud'] = tem['location'].apply(lambda loc: loc.longitude if loc else None)
    tem['latitud'] = tem['location'].apply(lambda loc: loc.latitude if loc else None)
    tem['respuesta'] = tem['location'].apply(lambda loc: loc.raw if loc else None)
    tem['coordenadas'] = tem['location'].apply(lambda loc: tuple([loc.longitude, loc.latitude]) if loc else None)
    df_addresses = pd.concat([tem, tem_2]).sort_index()
    # search neighbourhoods
    df_addresses['score'] = df_addresses.respuesta.apply(get_score).astype(int)
    df_addresses['ciudad_geo'] = df_addresses.respuesta.apply(lambda x:get_city(x,pattern_general_))
    df_addresses['barrio_geo'] = df_addresses.respuesta.apply(get_neighbourhood) 

    # assign neighbourhood by polygon areas
    print('Paso 4. Asignando barrio')
    operation_search = partial(search_neighbourhood, data_shp.to_dict('index'))
    operation_search_near = partial(search_nearby, data_shp.to_dict('index'))
    # search by intersection and contains operations
    df_addresses['barrio_poly'] = df_addresses.coordenadas.apply(operation_search)
    # search nearby neighbourhood
    df_addresses.loc[(df_addresses.barrio_poly.isnull()) & 
                     (df_addresses.ciudad_geo=='Bucaramanga'), 'barrio_poly'] = df_addresses.loc[(df_addresses.barrio_poly.isnull()) 
                                                                                               & (df_addresses.ciudad_geo=='Bucaramanga'), 'coordenadas'].apply(operation_search_near)                    
    
    df_addresses.loc[(df_addresses.ciudad_geo!='Bucaramanga')
                    & (df_addresses.score>=98)
                    & (df_addresses.barrio_poly.isnull()), 'barrio_poly'] = df_addresses.loc[(df_addresses.ciudad_geo!='Bucaramanga')
                                                                                & (df_addresses.score>=98)
                                                                                & (df_addresses.barrio_poly.isnull()), 'ciudad_geo'].str.upper()

    df_addresses.loc[(df_addresses.ciudad_geo.isnull())
                    & (df_addresses.score>=98)
                    & (~df_addresses.barrio_geo.isnull())
                    & (df_addresses.barrio_poly.isnull()), 'barrio_poly'] =  df_addresses.loc[(df_addresses.ciudad_geo.isnull())
                                                                                            & (df_addresses.score>=98)
                                                                                            & (~df_addresses.barrio_geo.isnull())
                                                                                            & (df_addresses.barrio_poly.isnull()), 'barrio_geo'].str.upper() 

    print('Paso 5. Asignando comuna')
    todos_div_pol.BARRIO = todos_div_pol.BARRIO.str.upper().str.strip()
    df_addresses.barrio_poly = df_addresses.barrio_poly.str.upper().str.strip()
    df_addresses = pd.merge(df_addresses,todos_div_pol[['COMUNA', 'BARRIO']], left_on='barrio_poly', 
                                                                              right_on='BARRIO',
                                                                              how='left')

    print('Paso 6. Creando estructura final')
    df_addresses['NUMERO COMUNA'] = None
    df_addresses['NOMCOMUNA'] = None
    df_addresses['BARRIO_VER'] = None

    df_addresses[['NUMERO COMUNA','NOMCOMUNA']] =  df_addresses.COMUNA.str.split(".",expand=True)
    df_addresses['tem'] = df_addresses.NOMCOMUNA
    df_addresses.loc[df_addresses.NOMCOMUNA.isnull(),'NOMCOMUNA'] = df_addresses.loc[df_addresses.NOMCOMUNA.isnull(),'NUMERO COMUNA']
    df_addresses.loc[df_addresses.tem.isnull(),'NUMERO COMUNA'] = None

    df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                   &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                     'Floridablanca']))), 'COMUNA'] = df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                                                                                                          &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                                                                                                            'Floridablanca']))), 'ciudad_geo'].str.upper()
    df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                   &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                     'Floridablanca']))), 'NOMCOMUNA'] = df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                                                                                                          &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                                                                                                            'Floridablanca']))), 'ciudad_geo'].str.upper()
    df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                   &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                     'Floridablanca']))), 'BARRIO_VER'] = df_addresses.loc[~(df_addresses.ciudad_geo.isnull())
                                                                                                          &(~(df_addresses.ciudad_geo.isin(['Bucaramanga', 
                                                                                                                                            'Floridablanca']))), 'ciudad_geo'].str.upper()
    df_addresses.BARRIO_VER = df_addresses.barrio_poly.str.upper() 
    df_addresses.loc[df_addresses.COMUNA.isnull(),'COMUNA'] = 'SIN INFORMACION'
    df_addresses.loc[df_addresses.BARRIO_VER.isnull(),'BARRIO_VER'] = 'SIN INFORMACION'
    df_addresses.loc[df_addresses.NOMCOMUNA.isnull(),'NOMCOMUNA'] = 0
    df_addresses.loc[df_addresses['NUMERO COMUNA'].isnull(),'NUMERO COMUNA'] = 0
    df_addresses.rename(columns={'location':'dir_localizada'}, inplace=True)

    # delete temporal columns
    del df_addresses['tem']    
    del df_addresses['barrio_poly']
    del df_addresses['barrio_geo']
    del df_addresses['score']
    #del df_addresses['ciudad_geo']
    del df_addresses['coordenadas']
    del df_addresses['respuesta']
    del df_addresses['BARRIO'] 
    #print(df_addresses) 

    try:
        df_addresses.to_excel(addresses_path.split('/')[-1].split('.')[0]+'_estructura_final.xlsx', index=False) 
    except:
        df_addresses.to_csv(addresses_path.split('/')[-1].split('.')[0]+'_estructura_final.csv', index=False, encoding='utf-8-sig') 
    end_time = time.time()
    duration_hr = ((end_time - start_time)/60)/60
    print('procedimiento finalizado .... Nos vemos mañana') 
    print("Esto tardo %.2f horas" % (duration_hr))

if __name__ == '__main__':
    # To parallelize pandas operations
    from distributed import Client
    import modin.pandas as pd
    client = Client()
    # execute the principal function
    main()