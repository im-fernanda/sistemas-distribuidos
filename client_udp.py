import socket
import time

def udp_client(host="192.168.0.243", port=65432, n_packets=5, packet_size=1024):
    # Cria um pacote de dados com o tamanho especificado
    packet = b'X' * packet_size
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia informação sobre quantos pacotes serão enviados
        s.sendto(f"{n_packets}".encode(), (host, port))
        data, _ = s.recvfrom(1024)  # Recebe confirmação
        print(f"Resposta do servidor: {data.decode()}")
        
        # Envia os pacotes
        for i in range(n_packets):
            # Adiciona número do pacote no início para identificação
            packet_with_id = f"{i}:".encode() + packet
            
            s.sendto(packet_with_id, (host, port))
            print(f"Pacote {i+1}/{n_packets} enviado ({packet_size} bytes)")
            
            # Recebe confirmação do servidor
            s.settimeout(2.0)  # Define timeout para receber confirmação
            try:
                ack, addr = s.recvfrom(1024)
                print(f"Confirmação recebida: {ack.decode()}")
            except socket.timeout:
                print(f"Timeout ao receber confirmação do pacote {i+1}")
            
            time.sleep(0.1)  # Pequena pausa entre pacotes
            
    print(f"Processo de envio de {n_packets} pacotes concluído")

if __name__ == "__main__":
    udp_client(n_packets=5, packet_size=1024)
