import socket

def start_udp_client(server_host="127.0.0.1", server_port=8080):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input("Digite sua mensagem (ou 'sair' para encerrar): ")
        client.sendto(message.encode(), (server_host, server_port))

        if message.lower() == "sair":
            break

        response, _ = client.recvfrom(1024)
        print("Servidor:", response.decode())

    client.close()

if __name__ == "__main__":
    start_udp_client()
