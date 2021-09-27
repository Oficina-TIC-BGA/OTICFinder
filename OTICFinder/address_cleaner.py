# all functions for address cleaning
import re 

def regex_cleaner(string):
    """
    string: direccion tipo:string
    return: direccion filtrada
    """
    string = str(string)
    # pattern 1-3: Colocar espacio entre los numero y letras, numeros y signos (#-,)
    for typ, regex in zip(['finditer', 'finditer', 'finditer'],['[a-z#-,]\d', '\d[a-z#-,]', '[a-z](,|#|-)']): 
        pattern = re.compile(regex, re.IGNORECASE)
        if typ=='sub':
            string = re.sub(pattern, '', string)
        elif typ=='finditer':
            match = re.finditer(pattern, string)
            if match:
                for match_iter in match:
                    found_pattern = match_iter.group()
                    index = string.index(found_pattern)
                    string = string[:index+1] + ' ' + string[index+1:]

    # regex para reemplazar palabras comunes
    common_words = {}
    common_words['carrera'] = ['(?<![\w\d])c*[a-z]r+e+r+[a-z]*\s','carreta','carr+[a-z][ra]*\s*','(?<![\w\d])ca*rr\s','[c|k]r[a|.]*\s','CDRA\s',
                               '\A[k|c]\s', 'catrera', '(?<![\w\d])car.\s', '(?<![\w\d])crq.*\s']
    #common_words['carrera'] = ['carrear\s','carrea\s','\bK','KRA', 'CDRA\s','CRA', 'KR', '\s*CR\s', '\s*carre\s','ARRERA', 'CARRRERA', 'CARRRA', 'car\s','CRR','CARERRA', '\s*CARR\s', '\s*carr\s', '\s*CRARREA\s','CARRERA']
    common_words['calle'] = ['(?<![\w\d])ca+[l|k]+[a|e|r]*\s','(?<![\w])ce*a\s',
                             '[c|v]*[a-z]*a*ll[e|m|b]\s', '(?<![\w\d])[x|c][c|l]+[e|.|i]*\s','(?<![\w])c*alle[a-z]\s']
    #common_words['calle'] = ['CLL', 'CL', 'CLEE', '\s*CALL\s','\s*CC\s', 'CLLE', 'cale\s']
    common_words['numero'] = ['\bNUM\b', '\sNUM\s', 'NU*MERO', 'NÚMERO', '\sNO\s', 'NRO', 'n[^a-z0-9-\s]','n[ª|º]']
    common_words['diagonal'] = ['(?<![\w\d])DIAG.*\s', '(?<![\w\d])DIA[G|F]ONAL\s', '(?<![\w\d])DI*G.*\s']
    common_words['transversal'] = ['(?<![\w])(?:tr)*tr*[a|q]*n*s*[b|v|c](?:e[r|t|l]*s*[a|q]l+)*(?![\w])',
                                   '(?<![\w])trv\s','(?<![\w])tra*n*s\s','trasn*versal*\s','trnasversal*\s','(?<![\w])t*rans*v*\s']
    #common_words['transversal'] = ['TRANSVERSAL','trns\s', '\sTR\s','TRV','TRANSV', 'TV', 'TRANVERSAL', 'TRANSV', 'TRANSSV\s','TRASVERSAL', 'TRANV', 'TANSVERSAL', 'TRANVS', '\s*trans\s']
    common_words['circunvalar'] = ['(?<![\w])(?:cir)*[c|v]i[r|n]cu*[n|m][v|b|u]a*la[n|r]v*\s','(?<![\w])circ*cunv*\s',
                                  '(?<![\w])circn*v\s', '(?<![\w])circunva\s', '(?<![\w])circum\s','(?<![\w])cc*v\s','(?<![\w])cir*c\s']
    #common_words['circunvalar'] = ['CIRCUMBALAN\s','CIRCUMBALAR\s','circunvalara','VIRCUNVALAR','CIRCUNVALAR', '\sCIRC\s', '\sCIR\s', 'CCV', 'CV', 'circunvalarv', 'CIRCCUN\s', 'circircunvalar\s']
    common_words['apartamento'] = ['apae?rt[a|e]m[a|e][n|m]to*\s', 'ap[r|a]*t[a|o|0|p]{1,2}[:|.]?\d?\s', 'aparatamento',
                                   'apart*a*\s', '\sapartame\s', '\saparta\s','\sAPRO\s','\sap[p|t]*\s', '\spto\s', '\saoto\s']
    #common_words['apartamento'] = ['\sAPTO\s', '\sAPP\s' ,'APTO ','\sAPTO', 'ap\s', 'aparatamento','apartamento*', 'apar\s','apart\s', 'APRO\s', '\sapato', '\sapt', '\bAPTO\b', '\saparta\s', '\sapartame\s']
    common_words['torre'] = ['(?<![\w\d])t[e|o|p]rr*e[a-z]{1,2}\s','(?<![\w\d])tor*r*\s', '(?<![\w\d])t\s[-0-9]*\s', '(?<![\w\d])tr*\s']
    common_words['bloque'] = ['(?<![\w\d])bloque*[a-z]\s', '(?<![\w\d])blo*[q|k]*e*\s']    
    common_words['edificio'] = ['edi*fici*o', '(?<![\w\d])edific\s', '(?<![\w\d])edifi*[c|v]io\s', '(?<![\w\d])edi*f*i*o*\s', '(?<![\w\d])efd\s']
    common_words['avenida'] = ['(?<![\w\d])a+ven+i*[d|s|n]i*ad*\s','(?<![\w\d])ave*n*.*\s', '(?<![\w\d])a*vda\s','(?<![\w\d])avenia\s']
    common_words['quebradaseca'] = ['quebraceca\s','qdaseca', 'quebrada\sseca']#'quebrada\s(?![\w])'
    common_words['barrio'] = ['(?<![\w\d])[b|v]a*r*ri*o*\s']
    common_words['sector'] = ['(?<![\w\d])sect*o*r*\s'] 
    common_words['kilometro'] = ['(?<![\w\d])km\s*', 'kil[o|ó]*metr[o|i]*\s', 'kimoltro\s', '(?<![\w\d])kil\s']
    common_words['vereda'] = ['(?<![\w\d])v[d|r]a.*\s', '(?<![\w\d])ver.*\s', '(?<![\w\d])[b|v]ereda*\s']
    common_words['urbanizacion'] = ['urbani*zaci*[ó|o]n*\s','(?<![\w\d])urb\s']
    common_words['manzana'] = ['(?<![\w\d])m[a|q]n*z[a|q]*[b|n|s]*a*\s','(?<![\w\d])mz\s', '(?<![\w\d])manazana\s'] 
    common_words['casa'] = ['(?<![\w\d])ca[s|d][z|a]*\s', '(?<![\w\d])csa\s'] 
    common_words['peatonal'] = ['(?<![\w\d])a*p[e|r]a[t|r]on*a[k|l]*\s', 'peanotal\s']
    common_words['piso'] = ['(?<![\w\d])pi[s|z|d]?[i|o|p]?[b|c]?\s', '(?<![\w\d])p[o|a]s[i|o]\s']
    common_words['bulevar'] = ['(?<![\w\d])bo*u[l|o][e|u|a][v|b][a|e][r|l|s|d]d*\s']  
    common_words['autopista'] = ['(?<![\w\d])autopis*[r|t]*a*\s'] 
    common_words['etapa'] = ['(?<![\w\d])ea*tap*a\s', '(?<![\w\d])epata\s', '(?<![\w\d])et\s']   
    common_words['paralela'] = ['paralela\s'] 
    common_words['occidente'] = ['o[c|b][c|s]idente\s', '(?<![\w\d])occ\s']      
    
    # crear patrones a buscar y reemplazar
    pattern_carrera = re.compile(r'|'.join(common_words['carrera']), re.IGNORECASE)
    pattern_calle = re.compile(r'|'.join(common_words['calle']), re.IGNORECASE)
    pattern_diagonal = re.compile(r'|'.join(common_words['diagonal']), re.IGNORECASE)
    pattern_transversal = re.compile(r'|'.join(common_words['transversal']), re.IGNORECASE) 
    pattern_circunvalar = re.compile(r'|'.join(common_words['circunvalar']), re.IGNORECASE) 
    pattern_apto = re.compile(r'|'.join(common_words['apartamento']), re.IGNORECASE)
    pattern_torre = re.compile(r'|'.join(common_words['torre']), re.IGNORECASE)
    pattern_bloque = re.compile(r'|'.join(common_words['bloque']), re.IGNORECASE)
    pattern_edificio = re.compile(r'|'.join(common_words['edificio']), re.IGNORECASE)

    pattern_avenida = re.compile(r'|'.join(common_words['avenida']), re.IGNORECASE)
    pattern_quebradaseca = re.compile(r'|'.join(common_words['quebradaseca']), re.IGNORECASE)
    pattern_barrio = re.compile(r'|'.join(common_words['barrio']), re.IGNORECASE)
    pattern_sector = re.compile(r'|'.join(common_words['sector']), re.IGNORECASE)
    pattern_kilometro = re.compile(r'|'.join(common_words['kilometro']), re.IGNORECASE)
    pattern_vereda = re.compile(r'|'.join(common_words['vereda']), re.IGNORECASE)
    pattern_urbanizacion = re.compile(r'|'.join(common_words['urbanizacion']), re.IGNORECASE)
    pattern_manzana = re.compile(r'|'.join(common_words['manzana']), re.IGNORECASE)
    pattern_casa = re.compile(r'|'.join(common_words['casa']), re.IGNORECASE)
    pattern_piso = re.compile(r'|'.join(common_words['piso']), re.IGNORECASE)
    pattern_bulevar = re.compile(r'|'.join(common_words['bulevar']), re.IGNORECASE)
    pattern_autopista = re.compile(r'|'.join(common_words['autopista']), re.IGNORECASE)
    pattern_etapa = re.compile(r'|'.join(common_words['etapa']), re.IGNORECASE)
    pattern_paralela = re.compile(r'|'.join(common_words['paralela']), re.IGNORECASE)
    pattern_peatonal = re.compile(r'|'.join(common_words['peatonal']), re.IGNORECASE)
    pattern_occ = re.compile(r'|'.join(common_words['occidente']), re.IGNORECASE) 

    pattern_num = re.compile(r'|'.join(common_words['numero']), re.IGNORECASE)  

    patterns = [pattern_carrera, pattern_calle, pattern_diagonal, 
                pattern_transversal, pattern_circunvalar, pattern_apto, pattern_torre, 
                pattern_bloque, pattern_edificio, pattern_avenida, pattern_quebradaseca, 
                pattern_barrio, pattern_sector, pattern_kilometro, pattern_vereda, pattern_urbanizacion,
                pattern_manzana, pattern_casa, pattern_piso, pattern_bulevar, pattern_autopista, 
                pattern_etapa, pattern_paralela, pattern_peatonal, pattern_num, pattern_occ]
    
    # Cambiar por algún estándard definido
    for pattern, p in zip(patterns,[' KR ', ' CL ',' DG ', ' TV ', ' CV ',
                                    ' apartamento ', ' torre ', ' bloque ' , ' ED ', ' AV ' ,
                                    ' quebradaseca ', ' BR ', ' sector ', ' KM ', ' vereda ',
                                    ' UR ', ' manzana ', ' casa ', ' piso ', ' bulevar ',
                                    ' AU ', ' ET ', ' paralela ', ' PT ',' # ', ' oeste ']):
        matches = re.finditer(pattern, string)
        if matches:
            for match in matches:
                found_pattern = match.group()
                string = string.replace(found_pattern, p)
                if p != ' ':
                    pattern_tem = re.compile(p)
                    found_tem = re.search(pattern_tem, string)
                    #print('tem',found_tem)
                    try:
                        if found_tem and dir[found_tem.end()+1]!= ' ':
                            string = string[:found_tem.end()] + ' ' + string[found_tem.end():]
                    except:
                        pass        
            
    
    # pattern: Quitar múltiples espacios en blanco  
    string = re.sub(re.compile('\s{2,5}'), ' ', string)

    # pattern: para eliminar piso
    string = re.sub(re.compile('|'.join(['\squinto*\spiso','\sprimero*\spiso','\ssegundo\spiso','\stercero*\spiso',
                            '\scuarto\spiso', '\s?piso\s?\d{1,2}\s?', '\spiso\suno', '\spiso\sdos', '\spiso\stres', '\spiso\scuatro',
                            '\s\d{1,1}\spiso','\spiso']), re.IGNORECASE), ' ', string)
    # pattern: para eliminar apartamento
    string = re.sub(re.compile('|'.join(['\sapartamento\s[a-z-#]?\s?\d{1,4}', '\sapartamento']), re.IGNORECASE), ' ', string)
    # pattern: para eliminar torre
    string = re.sub(re.compile('|'.join(['\storre\s+[a-z0-9]{1,6}\s*\d{0,4}\s?']), re.IGNORECASE), ' ', string)
    # pattern: para elimiar bloque
    string = re.sub(re.compile('|'.join(['\sbloque\s-*\s*[a-z0-9]{1,3}\s']), re.IGNORECASE), ' ', string)
    # pattern: para eliminar manzana
    string = re.sub(re.compile('|'.join(['\smanzana\s-*\s*[a-z0-9]{1,3}\s?']), re.IGNORECASE), ' ', string)
    # pattern: para eliminar casa
    string = re.sub(re.compile('|'.join(['\scasa\s*-*\s*[a-z0-9]{1,3}\s?']), re.IGNORECASE), ' ', string)
    # pattern: Eliminar lote y local
    string = re.sub(re.compile('|'.join(['\slote\s*-*\s*[a-z0-9]{0,3}\s?']), re.IGNORECASE), ' ', string)
    string = re.sub(re.compile('|'.join(['\sloca*l*\s*-*\s*[a-z0-9]{0,3}\s?']), re.IGNORECASE), ' ', string)
    # pattern: Quitar simbolos por espacios         
    string = re.sub(re.compile('[-_#,.:()<>/~]'), ' ', string)
    # pattern: Quitar múltiples espacios en blanco  
    string = re.sub(re.compile('\s{2,5}'), ' ', string)
    # suponiendo que solo se encuentra un patron por direccion
    pattern2 = re.compile('\s\d\d\d\d\s?', re.IGNORECASE)
    match = re.search(pattern2, string)
    if match:
        x0, xt = match.span()
        rest = string[x0+3:] 
        string = string[:x0+3] + ' ' + rest      
    # pattern: quitar elementos no deseados
    pattern3 = re.sub(re.compile(r'2DO|1RO|1ERO|NO ENCONTRADO|ENTRADA|\spi\s+\d*|ninguno|ninguna|na|sin dato|sin informaci[ó|o]n', re.IGNORECASE),'', string)        

    # pattern: Quitar múltiples espacios en blanco  
    string = re.sub(re.compile('\s{2,5}'), ' ', string)
    if len(str(string))<5:
        string = 'nan'

    return string.lower().strip()  

def regex_neighbourhood(lookup_table, string):
    #print(string)
    for i, dict_ in lookup_table.items():
        pattern = re.compile('(?<![\w\d])'+dict_['key']+'(?![\w\d])', re.IGNORECASE)
        #print(pattern)
        string = re.sub(pattern, dict_['value'], string)
    #print(string)

    return string

