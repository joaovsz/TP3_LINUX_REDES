import ssl
import socket
import datetime

def get_ssl_certificate(hostname, port=443):
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            cipher = ssock.cipher()

    return cert, cipher

def parse_certificate(cert):
    subject = dict(x[0] for x in cert["subject"])
    issuer = dict(x[0] for x in cert["issuer"])
    valid_from = datetime.datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
    valid_to = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

    return {
        "Nome Comum (CN)": subject.get("commonName", "N/A"),
        "Organização": subject.get("organizationName", "N/A"),
        "Emitido por": issuer.get("commonName", "N/A"),
        "Data de Início": valid_from.strftime("%d/%m/%Y %H:%M:%S"),
        "Data de Expiração": valid_to.strftime("%d/%m/%Y %H:%M:%S"),
    }

if __name__ == "__main__":
    hostname = input("Digite o domínio do servidor HTTPS: ").strip()

    try:
        cert, cipher = get_ssl_certificate(hostname)
        cert_info = parse_certificate(cert)

        print("\nInformações do Certificado SSL/TLS")
        for key, value in cert_info.items():
            print(f"{key}: {value}")

        print(f"\nCifra Utilizada: {cipher[0]} | Tamanho da Chave: {cipher[2]} bits")

    except Exception as e:
        print(f"Erro ao obter o certificado: {e}")
