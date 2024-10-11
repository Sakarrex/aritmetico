import time
import copy
from decimal import Decimal,getcontext
import sys
import os
getcontext().prec = 1000
cantchar = 200
archivo = "quijote.txt"

def valchar():
    pass

def codificar(prob,total):



    probabilidades = copy.deepcopy(prob)
    
    #Inicializar el intervalo [low, high) para todo el proceso
    current_low = Decimal(0.0)
    current_high = Decimal(1.0)

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
                
                for c in textocodificar:
                    try:
                        #disminuyo en 1 pq ya lei el caracter
                        probabilidades[c] -=1
                        total -= 1
                    except:
                        print(textocodificar)

                    symbol_low, symbol_high = intervalos[c]
                    range_width = current_high - current_low
                    
                    # Actualizar el intervalo [low, high) basado en el símbolo actual
                    current_high = current_low + range_width * symbol_high
                    current_low = current_low + range_width * symbol_low
                #limpio texto y reinicio intervalos
                
                textocodificar = ""
                # El punto medio del intervalo final será el código
                codigos.append((current_low + current_high) / 2)
                current_low = Decimal(0.0)
                current_high = Decimal(1.0)
            
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
    
    return probord,total

def decodificar(codigos,prob,long):
    probabilidades = copy.deepcopy(prob)
    total = long 
    texto = ""
    
    contador = 0
    #mientras no lea todos los caracteres
   
    #por cada codigo
    for c in codigos:
        #reinicio intervalo actual
        actualsuperior = 1
        actualinferior = 0
        #creo intervalo para este nuevo codigo
        intervalos = crearintervalos(probabilidades,total)
        #inicializo rango de intervalo
        
        #por cada codigo son cantcaracteres de longitud

        for i in range(cantchar):
            #para el utlimo codigo que peude ser menor a cantcarcteres
            if contador > long:
                break
            rango = actualsuperior-actualinferior
            for simbolo in intervalos:
                #calculo intervalo del simbolo
                simbolo_inf , simbolo_sup =  intervalos[simbolo]
                nuevo_inf = actualinferior + rango * simbolo_inf
                nuevo_sup = actualinferior + rango * simbolo_sup
                #si entra
                if nuevo_inf <= c and nuevo_sup > c:

                        texto += simbolo
                        total -=1
                        probabilidades[simbolo] -= 1
                        actualsuperior = nuevo_sup
                        actualinferior = nuevo_inf
                        contador += 1
                        break
                    
                        
        
    return texto
       

    
def crearintervalos(probabilidades,total):
    intervals = {}
    low = Decimal(0.0)
    for symbol, prob in probabilidades.items():
        if prob == 0:
            continue
        high = low + Decimal(prob/total)
        intervals[symbol] = (low, high)
        low = high
    return intervals

def escribir_archivo(texto):
    file= open("nuevo.txt","w",encoding=("utf-8"))
    file.write(texto)
    file.close()
    
if __name__ == "__main__":
    
    inicio = time.time()
    
    
    probabilidades,total = inicializar()
    
    
    
    codigos = codificar(probabilidades,total)
    print("termino codigos")

    codificacion = time.time()
    print(f"demora en codificar: {codificacion-inicio} seg")
    
    textodecodificado = decodificar(codigos,probabilidades,total)
    fin = time.time()

    print(f"demora en decodificar: {fin-codificacion} seg")

    print(f"Demora de total: {fin - inicio} seg")
    
    print(textodecodificado)
    
    escribir_archivo(textodecodificado)
    
    print(f"tamaño texto (Bytes): {os.path.getsize(archivo)}")
    print(f"tamaño de codigos (Bytes): {sys.getsizeof(codigos)}")

    print(os.path.getsize(archivo)>sys.getsizeof(codigos))

  
   #zen cant 2 decimal 200
   #quijote cant 200 decimal 2000