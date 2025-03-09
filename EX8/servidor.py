import os
import socket

def start_http_server(host="0.0.0.0", port=5173):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor HTTP rodando em {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        request = client_socket.recv(1024).decode()
        print(f"Requisição recebida de {client_address}:\n{request}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "index.html")

        try:
            with open(file_path, "r") as file:
                response_body = file.read()

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )
        except FileNotFoundError:
            response_body = "<h1>404 - Página não encontrada</h1>"
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )

        client_socket.send(response.encode())
        client_socket.close()

if __name__ == "__main__":
    start_http_server()
