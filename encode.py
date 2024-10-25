
import copy

import sys
import os
from struct import *


precision = 7 #10 ** precision para redondear probabilidades a enteros
cantchar = 1400 #1400
archivo = "quijote.txt"
potencia_max = (2**13) # 2**13
    
def crearintervalos(probabilidades,total):
    intervals = {}
    low = 0
    for symbol, prob in probabilidades.items():
        if prob == 0:
            continue
        high = round(low + prob/total * 10 ** precision )
       
        intervals[symbol] = (low, high)
        low = high
    return intervals

def codificar(prob,total):
    
    probabilidades = copy.deepcopy(prob)
  
    #Inicializar el intervalo [low, high) para todo el proceso
    current_low = 0
    current_high = (1 << potencia_max) - 1 

  
    #inicializdo band y contadores
    band = True
    textocodificar = ""
    codigos = []
    
    buffer = b''
    with open(archivo, 'rb') as f:
        
        while band:
            #leo un byte
            byte = f.read(1)
            #si ya no queda bytes para leer
            if not byte:
                band = False

            byte = buffer + byte
            try:
                #me fijo si no hay byte cortado
                textocodificar += byte.decode("utf-8")
                buffer = b''
                #si ya lei sufienctes bytes
                if len(textocodificar) < cantchar and band:
                    continue
                #creo intervalos con probabilidades correspondientes
                intervalos = crearintervalos(probabilidades,total)
                total_frecuencias = sum(intervalos[s][1]-intervalos[s][0] for s in intervalos)
               
                for c in textocodificar:
                    try:
                    #disminuyo en 1 pq ya lei el caracter
                        probabilidades[c] -=1
                        total -= 1
                    except:
                        print(textocodificar)
                    
                    #obtengo el rango de ese caracter
                    symbol_low, symbol_high = intervalos[c]
                    # rango total con el q estoy trabajando
                    range_width = current_high - current_low + 1
                    
                    # Actualizar el intervalo [low, high) basado en el símbolo actual
                    current_high = current_low + (range_width * symbol_high // total_frecuencias) - 1 
                    current_low = current_low + (range_width * symbol_low // total_frecuencias)
                #limpio texto y reinicio intervalos
                
                textocodificar = ""
                # El punto medio del intervalo final será el código
                codigos.append(current_low)
                current_low = 0
                current_high = (1 << potencia_max) -1 
            
            except UnicodeDecodeError:
                buffer = byte

    return codigos

def inicializar():
    
    prob = {}
    total = 0
    buffer = b''
    with open(archivo, 'rb') as f:
        while True:
            
            byte = f.read(1)

            if not byte:
                break
            byte = buffer + byte
            try:
                decodificado = byte.decode("utf-8")
                buffer = b''
                if decodificado in prob.keys():
                    prob[decodificado] += 1
                else:
                    prob[decodificado] = 1
                total+=1
            except UnicodeDecodeError:
                buffer = byte

        
    
    prob = sorted(prob.items(), key= lambda x:x[1], reverse=True)
    
    probord = {}
    for i in prob:
        probord[i[0]] = i[1]
    
    #print(probord)
    #retorno total menos 1 pq no se donde se agregar un caracter de mas al final
    return probord,total-1

def escribir_archivo(codigos,probabilidades,total):
    #El formato va a ser precision 4B,cant_char 4B,potencia_max 4B,total 4B,cant_caracteres 4B,cant codigos 4B,tamaño de prob 1B,tamaño de codigo 4B,char1 1B (pq es ascii),probchar1 (tamaño de prob)B,...,codigo1 (tamaño de codigo) B, codigo2,... 
    with open("comprimido.cmp","wb") as file:
        
        #precision 4B,cant_char 4B,potencia_max 4B,total 4B,cant_caracteres 4B,cant codigos 4B
        file.write(pack("iiiiii",precision,cantchar,potencia_max,total,len(probabilidades),len(codigos)))
    
        
        #todos los codigos son de igual tamaño (ej 28 B para probs y 300 B para codigos con el quijote)
        tamaño_probs = sys.getsizeof(list(probabilidades.values())[0])
        tamaño_codigo = sys.getsizeof(codigos[0])
        
        #tamaño en B de cada probabilidad 1B
        file.write(tamaño_probs.to_bytes(1,"big")) 
        #tamaño en B de cada codigo 4B
        file.write(tamaño_codigo.to_bytes(4,"big")) 
        #escribo las probabilidades
        for key,value in probabilidades.items():
            file.write(key.encode("utf-8"))
            file.write(value.to_bytes(tamaño_probs,"big"))
        
        #Escribo los codigos
        
        for i in codigos:
            file.write(i.to_bytes(tamaño_codigo,"big"))



probabilidades,total = inicializar()



codigos = codificar(probabilidades,total)


escribir_archivo(codigos,probabilidades,total)

print(f"original: {os.path.getsize(archivo)}")
print(f"comprimido: {os.path.getsize("comprimido.cmp")}")







