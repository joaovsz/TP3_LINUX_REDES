import socket
import os
import struct

def upload_file(server_host, server_port, filename):
    if not os.path.exists(filename):
        print(f"Erro: O arquivo '{filename}' não existe.")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    client.send(f"UPLOAD {os.path.basename(filename)}".encode())

    response = client.recv(1024).decode()
    if response != "READY":
        print("Erro no servidor ao iniciar upload.")
        client.close()
        return

    file_size = os.path.getsize(filename)
    client.send(struct.pack("!Q", file_size))

    with open(filename, "rb") as file:
        while chunk := file.read(1024):
            client.send(chunk)

    response = client.recv(1024).decode()
    print("Servidor:", response)
    client.close()

def download_file(server_host, server_port, filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    client.send(f"DOWNLOAD {filename}".encode())

    response = client.recv(1024).decode()
    if response == "OK":
        file_size = struct.unpack("!Q", client.recv(8))[0]

        with open(f"downloaded_{filename}", "wb") as file:
            received = 0
            while received < file_size:
                data = client.recv(min(1024, file_size - received))
                if not data:
                    break
                file.write(data)
                received += len(data)

        print(f"Arquivo {filename} baixado com sucesso.")
    else:
        print(f"Erro: O arquivo {filename} não existe no servidor.")

    client.close()

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080
    action = input("Digite 'upload' ou 'download': ").strip().lower()
    filename = input("Nome do arquivo: ").strip()

    if action == "upload":
        upload_file(server_host, server_port, filename)
    elif action == "download":
        download_file(server_host, server_port, filename)
    else:
        print("Comando inválido.")
