#Librerias
import RPi.GPIO as GPIO
import time
import threading
import random
import pygame
from pygame import mixer 
#Documentacion pygame : 
#https://www.pygame.org/docs/ref/music.html

"""
El presente código se utiliza para hacer sonar un timbre de teléfono antiguo 
y reproducción de un audio precargado por la bocina del mismo teléfono. 
Realizando lo siguiente:

1.El audio sonará siempre que se levante el auricular y comenzará de cero cada vez. 
Entonces siempre que se cuelgue el auricular se detendrá el audio por completo

2.El audio se repetirá en bucle siempre que esté descolgado el auricular.

3.El timbre sonará solo si esta colgado el auricular y sonara en periodos de entre 10 a 30 minutos dado un numero aleatorio 
(este rango se puede configurar con las variables "tiempoInferior" y "tiempoSuperior").

4. El timbre sonará máximo 20 segundos (se puede configurar con la variable "tiempoEncendidoTimbre") . 
Sino se levanta el auricular en dicho periodo el timbre se apaga 
y se genera un nuevo numero aleatorio para el periodo de espera entre sonidos del timbre.
"""

print("Programa iniciado")

#Pines
PinIN1 = 11 #Pin para puente H 
PinIN2 = 13 #Pin para puente H
PinAur = 10 #Pin interruptor de timbre 

#Variables
periodo = 0.1 #Periodo de la onda sinusoidal simulada [s]
tiempoParada = 1.5 #Tiempo de silencio entre sonidos del timbre [s]
ciclos = 20 #Modifica la duracion del sonido del timbre ---> Duracion[s]=periodo*ciclos (0.1*20 = 2s)

tiempoEncendidoTimbre = 20 #segundos / Tiempo maximo de duración del sonido del timbre

#Tiempo aleatorio comprendido en un rango que transcurre entre colgar el telefono y sonar el timbre de nuevo
tiempoInferior= 600 #10 minutos
tiempoSuperior= 1800 #30 minutos
tiempoAleatorio = random.randint(tiempoInferior, tiempoSuperior) #segundos 
tiempoEntreEvento = tiempoAleatorio # segundos 

prev_s = time.time() # Inicializa la variable con el tiempo actual en milisegundos 
detener_hilo = True # Bandera para detener el hilo del timbre
reproduciendo = False #Variable auxiliar en reproducción del audio

#Configuracion de pines GPIO
GPIO.setmode(GPIO.BOARD) #Numeración física de los pines
GPIO.setup(PinIN1, GPIO.OUT)
GPIO.setup(PinIN2, GPIO.OUT)
GPIO.setup(PinAur, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Configuración pygame

pygame.init() # Inicializa pygame mixer

mixer.music.load('/home/telefono01/Adios chimuelo.mp3') # Carga el archivo de audio

pygame.mixer.music.set_volume(1) ## Establecer volumen / Parámetro va de 0 a 1

#FUNCIONES PARA EL PUENTE H
#auxiliares para simular sonido de llamada 
#con una entrada de corriente continua
def sentidoHorario():
    GPIO.output(PinIN1, GPIO.HIGH)
    GPIO.output(PinIN2, GPIO.LOW)

def sentidoAntiHorario():
    GPIO.output(PinIN1, GPIO.LOW)
    GPIO.output(PinIN2, GPIO.HIGH)

def detener():
    GPIO.output(PinIN1, GPIO.LOW)
    GPIO.output(PinIN2, GPIO.LOW)

#FUNCIÓN RING TELEFONO (HILO)
def ringTelefono():
    global detener_hilo
    while(True):
        while not detener_hilo:
            for i in range(ciclos):
                if detener_hilo == True:
                    break
                sentidoHorario()
                time.sleep(periodo/2)

                sentidoAntiHorario()
                time.sleep(periodo/2)   
            detener()
            time.sleep(tiempoParada)
            print("HILO RING ACTIVADO")

#Creacion del hilo
hiloRing = threading.Thread(target=ringTelefono)

#Comienzo del hilo
hiloRing.start()

#Codigo principal
if __name__ == '__main__':
    try:
        while True:

            current_s = time.time()

            #Si está colocado el auricular y transcurre el tiempo (tiempoEntreEvento) comienza a sonar el timbre   
            if current_s > prev_s + tiempoEntreEvento and GPIO.input(PinAur) == GPIO.HIGH:  
                detener_hilo = False #Comienza a sonar el timbre
                prev_s = current_s  # Actualiza prev_s
                tiempoAleatorio = random.randint(tiempoInferior, tiempoSuperior) #segundos  
                tiempoEntreEvento = tiempoAleatorio #Actualización del tiempo aleatorio del timbre dentro del rango establecido
                print("1.TIMBRE SONANDO")
            
            #Si tras sonar el timbre no es levantado el auricular durante tantos segundos (tiempoEncendidoTimbre) se apaga el timbre
            if current_s > prev_s + tiempoEncendidoTimbre and GPIO.input(PinAur) == GPIO.HIGH and detener_hilo == False: 
                 detener_hilo = True #Detenemos el sonido del timbre
                 prev_s = current_s # Actualiza prev_s
                 print("2.APAGANDO TIMBRE POR NO CONTESTAR")
            
            #Si se levanta el auricular y el timbre estaba sonando, deja de sonar y comienza con el audio
            if GPIO.input(PinAur) == GPIO.LOW and not reproduciendo: 
                detener_hilo = True  #Detenemos el sonido del timbre
                reproduciendo = True #Nos auxilia para que no se ejecute de forma indefinida este condicional una vez levantado el auricular
                pygame.mixer.music.play(-1) #El -1 indica que se reproducirá en bucle el audio hasta que se cuelgue el auricular
                print("3.SONAR AUDIO")
            
            #Si se "cuelga" el telefono y estaba sonando el audio, se detiene y actualiza tiempo
            if GPIO.input(PinAur) == GPIO.HIGH and pygame.mixer.music.get_busy(): 
                reproduciendo = False #Indicamos que se puede ejecutar de nueva cuenta el condicional de reproducción del audio al
                pygame.mixer.music.stop() #Se detiene el audio
                prev_s = current_s # Actualiza prev_s 
                print("4.DETENER AUDIO")
            
            time.sleep(0.1)

    except Exception as e:
        print(f"Ocurrió una excepción: {e}")

    finally:
        # Limpieza de recursos
        detener_hilo = True  # Detiene el hilo si está en ejecución
        hiloRing.join()      # Espera que el hilo termine
        GPIO.cleanup()       # Limpia los pines GPIO
        pygame.mixer.music.stop()  # Detiene cualquier audio en reproducción
        print("Recursos limpiados.")


