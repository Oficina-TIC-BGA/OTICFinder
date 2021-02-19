# all functions for address cleaning
import re 

def regex_cleaner(dir):
    """
    input:
        dir: text address (type:string)
    return:
        dir: Address cleaned (type:string)
    """
    dir = str(dir)
    #print('Inicial {}'.format(dir))
    # definir las palabras comunes para tratar de estandarizar las direcciones
    # TODO: Resumir expresiones regulares
    common_words = {} 
    common_words['carrera'] = ['carrear\s','carrea\s','\bK','KRA', 'CDRA\s','CRA', 'KR', '\s*CR\s', '\s*carre\s','ARRERA', 'CARRRERA', 'CARRRA', 'car\s','CRR','CARERRA', '\s*CARR\s', '\s*carr\s', '\s*CRARREA\s','CARRERA']
    common_words['calle'] = ['CLL', 'CL', 'CLEE', '\s*CALL\s','\s*CC\s', 'CLLE', 'cale\s']
    common_words['diagonal'] = ['DIAG\s', 'DIAGONAL', 'DG', '\sDIG\s']
    common_words['transversal'] = ['TRANSVERSAL','trns\s', '\sTR\s','TRV','TRANSV', 'TV', 'TRANVERSAL', 'TRANSV', 'TRANSSV\s','TRASVERSAL', 'TRANV', 'TANSVERSAL', 'TRANVS', '\s*trans\s']
    common_words['numero'] = ['\bNUM\b', '\sNUM\s', 'NUMERO', 'NMERO', 'NÚMERO', '#', '\sNO\s', 'NRO', 'Nª','Nº','N°']
    common_words['circunvalar'] = ['CIRCUMBALAN\s','CIRCUMBALAR\s','circunvalara','VIRCUNVALAR','CIRCUNVALAR', '\sCIRC\s', '\sCIR\s', 'CCV', 'CV', 'circunvalarv', 'CIRCCUN\s', 'circircunvalar\s']
    common_words['avenida'] = ['AV\s+', 'AVENIDA', '\sAVD\s','AVDA', 'AVEN\s', 'avn', '\svda\s', '\savd\s']
    common_words['quebradaseca'] = ['qdaseca', 'quebrada seca', 'quebrada']
    common_words['edificio'] = ['edif*\s', 'edf', 'edificio', '\sedi\s']
    common_words['torre'] = ['tprre\s','\storr*\s', '\stor\s', '\sto\s', '\str\s', '\st\s']
    common_words['barrio'] = ['\sbrr', '\sbario\s','barrio','BARRIO', '\sbr\s', '\sbarri\s','\sbrr\s']
    common_words['apartamento'] = ['\sAPTO\s', '\sAPP\s' ,'APTO ','\sAPTO', 'ap\s', 'aparatamento','apartamento*', 'apar\s','apart\s', 'APRO\s', '\sapato', '\sapt', '\bAPTO\b', '\saparta\s', '\sapartame\s']
    common_words['bloque'] = ['BLOQUE', '\sblo\s', '\s*bloq\s']
    common_words['sector'] = ['SECTOR', '\ssect\s', '\ssec\s'] 
    common_words['kilometro'] = ['KM\s*', 'KILOMETRO', 'KM ']
    common_words['vereda'] = ['\s*VDA\s', '\s*VER\s', '\sBEREDA\s']
    common_words['urbanizacion'] = ['URBANIZAC\s', 'URBANIZACION', 'URBANIZACIÓN', 'urb']
    common_words['manzana'] = ['\s*MANZANA\s','\s*mz\s*\d+', '\s*mz\s', '\smz\s*[a-z]', '\s*manza\s', '\s*manz\s']

    # definir los patrones con las expresiones regulares
    pattern_numeros = re.compile(r'\d\s*[A-Z]\s*#', re.IGNORECASE)
    pattern_carrera = re.compile(r'|'.join(common_words['carrera']), re.IGNORECASE)
    pattern_calle = re.compile(r'|'.join(common_words['calle']), re.IGNORECASE)
    pattern_diagonal = re.compile(r'|'.join(common_words['diagonal']), re.IGNORECASE)
    pattern_transversal = re.compile(r'|'.join(common_words['transversal']), re.IGNORECASE)
    pattern_num = re.compile(r'|'.join(common_words['numero']), re.IGNORECASE)
    pattern_circunvalar = re.compile(r'|'.join(common_words['circunvalar']), re.IGNORECASE)
    pattern_avenida = re.compile(r'|'.join(common_words['avenida']), re.IGNORECASE)
    pattern_quebradaseca = re.compile(r'|'.join(common_words['quebradaseca']), re.IGNORECASE)
    pattern_edificio = re.compile(r'|'.join(common_words['edificio']), re.IGNORECASE)
    pattern_torre = re.compile(r'|'.join(common_words['torre']), re.IGNORECASE)
    pattern_apartamento = re.compile(r'|'.join(common_words['apartamento']), re.IGNORECASE)
    pattern_bloque = re.compile(r'|'.join(common_words['bloque']), re.IGNORECASE)
    pattern_sector = re.compile(r'|'.join(common_words['sector']), re.IGNORECASE)
    pattern_urbanizacion = re.compile(r'|'.join(common_words['urbanizacion']), re.IGNORECASE)
    pattern_kilometro = re.compile(r'|'.join(common_words['kilometro']), re.IGNORECASE)
    pattern_manzana = re.compile(r'|'.join(common_words['manzana']), re.IGNORECASE)
    pattern_guion = re.compile(r'-|\.|·|º|°')#|Nª|º|°
    pattern_nume2 = re.compile(r'\sNO\d|\sNUM\d', re.IGNORECASE)
    pattern_nume3 = re.compile(r'\dNO\d|\dNUM\d', re.IGNORECASE)
    pattern_final = re.compile(r'barrio|primer piso\s*|peatonal\s*\d+|manzana\s*\d+|t\d+|casa\s*\d+|piso\s*\d+|apartamento\s*\d+|torre\s*\d+', re.IGNORECASE)
    pattern_final2 = re.compile(r'conjunto residencial|torre\s[a-z]*|edificio|edificio\s*\d+|bloque\s*\d+|apartamento|manzana\s*\d+|manzana\s*[a-z]|sector\s*\d+', re.IGNORECASE)
    pattern_final3 = re.compile(r'conjunto|conj|conjunto\s*residen|segundo piso|sin dato|ninguno|direccion|local\s*\d*|piso|sector\s*[a-z]|manzana', re.IGNORECASE)
    pattern_final4 = re.compile(r'2DO|1RO|1ERO|NO ENCONTRADO|ENTRADA|PI\s+\d*|ninguno|ninguna|urbanizacion|casa\s[a-z]', re.IGNORECASE)
    #pattern_final = re.compile(r'(\s[a-z\s*]*\s*)', re.IGNORECASE)
    pattern_barrio = re.compile(r'|'.join(common_words['barrio']), re.IGNORECASE)
    pattern_std = re.compile(r'carrera|calle|avenida|diagonal|transversal|circunvalar')
    # ejecutar las expresiones regulares
    
    # Este patron separa los numeros pegados
    match_specials_num = re.search(pattern_nume2, dir)
    if match_specials_num:
        found_pattern = match_specials_num.group()
        dir = dir.replace(found_pattern[:-1], ' ')  
    # Este patron separa los numeros pegados
    match_specials_num3 = re.search(pattern_nume3, dir)
    if match_specials_num3:
        found_pattern3 = match_specials_num3.group()
        dir = dir.replace(found_pattern3[1:-1], ' ')
    # elimina signos especiales, guiones, grados, etc...
    match_specials = re.finditer(pattern_guion, dir)
    if match_specials:
        for match_guion in match_specials:
            found_pattern = match_guion.group()
            dir = dir.replace(found_pattern, ' ')
    # pega las letras de las calles si tiene
    match_numeros = re.search(pattern_numeros, dir)
    if match_numeros:
        x0, xt = match_numeros.span()
        if dir[x0+1]==' ':
            dir = dir[:x0+1] + dir[x0+1:].replace(' ','',1) 

    # ejecutar los patrones intermedios
    # cambia los patrones por su forma correcta y agrega espacios para separar        
    patterns = [pattern_carrera, pattern_calle, pattern_diagonal, pattern_transversal, pattern_num, pattern_circunvalar, 
                pattern_avenida, pattern_quebradaseca, pattern_edificio, pattern_torre, pattern_apartamento, pattern_bloque, pattern_sector,
                pattern_kilometro, pattern_barrio, pattern_urbanizacion, pattern_manzana]
    for pattern, p in zip(patterns,[' carrera ', ' calle ', ' diagonal ', ' transversal ', ' ', 'circunvalar', 'avenida', 'quebradaseca', 'edificio',
                                    ' torre ', ' apartamento ', ' bloque ', ' sector ', ' kilometro ', ' barrio ', ' urbanizacion ', ' manzana ']):
        matches = re.finditer(pattern, dir)
        if matches:
            for match in matches:
                found_pattern = match.group()
                dir = dir.replace(found_pattern, p)
                if p != ' ':
                    pattern_tem = re.compile(p)
                    found_tem = re.search(pattern_tem, dir)
                    #print('tem',found_tem)
                    try:
                        if found_tem and dir[found_tem.end()+1]!= ' ':
                            dir = dir[:found_tem.end()] + ' ' + dir[found_tem.end():]
                    except:
                        pass        
            dir = dir.strip().replace("  ", " ").replace("  ", " ").lower() 
    # Encuentra todos los patrones y los elimina 
    for pat in [pattern_final, pattern_final2, pattern_final3, pattern_final4]:
        matches_finales = re.finditer(pat, dir) 
        if matches_finales:
            for match_final in matches_finales:
                found_pattern = match_final.group()
                dir = dir.replace(found_pattern, '')
        else:    
            pass  
    dir = dir.strip().replace("  ", " ").replace("  ", " ")    
    if len(str(dir))<10:
        dir = 'nan'
    return dir 
