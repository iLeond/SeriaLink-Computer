import serial
import time

# Configura el puerto serial. Cambia 'COM3' por tu puerto correcto.
ser = serial.Serial('COM3', 9600)

print("Escuchando mensajes de la Pico...")

while True:
    if ser.in_waiting:
        # Lee los datos disponibles en el buffer y los decodifica
        received_data = ser.readline().decode().strip()
        print("Datos recibidos de la Pico:", received_data)
