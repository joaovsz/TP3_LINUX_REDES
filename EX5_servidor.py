import socket
import threading

clients = {}

def broadcast(message, sender_socket):
    for client_socket in clients.keys():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, address):
    client_socket.send("Digite seu nome: ".encode())
    name = client_socket.recv(1024).decode().strip()
    clients[client_socket] = name

    welcome_message = f"{name} entrou no chat."
    print(welcome_message)
    broadcast(welcome_message, client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            formatted_message = f"{name}: {message}"
            print(formatted_message)
            broadcast(formatted_message, client_socket)
    except:
        pass
    finally:
        exit_message = f"{name} saiu do chat."
        print(exit_message)
        broadcast(exit_message, client_socket)
        client_socket.close()
        del clients[client_socket]

def start_server(host="0.0.0.0", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor iniciado em {host}:{port}")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()
