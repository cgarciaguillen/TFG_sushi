# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:07:23 2020

@author: chach
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:34:39 2020

@author: chach
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#datos=pd.read_excel("Marzo_eur_usd_min.xlsx")
#datos=pd.read_excel("Enero-Abril_eur_usd_hora.xlsx")
#datos=pd.read_excel("Amazon_2019_dia.xlsx")
datos=pd.read_excel("2000-2020_eur_usd_semana.xlsx")

sns.lineplot(data=datos["Open"],label="Open")

rolls=10 
orden=20

#print(datos.head())



#print(min(datos.iloc[2,3],datos.iloc[3,3]))



## Crecimiento y decrecimiento
        
crece=[]
decrece=[]
igual=[]


for i in range (datos.shape[0]):
    if datos.iloc[i,1] > datos.iloc[i,4]:
        crece.append(i)
    
    elif datos.iloc[i,1] < datos.iloc[i,4]:
        decrece.append(i)
        
    else:
        igual.append(i)
        
maximo=[]
minimo=[]
nada=[]

for i in range (1, datos.shape[0]-1):
    if (i-1) in crece and (i+1) in decrece:
        maximo.append(i)
    elif (i-1) in decrece and (i+1) in crece:
        minimo.append(i)
    else:
        nada.append(i)
    
maximo_significativo=[]
minimo_significativo=[]   



##Crecimientos significativos




for i in range (orden , datos.shape[0]-orden):
    evaluacion_maximo=datos.iloc[i,2]
    no_max=False
    for j in range (-orden+1,orden):
        if datos.iloc[i+j,2] > evaluacion_maximo:
            no_max=True
        #if (datos.iloc[i+j,2] == evaluacion_maximo) and j==0:
         #   no_max=True
    if no_max == False:
        maximo_significativo.append(i)


for i in range (orden , datos.shape[0]-orden):
    evaluacion_minimo=datos.iloc[i,3]
    no_min=False
    for j in range (-orden+1,orden):
        if datos.iloc[i+j,3] < evaluacion_minimo:
            no_min=True
        #if (datos.iloc[i+j,3] == evaluacion_maximo) and j==0:
         #   no_max=True
    if no_min == False:
        minimo_significativo.append(i)


posible_bajista=[]
posible_alcista=[]

for i in range (datos.shape[0]-orden):
    maximo_previo=0
    minimo_previo=datos.iloc[i,3]
    for j in range (orden):
        maximo_previo=max(maximo_previo,datos.iloc[i+j,2])
        minimo_previo=min(minimo_previo,datos.iloc[i+j,3])
    if maximo_previo==datos.iloc[i+j,2]:
        posible_bajista.append(i+j)
    if minimo_previo==datos.iloc[i+j,3]:
        posible_alcista.append(i+j)




        
        
        
##Sushi roll
      
        
maximo1=0
maximo2=0

sushi=[]
sushi_filtrado=[]
repetidos=[]


for i in range (datos.shape[0]-2*rolls):
    maximo1=0
    minimo1=datos.iloc[i,3]
    maximo2=0
    minimo2=datos.iloc[i+3,3]

    for j in range (rolls):  #0,1,2,3,4
        maximo1=max(datos.iloc[i+j,2],maximo1)
        minimo1=min(datos.iloc[i+j,3],minimo1)
    for j in range (rolls,2*rolls): #5,6,7,8,9
        maximo2=max(datos.iloc[i+j,2],maximo2)
        minimo2=min(datos.iloc[i+j,3],minimo2)

    if maximo2>maximo1 and minimo2<minimo1:
        sushi.append(i)

    
for i in sushi:
    if (i-1) in sushi_filtrado:
        repetidos.append(i)
    elif (i-1) in repetidos:
        repetidos.append(i)
    else:
        sushi_filtrado.append(i) 
   


##Analizar sushi rolls
        
sushi_bajista=[]
#Pasa de Bullish a Bearish
#cumple siguientes condiciones:
#verde (cierra más alto que abre)
#Tiene tendencia alcista (máximo y mínimo mayores que el de hace 5)
#alcanza su máximo en los anteriores


for i in sushi:
    maximo3=0
    minimo3=datos.iloc[i,3]
    for j in range(rolls):
        maximo3=max(maximo3, datos.iloc[i+j,2])
    for j in range (2*rolls):
        minimo3=min(minimo3, datos.iloc[i+j,3])
           
        
    if ((datos.iloc[i+2*rolls-1,4] < datos.iloc[i+2*rolls-1,1]) and  (datos.iloc[i,3] < datos.iloc[i+rolls-1,3])
        and (datos.iloc[i,2] < datos.iloc [i+rolls-1,2])):
        sushi_bajista.append(i)
    
#for i in posicion:
    
    
    #if ((datos.iloc[i,4]) > datos.iloc[i,1])
        
    
sushi_alcista=[]
#Pasa de Bearish a Bullish
#cumple siguientes condiciones:
#rojo (abre más alto que cierra)
#Tiene tendencia bajista (máximo y mínimo menores que el de hace 5)
#alcanza su mínimo en los anteriores


for i in sushi:
    minimo4=datos.iloc[i,3]
    maximo4=0
    for j in range(rolls):
        minimo4=min(minimo4, datos.iloc[i+j,3])
    for j in range (2*rolls):
        maximo4=max(maximo4, datos.iloc[i+j,2])
        
        
    if ((datos.iloc[i+2*rolls-1,4] < datos.iloc[i+2*rolls-1,1]) and (datos.iloc[i,3] > datos.iloc[i+rolls-1,3])
        and (datos.iloc[i,2] > datos.iloc [i+rolls-1,2])):
        sushi_alcista.append(i)
    
#print ("sushi bajista =", sushi_bajista)
#print("maximo significativo =", maximo_significativo)

#print ("sushi alcista =", sushi_alcista)
#print("minimo significativo =", minimo_significativo)


podria_estar_bajista=[]
podria_noestar_bajista=[]

#for i in maximo_significativo:
for i in posible_bajista:
    if (i-rolls) in sushi_bajista or (i-rolls-1) in sushi_bajista or (i-rolls+1) in sushi_bajista:
        podria_estar_bajista.append(i)
    else:
        podria_noestar_bajista.append(i)
        
podria_estar_alcista=[]
podria_noestar_alcista=[]
#Comprobación
#for i in minimo_significativo:
for i in posible_alcista:
    if (i-rolls) in sushi_alcista or (i-rolls-1) in sushi_alcista or (i-rolls+1) in sushi_alcista:
        podria_estar_alcista.append(i)
    else:
        podria_noestar_alcista.append(i)
        

#Comprobación
esta_bajista=[]
noesta_bajista=[]

for i in maximo_significativo:
    if (i-rolls) in sushi_bajista or (i-rolls-1) in sushi_bajista or (i-rolls+1) in sushi_bajista:
        esta_bajista.append(i)
    else:
        noesta_bajista.append(i)
        
esta_alcista=[]
noesta_alcista=[]
#Comprobación
for i in minimo_significativo:
    if (i-rolls) in sushi_alcista or (i-rolls-1) in sushi_alcista or (i-rolls+1) in sushi_alcista:
        esta_alcista.append(i)
    else:
        noesta_alcista.append(i)



exito_alcista=[]
error_alcista=[]
exito_bajista=[]
error_bajista=[]

for i in podria_estar_alcista:
    if i in esta_alcista:
        exito_alcista.append(i)
    else:
        error_alcista.append(i)

for i in podria_estar_bajista:
    if i in esta_bajista:
        exito_bajista.append(i)
    else:
        error_bajista.append(i)


error_bajista_filtrado=[]
repetidos_bajista=[]
for i in error_bajista:
    if (i-1) in error_bajista_filtrado or (i-2) in error_bajista_filtrado:
        repetidos_bajista.append(i)
    elif (i-1) in repetidos_bajista or (i-2) in repetidos_bajista:
        repetidos_bajista.append(i)
    else:
        error_bajista_filtrado.append(i) 

error_alcista_filtrado=[]
repetidos_alcista=[]
for i in error_alcista:
    if (i-1) in error_alcista_filtrado or (i-2) in error_alcista_filtrado:
        repetidos_alcista.append(i)
    elif (i-1) in repetidos_alcista or (i-2) in repetidos_alcista:
        repetidos_alcista.append(i)
    else:
        error_alcista_filtrado.append(i)    


        

#print("Sushi bajista correctamente identificado en: ",exito_bajista)
#print("Sushi alcista correctamente identificado en: ",exito_alcista)

print("Ratio exito/fracaso en bajista=", len(exito_bajista), "/", len(error_bajista_filtrado))
print("Ratio exito/fracaso en alcista=", len(exito_alcista), "/", len(error_alcista_filtrado))

#Cambios en tendencia general

#derece_general=[]
#crece_general=[]


#Primero vamos a ver las tendencias sabiendo los picos, y luego intentar programar 
#esas tendencias sin saber el futuro.


    
    


#for i in posicion_filtrada:
            
        
        
        
        
        