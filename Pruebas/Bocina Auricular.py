#Librerias
import pygame
from pygame import mixer 
#Documentacion pygame : 
#https://www.pygame.org/docs/ref/music.html

"""
El presente código se utiliza para reproducir un audio por medio de la salida 3.5mm de audio de una computadora Raspberry Pi. 

"""

pygame.init() # Inicializa pygame mixer
mixer.music.load('/home/telefono01/Adios chimuelo.mp3') # Carga el archivo de audio
pygame.mixer.music.set_volume(1) ## Establecer volumen / Parámetro va de 0 a 1

pygame.mixer.music.play(-1) #El -1 indica que se reproducirá en bucle el audio hasta que se cuelgue el auricular
print("SONANDO AUDIO")
            

    