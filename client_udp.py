import socket
import time

def udp_client(host='127.0.0.1', port=5005, n_packets=5, packet_size=1024, max_retries=3):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    client_socket.settimeout(2.0)  # Define timeout para receber ACK
    
    try:
        # Envia informações sobre N e T
        info_message = f"INFO:{n_packets}:{packet_size}".encode()

        for attempt in range(max_retries):
            try:
                client_socket.sendto(info_message, server_address)
                print(f"Informações enviadas ao servidor: {n_packets} pacotes de {packet_size} bytes")
                
                # Espera pelo ACK da mensagem de informação
                ack, _ = client_socket.recvfrom(1024)
                if ack.decode() == "ACK:INFO":
                    print("Servidor confirmou recebimento das informações")
                    break
            except socket.timeout:
                print(f"Timeout ao aguardar confirmação das informações, tentativa {attempt+1}/{max_retries}")
                if attempt == max_retries - 1:
                    print("Número máximo de tentativas excedido. Encerrando.")
                    return
        
        # Cria um pacote de dados com o tamanho especificado
        packet_data = b'X' * packet_size
        
        # Envia os N pacotes
        start_time = time.time()  # Inicia o cronômetro
        packets_lost = 0  # Contador de pacotes perdidos
        retransmissions = 0  # Contador de retransmissões
        received_packets = set()  # Conjunto para verificar ordem de entrega
        for i in range(n_packets):
            # Adiciona um cabeçalho com o número do pacote
            packet_with_header = f"{i+1}:".encode() + packet_data
            
            # Tenta enviar o pacote com retentativas
            for attempt in range(max_retries):
                try:
                    client_socket.sendto(packet_with_header, server_address)
                    print(f"Pacote {i+1}/{n_packets} enviado ({packet_size} bytes)")
                    
                    # Espera pelo ACK
                    ack, _ = client_socket.recvfrom(1024)
                    ack_parts = ack.decode().split(':')
                    
                    if len(ack_parts) == 2 and ack_parts[0] == "ACK" and ack_parts[1] == str(i+1):
                        print(f"Servidor confirmou recebimento do pacote {i+1}/{n_packets}")
                        received_packets.add(i+1)  # Adiciona ao conjunto de pacotes recebidos
                        break
                    else:
                        print(f"Recebida confirmação incorreta: {ack.decode()}")
                        retransmissions += 1  # Incrementa retransmissões
                        
                except socket.timeout:
                    print(f"Timeout ao aguardar confirmação do pacote {i+1}, tentativa {attempt+1}/{max_retries}")
                    if attempt == max_retries - 1:
                        print(f"Falha ao enviar o pacote {i+1} após {max_retries} tentativas")
                        packets_lost += 1  # Incrementa pacotes perdidos
            
            time.sleep(0.01)
        
        end_time = time.time()  # Termina o cronômetro
        total_time = end_time - start_time
        data_transferred = n_packets * packet_size * 8 / 1e6  # Dados transferidos em Megabits
        transmission_rate = data_transferred / total_time  # Taxa de transmissão em Mbps
        
        print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")
        print(f"Pacotes perdidos: {packets_lost}")
        print(f"Retransmissões: {retransmissions}")
        print(f"Pacotes recebidos fora de ordem: {n_packets - len(received_packets)}")
        
        print(f"Processo de envio de {n_packets} pacotes concluído")
        
    finally:
        client_socket.close()

if __name__ == "__main__":
    udp_client(host='127.0.0.1', n_packets=20, packet_size=1024)