# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:07:23 2020

@author: chach
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:34:39 2020

@author: Carlos García Guillén
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

datos=pd.read_excel("Marzo_eur_usd_min.xlsx")
#datos=pd.read_excel("Enero-Abril_eur_usd_hora.xlsx")
#datos=pd.read_excel("Amazon_2019_dia.xlsx")
#datos=pd.read_excel("2000-2020_eur_usd_semana.xlsx")

#sns.lineplot(data=datos["Open"],label="Open")

rolls=10 
orden=50
rango=2
comision_trader=0.36/10000
spread=0





      
        
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
   


sushi_bajista=[]


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
    

sushi_alcista=[]


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
    


"""
Empezamos a ver si es viable economicamente

"""



exito_bajista=0
fracaso_bajista=0
dinero_perdido_bajista=0
dinero_ganado_bajista=0
ganancias=[]
perdidas=[]

            
for i in sushi_bajista:   #Máximo y para abajo
    contador=0
    pico=0
    stop_loss=False
    take_profit=False
    for j in range (2*rolls):
        pico=max(pico,datos.iloc[i+j,2])
    entrada=datos.iloc[i+j,4]        #entramos en el cierre
    ancho=rango*(pico-entrada)
    
    if ancho > (comision_trader+spread):
        while stop_loss==False and take_profit==False and (i+j+contador+1) < datos.shape[0]:
            contador=contador+1
            if datos.iloc [i+j+contador,4] >= (entrada+ancho) or datos.iloc[i+j+contador,2] >= (entrada+ancho):
                stop_loss=True
            elif datos.iloc [i+j+contador,4] <= (entrada-ancho) or datos.iloc[i+j+contador,3] <= (entrada-ancho):
                take_profit=True
                
        if stop_loss==True:
            fracaso_bajista=fracaso_bajista+1
            dinero_perdido_bajista=dinero_perdido_bajista+ancho+comision_trader+spread
            perdidas.append((ancho+comision_trader+spread)*10000)
            
        
        elif take_profit==True:
            exito_bajista=exito_bajista+1
            dinero_ganado_bajista=dinero_ganado_bajista+ancho-comision_trader-spread
            ganancias.append((ancho-comision_trader-spread)*10000)
    



exito_alcista=0
fracaso_alcista=0
dinero_perdido_alcista=0
dinero_ganado_alcista=0

            
for i in sushi_alcista:   #Mínimo y para arriba
    contador=0
    valle=datos.iloc[i,3]
    stop_loss=False
    take_profit=False
    for j in range (2*rolls):
        valle=min(valle,datos.iloc[i+j,3])
    entrada=datos.iloc[i+j,4]        #entramos en el cierre
    ancho=rango*(entrada-valle)    
    
    if ancho > comision_trader:
        while stop_loss==False and take_profit==False and (i+j+contador+1) < datos.shape[0]:
            contador=contador+1
            if datos.iloc [i+j+contador,4] <= (entrada-ancho) or datos.iloc[i+j+contador, 3] <= (entrada-ancho):
                stop_loss=True
            elif datos.iloc [i+j+contador,4] >= (entrada+ancho) or datos.iloc[i+j+contador,2] >= (entrada+ancho):
                take_profit=True
                
        if stop_loss==True:
            fracaso_alcista=fracaso_alcista+1
            dinero_perdido_alcista=dinero_perdido_alcista+ancho+comision_trader
            perdidas.append((ancho+comision_trader)*10000)
        
        elif take_profit==True:
            exito_alcista=exito_alcista+1
            dinero_ganado_alcista=dinero_ganado_alcista+ancho-comision_trader
            ganancias.append((ancho-comision_trader)*10000)
        


exitos_totales=exito_alcista+exito_bajista
fracasos_totales=fracaso_alcista+fracaso_bajista
operaciones_efectuadas=exitos_totales+fracasos_totales
ratio_porcentual=100*exitos_totales/operaciones_efectuadas
diferencia=exitos_totales-fracasos_totales
dinero_ganado=dinero_ganado_alcista+dinero_ganado_bajista
dinero_perdido=dinero_perdido_bajista+dinero_perdido_alcista
renta_total=dinero_ganado-dinero_perdido
print("El porcentaje de aciertos es del ", ratio_porcentual, " por ciento")
print("He ganado",  dinero_ganado*10000," pips en ", exitos_totales, "veces")
print("He perdido", dinero_perdido*10000," pips en ", fracasos_totales, "veces")
print("El balance total ha sido de", (dinero_ganado-dinero_perdido)*10000,"pips")
