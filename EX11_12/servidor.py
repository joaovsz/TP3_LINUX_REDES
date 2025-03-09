import socket
import os
import struct

def handle_client(client_socket):
    request = client_socket.recv(1024).decode().strip()

    if not request:
        client_socket.close()
        return

    try:
        command, filename = request.split(maxsplit=1)
    except ValueError:
        client_socket.send("Comando inválido".encode())
        client_socket.close()
        return

    if command == "UPLOAD":
        file_path = os.path.join("server_files", filename)
        client_socket.send("READY".encode())
        file_size = struct.unpack("!Q", client_socket.recv(8))[0]

        with open(file_path, "wb") as file:
            received = 0
            while received < file_size:
                data = client_socket.recv(min(1024, file_size - received))
                if not data:
                    break
                file.write(data)
                received += len(data)

        print(f"Arquivo {filename} ({file_size} bytes) recebido com sucesso.")
        client_socket.send(f"Upload de {filename} concluído.".encode())

    elif command == "DOWNLOAD":
        file_path = os.path.join("server_files", filename)
        if os.path.exists(file_path):
            client_socket.send("OK".encode())

            file_size = os.path.getsize(file_path)
            client_socket.send(struct.pack("!Q", file_size))

            with open(file_path, "rb") as file:
                while chunk := file.read(1024):
                    client_socket.send(chunk)
            print(f"Arquivo {filename} enviado com sucesso.")
        else:
            client_socket.send("ERRO".encode())

    client_socket.close()

def start_file_server(host="0.0.0.0", port=8080):
    if not os.path.exists("server_files"):
        os.makedirs("server_files")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor de arquivos rodando em {host}:{port}")

    while True:
        client_socket, _ = server.accept()
        handle_client(client_socket)

if __name__ == "__main__":
    start_file_server()
