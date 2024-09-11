import tkinter as tk
import socket
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
BUFFER_SIZE = 4096

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# Client handling thread
def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break

            # Handle client commands
            if data.startswith('MSG:'):
                message = data[4:].strip()
                print(f"[*] Received message from {client_address[0]}: {message}")
                # Broadcast the message to all connected clients
                for client in clients:
                    if client != client_socket:
                        client.send(f"MSG:{message}".encode())
                        # Display the message in the UI
                        display_message(f"{client_address[0]}: {message}")

            # ... (other client commands handling)

        except ConnectionResetError:
            break

    print(f"[*] {client_address[0]} disconnected")
    clients.remove(client_socket)
    client_socket.close()

# Main server loop
clients = []
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

# Create the user interface
root = tk.Tk()
root.title("Blackman Chat App")

# Create a label for the chat messages
chat_label = tk.Label(root, text="Chat Messages:")
chat_label.pack()

# Create a text widget to display the chat messages
chat_text = tk.Text(root, height=20, width=50)
chat_text.pack()

# Create an input field for sending messages
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# Function to handle sending messages
def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    # Send the message to the server
    for client in clients:
        client.send(f"MSG:{message}".encode())

# Function to display received messages
def display_message(message):
    chat_text.insert(tk.END, f"{message}\n")

# Create a button to send messages
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Start the user interface main loop
root.mainloop()
