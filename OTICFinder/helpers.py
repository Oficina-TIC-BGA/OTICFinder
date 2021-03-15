import re
import unicodedata
import numpy as np
import shapely.wkt
import shapely.speedups
from shapely.geometry import Point, Polygon 
from collections import defaultdict

def seeking_belonging(dir, df_bucaramanga, df_floridablanca, df_giron):
    total_asign = defaultdict(list)
    for c, df_c in zip(['bucaramanga', 'floridablanca', 'giron'],[df_bucaramanga, df_floridablanca, df_giron]):
        # paso 1: Unir columnas SECTOR - CONJUNTO - EDIFICIO para cada barrio y buscar
        for row in df_c.keys():
            founded = pattern_row(df_c[row], dir)
            #print(founded)
            if len(founded)>0:
                # esto quiere decir que hubo al menos un concidencia para ese barrio
                # asignar el barrio a la ciudad
                total_asign[c].append(df_c[row]['BARRIO'])
    #print(total_asign)
    return total_asign    

def pattern_row(row, dir):
    # Revisar que no este nulo los campos
    #print('direccion:',dir)
    total = []
    for column in ['BARRIO','SECTOR', 'EDIFICIO', 'CONJUNTO']: 
        if isinstance(row[column], str): # si no es vacio
            total = total + [j.strip() for j in row[column].strip().split(',')]        
    if len(total)>0: 
        pattern = re.compile(r'|'.join([i for i in total]), re.IGNORECASE)
        #print(pattern, '##############')
        result = re.findall(pattern, dir)
        #print('result pattern:', result)
    else:
        result = total  
    #print(dir, result)      
    return result  

def get_score(x):
    if isinstance(x, dict):
        r = x['score']
    elif isinstance(x, str):    
        r = eval(x)['score']        
    else:
        r = 0.0      
    return r   

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_city(x, pattern_general):
    if isinstance(x, dict):
        r = x['address']
        match_found = re.findall(pattern_general, remove_accents(r))
        if len(match_found) >= 1:
            r = remove_accents(match_found[0])
        else:
            r = None   
    elif isinstance(x, str):    
        r = eval(x)['address']        
        match_found = re.findall(pattern_general, remove_accents(r))
        if len(match_found) >= 1:
            r = remove_accents(match_found[0])
        else:
            r = None   
    else:     
        r = None   
    return r 

def get_neighbourhood(x):
    if isinstance(x, dict):
        r = x['address']
        split_r = r.split(',')
        if len(split_r)<3:
            r = None
        elif len(split_r)==4 or len(split_r)==3:
            numbers = re.compile(r'[0-9]+')
            if len(re.findall(numbers, split_r[0]))==0:
                r = remove_accents(split_r[0].strip())
            else:
                r = remove_accents(split_r[1].strip())   
        elif len(split_r)>=5:  
            r = remove_accents(split_r[1].strip())  
        else:
            r = None

    elif isinstance(x, str):    
        r = eval(x)['address']        
        r = x['address']
        split_r = r.split(',')
        if len(split_r)<=3:
            r = None
        elif len(split_r)==4 or len(split_r)==3:
            numbers = re.compile(r'[0-9]+')
            if len(re.findall(numbers, split_r[0]))==0:
                r = remove_accents(split_r[0].strip())
            else:
                r = remove_accents(split_r[1].strip())   
        elif len(split_r)>=5:  
            r = remove_accents(split_r[1].strip())  
        else:
            r = None
    else:
        r = None        
    return r      


def search_neighbourhood(datos_barrios, coords):
    if isinstance(coords, tuple):
        lon = coords[0] 
        lat = coords[1]
    else:    
        lon = np.nan
        lat = np.nan
    # crear el punto
    point_x_y = Point(lon, lat)
    # Validar que las coordenadas no esten vacias
    collect_intersections_bar = None
    if np.isnan(point_x_y)[0]!=True:
        # leer los poligonos de los barrios
        for i in datos_barrios.keys():
            polygon_string = datos_barrios[i]['geometry']
            # Extraer el nombre barrio
            name = datos_barrios[i]['NOMBRE']
            # Convertir el poligono string al objeto poligono
            polygon = shapely.wkt.loads(polygon_string)
            if polygon.contains(point_x_y):
                # contiene el punto totalmente
                collect_intersections_bar = name
                break
            elif polygon.intersects(point_x_y):
                # opcional si se intersectan el barrio y el punto 
                collect_intersections_bar = name 
                break

    return collect_intersections_bar

def search_nearby(datos, coords):
    key='NOMBRE'
    distancia = np.inf
    if isinstance(coords, tuple):
        lon = coords[0] 
        lat = coords[1]
    else:    
        lon = np.nan
        lat = np.nan
    # crear el punto
    point_xy = Point(lon, lat )   
    for i in datos.keys():
        polygon_string = datos[i]['geometry']
        # Extraer el nombre barrio
        name = datos[i][key]
        # Convertir el poligono string al objeto poligono
        polygon = shapely.wkt.loads(polygon_string)
        distancia_pts = polygon.distance(point_xy)
        #distancia_pts = polygon.hausdorff_distance(point_xy)

        if distancia_pts < distancia:
            distancia = distancia_pts
            result = name  
    
    return result  

                                         