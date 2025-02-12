Real-Time File Transfer and Verification System

This project implements a real-time file transfer system between a client and a server using TCP sockets. The system ensures file integrity by splitting the file into chunks, transmitting them with sequence numbers, and verifying the file using a checksum (SHA256). The server also simulates packet corruption to test the client's ability to detect and handle errors.

Prerequisites

- Python 3.12.2
- A file to transfer (e.g., data.txt)

Create a virtual environment:
- python -m venv venv

Activate the virtual environment:
On Windows:
- venv\Scripts\activate

How to Run:

1. Clone the Repository
Clone or download the project files to your local machine.

2. Set Up the Environment
Ensure Python 3.x is installed. No additional dependencies are required.

3. Prepare the File to Transfer
Place the file you want to transfer (e.g. data.txt) in the same directory as the server script.

4. Start the Server
Run the server script to listen for incoming connections:
python server.py

5. Start the Client
Run the client script to connect to the server and receive the file:
python client.py


Code Overview:

Server (server.py)
Functionality:
- Listens for client connections on a specified port (default: 8080).
- Splits the file into chunks and sends them to the client.
- Simulates packet corruption for testing purposes.
- Sends the file size and checksum to the client.

Key Functions:
- split_file_into_chunks: Splits the file into fixed-size chunks.
- calculate_checksum: Computes the SHA256 checksum of the file.
- simulate_packet_corruption: Randomly corrupts chunks to simulate network errors.
- send_file_chunks: Sends file chunks, checksum, and file size to the client.


Client (client.py)
Functionality:
- Connects to the server and receives the file size, checksum, and file chunks.
- Reassembles the file and verifies its integrity using the checksum.
- Detects corrupted chunks and requests retransmission.

Key Functions:
- receive_file_chunks: Receives file chunks and reassembles the file.
- is_corrupted: Detects corrupted chunks.
- verify_checksum: Verifies the file integrity using the checksum.

