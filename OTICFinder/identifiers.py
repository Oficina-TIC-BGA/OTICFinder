import re
import numpy as np 
from helpers import seeking_belonging 

def regex_identifier(dir, data, df_bucaramanga, df_floridablanca, df_giron, pattern_general):
    if dir != 'nan':
        # buscar en que barrios y ciudades puede haber una coincidencia
        total_asign = seeking_belonging(dir, df_bucaramanga, df_floridablanca, df_giron)            
        # Buscar si hay algun patron para otra ciudad)
        # construir el patron para buscar ciudades fuera del area metropolitana consideradas
        matches_found = re.findall(pattern_general, dir)
        # finalmente tomar una decision en que barrio y ciudad colocar 
        if len(total_asign) == 1:
            # colocar la unica que encontro
            ciudad = str(np.squeeze(list(total_asign.keys())))
            if len(matches_found) == 0:
                dir = dir + str(', '+ciudad.lower())
                #print('Opción 1 {}'.format(dir))
                  
            elif len(matches_found) == 1:
                # en caso de que haya una coincidencia en ciudad dejar esa
                dir = dir + str(', '+matches_found[0].lower())
                #print('Opción 2 {}'.format(dir))
   
            else: # cuando hay una coincidencia y muchas en las ciudades
                # seleccionar el que mas veces se repite en las listas
                names, counts = np.unique([ciudad]+matches_found, return_counts=True)
                votos = names[np.argsort(counts)][::-1] # ordenar mayor a menor
                if len(re.findall(re.compile(votos[0].lower().strip(), re.IGNORECASE), dir))==0: 
                    # para no repetir info
                    dir = dir + str(', '+votos[0].lower())
                #print('Opción 3 {}'.format(matches, ciudad))


        elif len(total_asign) > 1: # # TODO decidir que hacer con multiples coincidencias
            # analizar si hay algo en base de datos y en coincidencias
            ciudades = list(total_asign.keys())
            if len(matches_found) == 0:
                # seleccionar el que mas veces se repite en las listas
                names, counts = np.unique(ciudades, return_counts=True)
                votos = names[np.argsort(counts)][::-1] # ordenar mayor a menor
                if len(re.findall(re.compile(votos[0].lower().strip(), re.IGNORECASE), dir))==0: 
                    # para no repetir info
                    dir = dir + str(', '+votos[0].lower())    
                    #print('Opción 4 {}'.format(dir)) 

            elif len(matches_found) > 0:
                names, counts = np.unique(ciudades+matches_found, return_counts=True)
                votos = names[np.argsort(counts)][::-1] # ordenar mayor a menor
                seleccion = votos[0]
                dir = dir + str(', '+seleccion.lower())
                #print('Opción 5 {}'.format(dir))

        else:# cuando es cero
            if len(matches_found) == 0: # No hay ninguna información
                if dir!='nan' and dir!='sin informacion' and len(dir)>=3:
                    dir = dir + str(', bucaramanga')
                    #print('Opción 6 {}'.format(dir))
                else :
                    dir = np.nan    
                    #print('Opción nan {}'.format(dir))

            elif len(matches_found) == 1:
                dir = dir + str(', '+matches_found[0].lower())
                #print('Opción 7 {}'.format(dir)) 

            else:
                names, counts = np.unique(matches_found, return_counts=True)
                votos = names[np.argsort(counts)][::-1] # ordenar mayor a menor
                seleccion = votos[0]
                dir = dir + str(', '+seleccion.lower())
                #print('Opción 8 {}'.format(dir))

    else:# se puede decir que coloque el municipio
        dir = np.nan
    #print('-->',dir)                           
    return dir