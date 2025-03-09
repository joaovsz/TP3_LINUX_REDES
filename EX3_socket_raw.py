import socket
import struct

def eth_addr(a):
    return ':'.join('%02x' % b for b in a)

try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
except socket.error as msg:
    print('Não foi possível criar o socket. Código do erro: ' + str(msg.errno) + ' Mensagem: ' + msg.strerror)
    exit()

while True:
    packet = s.recvfrom(65565)
    packet = packet[0]
    
    eth_length = 14
    eth_header = packet[:eth_length]
    eth = struct.unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    
    print('MAC de Destino: ' + eth_addr(packet[0:6]) + ' MAC de Origem: ' + eth_addr(packet[6:12]) + ' Protocolo: ' + str(eth_protocol))

