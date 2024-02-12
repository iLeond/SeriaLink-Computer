import serial
import time
import threading

class PCSerialCommunicator:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.ser = serial.Serial(port, baudrate)
        self.running = True

    def send_data(self, data):
        complete_message = f"{data}\n"
        print(f"Enviando a {self.port}: {complete_message.strip()}")
        self.ser.write(complete_message.encode('utf-8'))

    def listen_for_responses(self):
        print(f"Escuchando respuestas en {self.port}...")
        while self.running:
            if self.ser.in_waiting:
                received_data = self.ser.readline().decode().strip()
                print(f"Respuesta de {self.port}: {received_data}")

    def run(self):
        listen_thread = threading.Thread(target=self.listen_for_responses)
        listen_thread.start()

        # Ejemplo de cómo enviar datos. Puedes adaptar esto según necesites.
        try:
            while True:
                self.send_data("Mensaje desde la computadora")
                time.sleep(10)
        except KeyboardInterrupt:
            self.running = False
            listen_thread.join()

def main():
    communicator_com3 = PCSerialCommunicator('COM3')
    communicator_com4 = PCSerialCommunicator('COM4')

    # Iniciar ambos comunicadores en sus propios hilos para permitirles operar simultáneamente
    thread_com3 = threading.Thread(target=communicator_com3.run)
    thread_com4 = threading.Thread(target=communicator_com4.run)

    thread_com3.start()
    thread_com4.start()

    try:
        while True:
            time.sleep(1)  # Mantén el programa principal ejecutándose
    except KeyboardInterrupt:
        communicator_com3.running = False
        communicator_com4.running = False
        thread_com3.join()
        thread_com4.join()
        print("Programa terminado.")

if __name__ == "__main__":
    main()
