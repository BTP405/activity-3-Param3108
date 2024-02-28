import socket
import pickle
from task_functions import task_multiply

# Define task execution function
def execute_task(task_data):
    """
    Execute the task received from the client.

    Args:
        task_data (bytes): Serialized task data containing the task function and arguments.

    Returns:
        Any: Result of executing the task.
    """
    try:
        # Unpickle the task data
        task, args = pickle.loads(task_data)
        # Execute the task with provided arguments
        result = task(*args)
        return result
    except Exception as e:
        print("Error executing task:", e)
        return None

def main():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12346  # Change this port number for each worker node

    # Create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind socket to address
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()
        print("Worker node is listening for incoming connections...")

        while True:
            # Accept connection
            conn, addr = server_socket.accept()
            print(f"Connection established from {addr}")

            with conn:
                # Receive task data
                task_data = conn.recv(4096)
                if not task_data:
                    print("No task data received")
                    continue

                # Execute task
                result = execute_task(task_data)

                # Send result back to client
                if result is not None:
                    result_data = pickle.dumps(result)
                    conn.sendall(result_data)

if __name__ == "__main__":
    main()
