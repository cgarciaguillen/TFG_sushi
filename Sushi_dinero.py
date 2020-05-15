# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:09:29 2020

@author: Carlos García Guillén
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numba import njit
from time import time




datos_df=pd.read_excel("Marzo_eur_usd_min.xlsx")
#datos_df=pd.read_excel("Enero-Abril_eur_usd_hora.xlsx")
#datos_df=pd.read_excel("Amazon_2019_dia.xlsx")
#datos_df=pd.read_excel("2000-2020_eur_usd_semana.xlsx")
datos=np.zeros((datos_df.shape[0],4))

for i in range (datos.shape[0]):
    for j in range (4):
        datos[i][j]=datos_df.iloc[i,j+1]
        
   
        
#sns.lineplot(data=datos_df["Open"],label="Open")


#roll = (20,30,40,50,100,200)
salida_emergencia = 10
#roll=(5,6,7,8,9,10,20) 
#rangos = (0.5,1,1.5,2,2.5,3,5)
#roll=np.array([5,6,7,8,9,10,20])
roll = np.array ([20,30,40,50,100,200])
rangos = np.array([0.5,1,1.5,2,2.5,3,5])
comision_trader = 0.36/10000


pips = True
representar = True






@njit
def Primer_intento(datos,roll,salida_emergencia,rangos,comision_trader,pips):
    data_final=np.zeros( ( len(roll), len(rangos) ) )
    data_acierto=np.zeros( (len(roll), len(rangos) ) )


    posicion_x=-1
    
    
    for rolls in roll:
        
            
        posicion_x += 1
        
        posicion_y = -1
        
        for rango in rangos:
            
                        
            posicion_y += 1
          
            
            maximo1=0
            maximo2=0
            exito_bajista=0
            fracaso_bajista=0
            dinero_perdido_bajista=0
            dinero_ganado_bajista=0  
            exito_alcista=0
            fracaso_alcista=0
            dinero_perdido_alcista=0
            dinero_ganado_alcista=0
    
            
            
            for i in range (len(datos)-2*rolls):
                maximo1=0
                minimo1=datos[i,2]
                maximo2=0
                minimo2=datos[i+3,2]
            
                for j in range (rolls):  #0,1,2,3,4
                    maximo1=max(datos[i+j,1],maximo1)
                    minimo1=min(datos[i+j,2],minimo1)
                for j in range (rolls,2*rolls): #5,6,7,8,9
                    maximo2=max(datos[i+j,1],maximo2)
                    minimo2=min(datos[i+j,2],minimo2)
            
                if maximo2>maximo1 and minimo2<minimo1:
    
    
                    maximo3=0
                    minimo3=datos[i,2]
                    minimo4=datos[i,2]
                    maximo4=0
                    
                    for j in range(rolls):
                        maximo3=max(maximo3, datos[i+j,1])
                        minimo4=min(minimo4, datos[i+j,2])
                    for j in range (2*rolls):
                        minimo3=min(minimo3, datos[i+j,1])
                        maximo4=max(maximo4, datos[i+j,2])
                        
                        
                           
                    #Sushi Bajista    
                    if ((datos[i+2*rolls-1,3] < datos[i+2*rolls-1,0]) and  (datos[i,2] < datos[i+rolls-1,2])
                        and (datos[i,1] < datos[i+rolls-1,1])):
                        
                        contador=0
                        pico=0
                        stop_loss=False
                        take_profit=False
    
                        for j in range (2*rolls):
                            pico=max(pico,datos[i+j,1])
                        entrada=datos[i+j,3]        #entramos en el cierre
                        ancho=rango*(pico-entrada)
                        
                        if ancho > comision_trader:
                            while stop_loss==False and take_profit==False and (i+j+contador+1) < len(datos) and contador < salida_emergencia*rolls:
                                contador=contador+1
                                
                                if contador >= salida_emergencia*rolls:
    
                                    salida_emerg=datos[i+j+contador,3]
                                    resultado_emergencia=-salida_emerg+entrada-comision_trader
                                    
                                    if resultado_emergencia > 0 :
                                        exito_bajista += 1
                                        dinero_ganado_bajista += resultado_emergencia                               
                                        
                                    
                                    elif resultado_emergencia < 0 :
                                        fracaso_bajista += 1
                                        dinero_perdido_bajista += abs(resultado_emergencia)
                                    
                                    
                                elif datos[i+j+contador,3] >= (entrada+ancho) or datos[i+j+contador,1] >= (entrada+ancho):
                                    stop_loss=True
                                    fracaso_bajista += 1
                                    dinero_perdido_bajista += (ancho+comision_trader)
                                
                                                           
                                elif datos[i+j+contador,3] <= (entrada-ancho) or datos[i+j+contador,2] <= (entrada-ancho):
                                    take_profit=True
                                    exito_bajista += 1
                                    dinero_ganado_bajista += (ancho-comision_trader)
                                                         
                                                 
                            
                            
                    #Sushi Alcista
                    elif ((datos[i+2*rolls-1,3] < datos[i+2*rolls-1,0]) and (datos[i,2] > datos[i+rolls-1,2])
                    and (datos[i,1] > datos [i+rolls-1,1])):
                        contador=0
                        valle=datos[i,2]
    
                        for j in range (2*rolls):
                            valle=min(valle,datos[i+j,2])
                        entrada=datos[i+j,3]        #entramos en el cierre
                        ancho=rango*(entrada-valle) 
                        stop_loss=False
                        take_profit=False
                        
                        if ancho > comision_trader:
                            while stop_loss==False and take_profit==False and (i+j+contador+1) < len(datos) and contador < salida_emergencia*rolls:
                                contador=contador+1
                                
                                if contador >= salida_emergencia*rolls:
    
                                    salida_emerg=datos[i+j+contador,3]
                                    resultado_emergencia=salida_emerg-entrada-comision_trader  
                                    
                                    if resultado_emergencia > 0 :
                                        exito_alcista += 1
                                        dinero_ganado_alcista += resultado_emergencia
                                        
                                                                          
                                    if resultado_emergencia < 0 :
                                        fracaso_alcista += 1
                                        dinero_perdido_alcista += abs(resultado_emergencia)
                                    
                                    
                                  
                                    
                                elif datos[i+j+contador,3] <= (entrada-ancho) or datos[i+j+contador, 2] <= (entrada-ancho):
                                    stop_loss=True
                                    fracaso_alcista=fracaso_alcista+1
                                    dinero_perdido_alcista += (ancho+comision_trader)
                                    
                                    
                                    
                                elif datos[i+j+contador,3] >= (entrada+ancho) or datos[i+j+contador,1] >= (entrada+ancho):
                                    take_profit=True
                                    exito_alcista=exito_alcista+1
                                    dinero_ganado_alcista += (ancho-comision_trader)
                                    
           
                                   
    
                    
            dinero_ganado=dinero_ganado_alcista+dinero_ganado_bajista
            dinero_perdido=dinero_perdido_bajista+dinero_perdido_alcista
            
            resultado=dinero_ganado-dinero_perdido
     
            pips_totales=(resultado)*10000
            
            if pips == True:
                data_final[posicion_x][posicion_y]=pips_totales
            else:
                data_final[posicion_x][posicion_y]=resultado
                
            exitos_totales=exito_alcista+exito_bajista
            fracasos_totales=fracaso_alcista+fracaso_bajista
            operaciones_efectuadas=exitos_totales+fracasos_totales
            ratio_porcentual=100*exitos_totales/operaciones_efectuadas
            
            data_acierto[posicion_x][posicion_y]=ratio_porcentual

    
    return (data_acierto, data_final)


tic=time()
data_acierto, data_final = Primer_intento(datos,roll,salida_emergencia,rangos,comision_trader,pips)
tac=time()

tiempo=tac-tic

 
 
if representar == True:
    plt.figure(figsize=(len(roll),len(rangos)))      
    sns.heatmap(data=data_final, annot=True, center=0, cmap="afmhot")
    plt.xlabel("Rango")
    plt.ylabel("Rolls")
    
    plt.figure(figsize=(len(roll),len(rangos)))      
    sns.heatmap(data=data_acierto, annot=True, center=50, cmap="afmhot")
    plt.xlabel("Rango")
    plt.ylabel("Rolls")


print("El tiempo ha sido",tiempo)    

