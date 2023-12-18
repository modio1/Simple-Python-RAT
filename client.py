import socket
import threading
import os
class CLIENT:
    def __init__(self,host,port):
        self.host = host
        self.port = port


    def client_socket(self):
        # Connects to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            self.client.connect((self.host,self.port))
            print("Connected to  server.")

        except:
            print("Unable to connect. Server is down.")

    def recv_msg(self):
        while True:
            try:
                message = self.client.recv(1024)
                if message:
                    print("Command:",message.decode())
                    x = message.decode()
                    print(x[:3])
                    if x[:4] == 'open':
                        print(x[:4])
                        print(x[4:])
                        self.command_chk(x[:4],x[5::])
                    elif x[:3] == "del":
                        self.command_chk(x[:3],x[3::])
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    def send_msg(self):
        try:

            self.client.send("Recieved...".encode())
        except Exception as e:
            print(e)

    def command_chk(self,command,link):
        if command == "open":
            import webbrowser
            webbrowser.open_new(link)
        elif command == "del":
            os.remove(link)

if __name__ == "__main__":
    client = CLIENT('127.0.0.1', 9999)
    client.client_socket()
    send_thread = threading.Thread(target=client.send_msg)
    send_thread.start()
    recv_thread = threading.Thread(target=client.recv_msg)
    recv_thread.start()

    try:
        recv_thread.join()
        send_thread.join()
    except Exception as e:
        print(e)

