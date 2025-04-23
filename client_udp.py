import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('servidor_ip', 5005)
client_socket.settimeout(2.0)  # Define timeout para receber ACK

message = "Olá, servidor UDP!"
max_retries = 5

for attempt in range(max_retries):
    try:
        client_socket.sendto(message.encode(), server_address)
        print(f"Mensagem enviada, tentativa {attempt+1}")
        
        # Espera pelo ACK
        ack, _ = client_socket.recvfrom(1024)
        if ack.decode() == "ACK!":
            print("ACK recebido do servidor!")
            break
    except socket.timeout:
        print(f"Timeout ao aguardar ACK, tentativa {attempt+1}")

client_socket.close()
