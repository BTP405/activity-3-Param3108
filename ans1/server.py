# Importing necessary libraries
import os
import socket

# Function to save received file data to a specified directory with a given filename
def save_file(data, directory, filename):
    """
    Save the received file data to a specified directory with the given filename.

    Args:
        data (bytes): The binary data representing the file.
        directory (str): The directory path where the file will be saved.
        filename (str): The name of the file to be saved.

    Returns:
        None
    """
    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)
    # Construct the file path
    filepath = os.path.join(directory, filename)
    # Write the file data to the specified file path
    with open(filepath, 'wb') as f:
        f.write(data)

# Main function to start the server and handle incoming connections
def main():
    """
    Main function to start the server and handle incoming connections.

    Args:
        None

    Returns:
        None
    """
    # Server configuration
    host = '127.0.0.1'     # localhost
    port = 12345            # port number
    buffer_size = 4096      # buffer size for receiving data
    directory = "received_files"  # directory to save received files

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening at", (host, port))

    # Accept incoming connections and handle them
    while True:
        # Accept connection request from client
        client_socket, client_address = server_socket.accept()
        print("Connected to", client_address)

        try:
            # Receive data from client
            data = client_socket.recv(buffer_size)
            if not data:
                print("No data received.")
                continue

            # Prompt user to enter filename to save the received file
            filename = input("Enter the filename to save the received file: ")
            # Save the received file data
            save_file(data, directory, filename)
            print("File saved successfully as", filename)
        except Exception as e:
            print("Error:", e)
        finally:
            # Close client socket
            client_socket.close()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
