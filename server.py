import socket
import threading

def header():
    print("[*]COMMANDS[*]")
    print("[*]open (link)[*]")
    print("[*]del (file path)[*]")


class SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_socket(self):
        self.server.bind((self.host, self.port))
        self.server.listen(4)
        print("Server is listening to port...")

        while True:
            client_socket, client_address = self.server.accept()
            print("Connection from", client_address)

            # Handle each client in a separate thread
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            self.send_msg(client_socket)
            self.recv_msg(client_socket)
        except (ConnectionResetError, BrokenPipeError):
            print("Client disconnected.")

    def send_msg(self, client_socket):
        while True:
            message = input("command:")

            if message == "":
                break
            else:
                client_socket.send(message.encode())

    def recv_msg(self, client_socket):
        while True:
            client_status = client_socket.recv(1024)
            if not client_status:
                break
            print(client_status.decode())


if __name__ == "__main__":
    header()
    server = SERVER('127.0.0.1', 9999)

    # Start the server_socket method in a separate thread
    server_thread = threading.Thread(target=server.server_socket)
    server_thread.start()

    # Allow the main thread to wait for the server_thread to finish (press Ctrl+C to stop)
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("Server stopped.")
