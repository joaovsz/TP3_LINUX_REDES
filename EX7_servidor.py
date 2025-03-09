import socket

def start_udp_server(host="0.0.0.0", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"Servidor UDP rodando em {host}:{port}")

    while True:
        data, client_address = server.recvfrom(1024)
        message = data.decode()
        print(f"Mensagem de {client_address}: {message}")

        if message.lower() == "sair":
            print(f"Cliente {client_address} saiu do chat.")
            continue

        response = f"Recebido: {message}"
        server.sendto(response.encode(), client_address)

if __name__ == "__main__":
    start_udp_server()
