import socket
import threading
import pickle

class ChatServer:
    """
    Simple chat server implementation.
    """

    def __init__(self):
        """
        Initialize the ChatServer class.
        """
        self.clients = []  # List to store client sockets
        self.lock = threading.Lock()  # Lock for thread safety
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create server socket
        self.server_socket.bind(('localhost', 12345))  # Bind server socket

    def start(self):
        """
        Start the server to listen for client connections.
        """
        self.server_socket.listen(5)
        print("Server is listening")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Connected to", client_address)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        """
        Handle individual client connections.

        Args:
            client_socket (socket.socket): Socket object representing the client.
        """
        with self.lock:
            self.clients.append(client_socket)

        try:
            while True:
                pickled_data = client_socket.recv(4096)
                if not pickled_data:
                    break
                message = pickle.loads(pickled_data)
                if message != "q":
                    print("Received message:", message)
                    broadcast_thread = threading.Thread(target=self.broadcast_message,
                                                         args=(message, client_socket,))
                    broadcast_thread.start()
                else:
                    break

        except ConnectionResetError:
            print("Client disconnected")
        except pickle.PickleError as pe:
            print("Error occurred while pickling:", pe)
        except socket.error as se:
            print("Socket error: ", se)
        except Exception as e:
            print("Error occurred:", e)
        finally:
            client_socket.close()
            with self.lock:
                self.clients.remove(client_socket)

    def broadcast_message(self, message, sender_socket):
        """
        Broadcast a message to all clients except the sender.

        Args:
            message (str): The message to be broadcast.
            sender_socket (socket.socket): The socket object representing the sender.
        """
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_socket:
                    pickled_message = pickle.dumps(message)
                    client_socket.sendall(pickled_message)

if __name__ == "__main__":
    server = ChatServer()
    server.start()

