import socket
import threading

class TCPClient:
    def __init__(self, host='127.0.0.1', port=3001):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Hilo para recibir mensajes
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, msg):
        try:
            self.sock.sendall(msg.encode())
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(f"📥 Mensaje recibido: {data.decode()}")
                else:
                    break
            except:
                break
