import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 5005))

print("Servidor UDP aguardando pacotes...")

while True:
    data, addr = server_socket.recvfrom(1024)
    print(f"Recebido: {data.decode()} de {addr}")
    
    # Envia ACK explicitamente de volta ao cliente
    ack_message = "ACK!".encode()
    server_socket.sendto(ack_message, addr)
