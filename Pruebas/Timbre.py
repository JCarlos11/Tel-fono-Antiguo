#Librerias
import RPi.GPIO as GPIO
import time

"""
El presente código se utiliza para hacer sonar el timbre de un teléfono antiguo de forma indefinida 
"""

#Pines
PinIN1 = 11 #Pin para puente H 
PinIN2 = 13 #Pin para puente H

#Variables
periodo = 0.1 #Periodo de la onda sinusoidal simulada [s]
tiempoParada = 1.5 #Tiempo de silencio entre sonidos del timbre [s]
ciclos = 20 #Modifica la duracion del sonido del timbre ---> Duracion[s]=periodo*ciclos (0.1*20 = 2s)

#Configuracion de pines GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PinIN1, GPIO.OUT)
GPIO.setup(PinIN2, GPIO.OUT)

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

#Codigo principal
if __name__ == '__main__':
    try:
        while True:
            for i in range(ciclos):
                sentidoHorario()
                time.sleep(periodo/2)

                sentidoAntiHorario()
                time.sleep(periodo/2)
                    
            detener()
            time.sleep(tiempoParada)
            print("Sonando")

    except Exception as e:
        print(f"Ocurrió una excepción: {e}")

    finally:
        # Limpieza de recursos
        GPIO.cleanup()       # Limpia los pines GPIO
        print("Recursos limpiados. Programa finalizado.")


