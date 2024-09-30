#Crear un diccionario llamado A-02
mkdir -p pcd/A-02
#Con el comando curl, procedemos a descargar los datos de las películas:
curl -O https://ai.stanford.edu/%7Eamaas/data/sentiment/aclImdb_v1.tar.gz
#Descomprimir el archivo
tar -xvf aclImdb_v1.tar.gz
#Nos vamos al directorio aclImdb, despues al directorio train y empezaremos con las reseñas positivas
cd aclImdb/train/pos
#Primero enlistamos todos los archivos que hay en el directorio pos.
#Después usaremos la sentencia grep el cual filtrara las líneas que coincidan con el patrón especificado. La opción -o nos ayudara a que solo imprima las líneas que coincidan con el patrón. 
#Seguido de esto, extraemos el segundo campo (después del delimitador “_”) de cada línea en el nombre del archivo
#Guardamos el resultado de todos los pasos anteriores en “pos_r.txt”
ls *.txt | grep -o '[0-9]\+_[0-9]\+' | cut -d'_' -f2 > pos_r.txt 
#Imprimimos al archivo creado
cat pos_r.txt
#Regresamos a la carpeta ahora de las reseñas negativas
cd ../neg
#Primero enlistamos todos los archivos que hay en el directorio neg.
#Después usaremos la sentencia grep el cual filtrara las líneas que coincidan con el patrón especificado. La opción -o nos ayudara a que solo imprima las líneas que coincidan con el patrón. 
#Seguido de esto, extraemos el segundo campo (después del delimitador “_”) de cada línea en el nombre del archivo
#Guardamos el resultado de todos los pasos anteriores en “neg_r.txt”
ls *.txt | grep -o '[0-9]\+_[0-9]\+' | cut -d'_' -f2 > neg_r.txt
#Regresamos a la carpeta pos
cd ../pos
#Primero usamos awk que sirve para buscar y manipular datos en un archivo de texto.
#La primera parte del comando: guarda cada línea del archivo pos_r.txt en un array “a” donde el índice es el número de línea NR (número de registros o líneas procesados hasta el momento).
#La segunda parte del comando: accede al elemento del array “a” que corresponde al número de registro actual “FNR” en urls_pos.txt, después imprime toda la línea actual seguida del contenido correspondiente a [FNR]
#Especificamos que vamos a devolver a tomar el archivo urls_pos.txt
#Guardamos nuestros resultados en pos_u_r.txt
awk 'NR==FNR{a[NR]=$0; next} {print $0, a[FNR]}' pos_r.txt ../urls_pos.txt > pos_u_r.txt
#Regresamos a la carpeta neg
cd ../neg
#Primero usamos awk que sirve para buscar y manipular datos en un archivo de texto.
#La primera parte del comando: guarda cada línea del archivo neg_r.txt en un array “a” donde el índice es el número de línea NR (número de registros o líneas procesados hasta el momento).
#La segunda parte del comando: accede al elemento del array “a” que corresponde al número de registro actual “FNR” en urls_neg.txt, después imprime toda la línea actual seguida del contenido correspondiente a [FNR]
#Especificamos que vamos a devolver a tomar el archivo urls_neg.txt
#Guardamos nuestros resultados en neg_u_r.txt
awk 'NR==FNR{a[NR]=$0; next} {print $0, a[FNR]}' neg_r.txt ../urls_neg.txt > neg_u_r.txt
#Regresamos a la carpeta pos
cd ../pos 
#Primero sumamos el valor del segundo campo (‘$2’) para cada clave del primer campo (‘$1’) y esa suma se almacena en el array sum bajo la clave ‘$1’. Además, incrementamos un contador para cada clave del primer campo el cual llevara la cuenta del numero de veces que aparece cada clave.
#Después con un bucle vamos a recorrer cada clave que ha sido registrada en el array sum. Para cada clave va a calcular el promedio de los valores en sum.
#Se imprimirá la clave y su promedio.
#El resultado se va a guardar en pro_pos.txt.
awk '{sum[$1]+=$2; count[$1]++} END {for (i in sum) print i, sum[i]/count[i]}' pos_u_r.txt > pro_pos.txt
#Regresamos a la carpeta neg
cd ../neg
##Primero sumamos el valor del segundo campo (‘$2’) para cada clave del primer campo (‘$1’) y esa suma se almacena en el array sum bajo la clave ‘$1’. Además, incrementamos un contador para cada clave del primer campo el cual llevara la cuenta del numero de veces que aparece cada clave.
#Después con un bucle vamos a recorrer cada clave que ha sido registrada en el array sum. Para cada clave va a calcular el promedio de los valores en sum.
#Se imprimirá la clave y su promedio.
#El resultado se va a guardar en pro_neg.txt.
awk '{sum[$1]+=$2; count[$1]++} END {for (i in sum) print i, sum[i]/count[i]}' neg_u_r.txt > pro_neg.txt
#Regresamos a la carpeta pos
cd ../pos
#Leemos el archivo pro_pos.txt
#Vamos a ordenar las líneas basándonos en el segundo campo de cada línea. Especificamos que debe ordenarse numéricamente en orden descendente
#Imprimimos los primeros 10 elementos que están ordenanos,
#Guardamos los resultados en mejores10.txt
cat pro_pos.txt | sort -k2,2nr | head -n 10 > mejores10.txt
#Regresamos a la carpeta neg
cd ../neg
#Leemos el archivo pro_neg.txt
#Vamos a ordenar las líneas basándonos en el segundo campo de cada línea. Especificamos que debe ordenarse numéricamente en orden descendente
#Imprimimos los primeros 10 elementos que están ordenanos,
#Guardamos los resultados en peores10.txt
cat pro_neg.txt | sort -k2,2nr | head -n 10 > peores10.txt