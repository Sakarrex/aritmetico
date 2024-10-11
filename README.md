# Codificación aritmetica
## Descripción
El proyecto contiene el codigo en pyhton para realizar la compresión aritmetica de un archivo texto y luego su descompresión.
Para esto se divide el texto en bloques de tamaño fijo los cuales son lo que se les asigna un valor decimal y qu eluego se usaran para decodificar.

## Funcionamiento 
El codigo lee un txt (en este caso de ejemplo se encuentra una copia del quijote) y determina las probabilidades individiales de aparición de cada caracter. 
Una vez que se tienen las probabilidades independientes se lee otra vez el txt armando bloques los cuales convierten en un valor decimal, a través de divisones sucesivas de los intervalos de probabilidades, que se añaden a un listado.
Cuando se termian de leer todo el archivo se tendra una lista con todos los codigos que corresponden a cada uno de los bloques.
Luego para descomprimir se vuelve a realizar la división de intervalos hasta identificar los caracteres originales.
Los 2 parametros principales a modificar son la cantidad de decimales de precisión para los codigos asi como la cantidad de caracteres a leer por bloque, estos se establecieron a través de prueba y error par cada txt usado 
(para este ejemplo se usan bloques de 200 caracteres y precisión de 1000 decimales después de la coma).

## Dependencias
No se utilizaron bibliotecas externas a las ya presentes en python.
