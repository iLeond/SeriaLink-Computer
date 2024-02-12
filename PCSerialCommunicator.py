import serial
import time
import threading

class PCSerialCommunicator:
    def __init__(self, port='COM3', baudrate=115200):
        self.ser = serial.Serial(port, baudrate)
        self.running = True

    def send_data(self, data):
        complete_message = f"{data}\n"
        print(f"Enviando: {complete_message.strip()}")  # Para depuración
        self.ser.write(complete_message.encode('utf-8'))

    def listen_for_responses(self):
        print("Comenzando a escuchar respuestas...")
        while self.running:
            if self.ser.in_waiting:
                received_data = self.ser.readline().decode().strip()
                print("Respuesta de la Pico:", received_data)

    def run(self):
        listen_thread = threading.Thread(target=self.listen_for_responses)
        listen_thread.start()

        try:
            while self.running:
                self.send_data("Mensaje desde la computadora")
                time.sleep(10)
        except KeyboardInterrupt:
            print("Deteniendo comunicación...")
            self.running = False
            listen_thread.join()

if __name__ == "__main__":
    communicator = PCSerialCommunicator()
    communicator.run()
