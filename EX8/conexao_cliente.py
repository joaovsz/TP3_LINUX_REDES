import socket

def http_client(server_host="127.0.0.1", server_port=5173):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))

    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(server_host)
    client.send(request.encode())

    response = client.recv(4096).decode()
    print("Resposta do servidor:\n", response)

    client.close()

if __name__ == "__main__":
    http_client()
