# Blackman

Blackman is a Python-based chat application that allows users to communicate with each other via messages, calls, and video calls. It is designed to be untraceable and unhackable, with the exception of the host (admin) who can access full control.

## Features

- Messaging: Users can send and receive text messages.
- Calls: Users can initiate calls with other users.
- Video Calls: Users can initiate video calls with other users.
- Location Retrieval: Users can retrieve their location.
- Audio Recording: Users can record audio and send it to other users.
- Camera Capture: Users can capture images from their camera and send them to other users.

## Security Measures

- Message Deletion: Messages are automatically deleted from the sender and receiver within the specified period (5 seconds for sender, 1 minute for receiver).
- User Registration: Users need to register by providing their username and photo data.
- Encryption: All communication between clients and the server is encrypted using SSL/TLS.
- Firewall: The server should be protected by a firewall to prevent unauthorized access.

## Requirements

- Python 3.x
- `socket` library
- `threading` library
- `arecord` command for audio recording
- `fswebcam` command for camera capture
- `curl` command for retrieving location

## Installation

1. Install Python on the Kali machine by running the following command:

sudo apt-get install python3


2. Install the required libraries (`socket` and `threading`) by running the following command:

pip3 install socket threading


3. Install additional tools like `arecord` and `fswebcam` by running the following commands:

sudo apt-get install arecord sudo apt-get install fswebcam


4. Save the Python script as a file, for example, `blackman.py`.


5. Make sure the script has execute permissions by running the following command:

chmod +x blackman.py


6. Run the script by executing the following command:

./blackman.py


## Usage


1. Run the `blackman.py` script on the Kali machine.

2. Users can register by sending a `REGISTER:` command followed by their username and photo data.

3. Users can send messages by sending a `MSG:` command followed by the message.

4. Users can initiate calls by sending a `CALL:` command followed by the target user's IP address.

5. Users can initiate video calls by sending a `VIDEO:` command followed by the target user's IP address.

6. Users can retrieve their location by sending a `LOCATION:` command.

7. Users can record audio by sending an `AUDIO:` command.

8. Users can capture images from their camera by sending a `CAMERA:` command.


## License


This project is licensed under the [MIT License](LICENSE).

This README.md file provides an overview of the Blackman project, lists the features, security measures, requirements, installation and usage instructions, and specifies the license under which the project is distributed.
