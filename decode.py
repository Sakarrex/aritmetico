import struct
import copy

precision = 0 #10 ** precision para redondear probabilidades a enteros, no afecta mucho realmente
cantchar = 0
archivo = "quijote.txt"
potencia_max = 0

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

def decodificar(codigos,prob,long):
    
    probabilidades = copy.deepcopy(prob)
    total = long 
    texto = ""
    
    contador = 0
    #mientras no lea todos los caracteres
   
    #por cada codigo
    for codigo in codigos:
        #reinicio intervalo actual
        actualsuperior = (1<<potencia_max)-1
        actualinferior = 0
        #creo intervalo para este nuevo codigo
        intervalos = crearintervalos(probabilidades,total)
        total_frecuencias = sum(intervalos[s][1]-intervalos[s][0] for s in intervalos)
        #inicializo rango de intervalo
        
        #por cada codigo son cantcaracteres de longitud

        for _ in range(cantchar):
            #para el ultimo codigo que puede ser menor de cantcarcteres
            if contador > long:
                break
            rango = actualsuperior-actualinferior + 1 
           
            valor = ((codigo - actualinferior + 1) * total_frecuencias - 1) // rango

            # Encontrar el símbolo que corresponde a este valor
            for symbol, (low_sym, high_sym) in intervalos.items():
                
                if low_sym <= valor < high_sym:
                    texto += symbol
                    total -=1
                    probabilidades[symbol] -= 1
                    # Actualizar los límites del intervalo
                    actualsuperior = actualinferior + (rango * high_sym // total_frecuencias) - 1
                    actualinferior = actualinferior + (rango * low_sym // total_frecuencias)
                    contador += 1
                    break
    return texto

def leer_archivo():
    #El formato va a ser precision 4B,cant_char 4B,potencia_max 4B,total 4B,cant_caracteres 4B,cant_codigos 4B,tamaño de prob 1B,tamaño de codigo 4B,char1 1B (pq es ascii),probchar1 (tamaño de prob)B,...,codigo1 (tamaño de codigo) B, codigo2,... 

    with open("comprimido.cmp","rb") as file:
        #variables globales
        globales = struct.unpack("iii",file.read(12))
        #Cantidad de caracteres totales del texto original
        total = struct.unpack("i",file.read(4))[0]
        #Cantidad de caracteres del alfabeto
        lenprob = struct.unpack("i",file.read(4))[0]
        #cantidad de codigos
        cant_codigos = struct.unpack("i",file.read(4))[0]
        #Tamño en bytes para cada probabilidad
        cantBProb = int.from_bytes(file.read(1),"big")
         #Tamño en bytes para cada codigo 
        cantBCodigo = int.from_bytes(file.read(4),"big")
        


        #guardo las variables globales
        global precision 
        global cantchar
        global potencia_max
        precision = globales[0]
        cantchar = globales[1]
        potencia_max = globales[2]
        
        #leo cada caracter y su probabilidad
        contador = 0
        probabilidades = {}
        buffer = b""
        band = True
        
        while band :
            try:
                #leo un byte
                byte = file.read(1)

                byte = buffer + byte
                caracter = byte.decode()
                buffer = b''
                contador += 1
                probablidad = int.from_bytes(file.read(cantBProb))
                probabilidades[caracter] = probablidad
                if contador == lenprob:
                    band = False
            except UnicodeDecodeError:
                buffer = byte 
        
        #ya tengo las probabilidades de cada caracter, faltan los codigos
        codigos = []
        
        for _ in range(cant_codigos):
            codigos.append(int.from_bytes(file.read(cantBCodigo),"big"))
        

    texto = decodificar(codigos,probabilidades,total)

    with open("nuevo.txt","w",encoding="utf-8",newline="") as f:
        f.write(texto)

        
        
leer_archivo()
