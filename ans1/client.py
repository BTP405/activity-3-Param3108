# Importing necessary libraries
import socket
import pickle
import os

# Function to load the content of a file and return its binary data
def load_file(filepath):
    """
    Load the content of a file and return its binary data.

    Args:
        filepath (str): The path of the file to be loaded.

    Returns:
        bytes: The binary data representing the content of the file.
    """
    with open(filepath, 'rb') as file:
        return file.read()

# Main function to connect to the server and send a file
def main():
    """
    Main function to connect to the server and send a file.

    Args:
        None

    Returns:
        None
    """
    # Server configuration
    server_host = '127.0.0.1'  # Server IP address
    server_port = 12345         # Server port number
    buffer_size = 4096          # Buffer size for data transmission

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))
    except Exception as e:
        print("Error connecting to the server:", e)
        return

    try:
        # Prompt the user to enter the path of the file to send
        file_path = input("Enter the path of the file to send: ")
        if not os.path.exists(file_path):
            print("File not found.")
            return
        
        # Load the file data
        file_data = load_file(file_path)
        # Serialize the file data using pickle
        serialized_data = pickle.dumps(file_data)

        # Send the serialized data to the server
        client_socket.sendall(serialized_data)
        print("File sent successfully")
    except Exception as e:
        print("Error:", e)
    finally:
        # Close the client socket
        client_socket.close()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
