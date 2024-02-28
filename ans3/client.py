import socket
import threading
import pickle

# Function to receive messages from the server
def receive_messages(client_socket):
    """
    Receives messages from the server.

    Args:
        client_socket (socket.socket): The client's socket connected to the server.

    Returns:
        None
    """
    try:
        while True:
            pickled_data = client_socket.recv(4096)
            message = pickle.loads(pickled_data)
            print(message)

    except ConnectionAbortedError:
        pass
    except Exception as e:
        print("Error receiving messages:", e)
    finally:
        client_socket.close()

# Function to send messages to the server
def send_message(client_socket):
    """
    Sends messages to the server.

    Args:
        client_socket (socket.socket): The client's socket connected to the server.

    Returns:
        None
    """
    print("To leave the chat room type: q")
    try:
        while True:
            message = input()
            if message == "q":
                break
            pickled_message = pickle.dumps(message)
            client_socket.sendall(pickled_message)

    except Exception as e:
        print("Error sending message:", e)
    finally:
        client_socket.close()

# Function to run the client
def run_client():
    """
    Establishes connection with the server and starts threads for sending and receiving messages.

    Args:
        None

    Returns:
        None
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_message, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except pickle.PickleError as pe:
        print("Error occurred while pickling:", pe)
    except socket.error as se:
        print("Socket error: ", se)
    except Exception as e:
        print("Error occurred:", e)
    finally:
        print("Connection closed")

if __name__ == "__main__":
    run_client()

