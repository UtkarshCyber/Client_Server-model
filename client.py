import socket
import hashlib

def receive_file_chunks(server_host, server_port, chunk_size):
    """Receive file chunks from the server and reassemble the file."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print(f"Connected to server at {server_host}:{server_port}")

        # Receive the file size from the server
        file_size_bytes = client_socket.recv(8)  # Receive 8-byte file size
        file_size = int.from_bytes(file_size_bytes, byteorder='big')
        print(f"Received file size: {file_size} bytes")

        # Receive the checksum from the server
        checksum = client_socket.recv(1024).decode()
        print(f"Received checksum from server: {checksum}")

        # Initialize a buffer to store the file data
        file_data = bytearray(file_size)
        received_chunks = set()

        while len(received_chunks) * chunk_size < file_size:
            try:
                # Receive a chunk from the server
                chunk_data = client_socket.recv(chunk_size + 10)  # Extra bytes for metadata
                if not chunk_data:
                    print("Server closed the connection.")
                    break

                # Extract sequence number and chunk data
                seq_num = int.from_bytes(chunk_data[:4], byteorder='big')
                chunk = chunk_data[4:]

                # Simulate packet corruption detection (optional)
                if is_corrupted(chunk):
                    print(f"Chunk {seq_num} is corrupted. Requesting retransmission...")
                    client_socket.sendall(f"RETRY:{seq_num}".encode())
                    continue

                # Store the chunk in the correct position
                start_index = seq_num * chunk_size
                end_index = start_index + len(chunk)
                file_data[start_index:end_index] = chunk
                received_chunks.add(seq_num)

                # Acknowledge receipt of the chunk
                client_socket.sendall(f"ACK:{seq_num}".encode())

            except ConnectionResetError:
                print("Server forcibly closed the connection.")
                break
            except Exception as e:
                print(f"An error occurred while receiving data: {e}")
                break

    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the server is running at {server_host}:{server_port}.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    finally:
        client_socket.close()

    return bytes(file_data), checksum

def is_corrupted(chunk):
    """Simulate packet corruption detection (optional)."""
    # For simplicity, we can assume corruption if the chunk contains null bytes
    return b'\x00' in chunk

def verify_checksum(file_data, expected_checksum):
    """Verify the checksum of the reassembled file."""
    sha256_hash = hashlib.sha256(file_data).hexdigest()
    print(f"Calculated checksum: {sha256_hash}")
    print(f"Expected checksum: {expected_checksum}")
    return sha256_hash == expected_checksum

def main():
    server_host = "127.0.0.1"
    server_port = 8080
    chunk_size = 1024  # Chunk size (1 KB)

    # Receive file chunks and checksum from the server
    file_data, checksum = receive_file_chunks(server_host, server_port, chunk_size)
    #expected_checksum="g4651d4gs344w6e1fe68w"

    if file_data and checksum:
        # Verify the checksum
        #if verify_checksum(file_data, expected_checksum):
        if verify_checksum(file_data, checksum):
            print("File transfer successful! Checksum verified.")
            print(f"Reassembled file content: {file_data.decode()}")
        else:
            print("File transfer failed! Checksum mismatch.")
    else:
        print("File transfer failed due to connection issues.")

if __name__ == "__main__":
    main()