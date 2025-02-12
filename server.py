import socket
import hashlib
import os
import random

def split_file_into_chunks(file_path, chunk_size):
    """Split the file into fixed-size chunks and assign sequence numbers."""
    chunks = []
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def calculate_checksum(file_path):
    """Calculate the SHA256 checksum of the file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def simulate_packet_corruption(chunk, corruption_probability=0.1):
    """Simulate packet corruption with a given probability."""
    if random.random() < corruption_probability:
        # Corrupt the chunk by altering a few bytes
        chunk = bytearray(chunk)
        for i in range(min(10, len(chunk))):  # Corrupt up to 10 bytes
            if random.random() < 0.5:
                chunk[i] = random.randint(0, 255)
        return bytes(chunk)
    return chunk

def send_file_chunks(server_host, server_port, file_path, chunk_size):
    """Send file chunks to the client with optional corruption simulation."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)

    print(f"Server listening on {server_host}:{server_port}...")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to client: {client_address}")

    try:
        # Get the file size
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        # Send the file size to the client
        client_socket.sendall(file_size.to_bytes(8, byteorder='big'))  # Send as 8-byte integer
        print(f"Sent file size: {file_size} bytes")

        # Split the file into chunks
        chunks = split_file_into_chunks(file_path, chunk_size)
        checksum = calculate_checksum(file_path)

        # Send the checksum to the client
        client_socket.sendall(checksum.encode())
        print(f"Sent checksum: {checksum}")

        # Send each chunk with a sequence number
        for seq_num, chunk in enumerate(chunks):
            # Simulate packet corruption
            chunk = simulate_packet_corruption(chunk)

            # Add sequence number to the chunk
            chunk_with_seq = seq_num.to_bytes(4, byteorder='big') + chunk

            # Send the chunk to the client
            client_socket.sendall(chunk_with_seq)
            print(f"Sent chunk {seq_num} of size {len(chunk)} bytes.")

            # Wait for acknowledgment
            ack = client_socket.recv(1024).decode()
            if ack.startswith("ACK"):
                print(f"Chunk {seq_num} acknowledged.")
            elif ack.startswith("RETRY"):
                print(f"Retransmitting chunk {seq_num}...")
                client_socket.sendall(chunk_with_seq)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        print("Server connection closed.")

def main():
    server_host = "127.0.0.1"
    server_port = 8080
    file_path = "data.txt"  # File to transfer
    chunk_size = 1024  # Chunk size (1 KB)

    # Send file chunks to the client
    send_file_chunks(server_host, server_port, file_path, chunk_size)

if __name__ == "__main__":
    main()