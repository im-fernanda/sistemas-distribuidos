import socket
import time

def udp_client(host='127.0.0.1', port=5005, n_packets=20, packet_size=1024, max_retries=3):
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
                        break
                    else:
                        print(f"Recebida confirmação incorreta: {ack.decode()}")
                        
                except socket.timeout:
                    print(f"Timeout ao aguardar confirmação do pacote {i+1}, tentativa {attempt+1}/{max_retries}")
                    if attempt == max_retries - 1:
                        print(f"Falha ao enviar o pacote {i+1} após {max_retries} tentativas")
            

            time.sleep(0.01)
        
        print(f"Processo de envio de {n_packets} pacotes concluído")
        
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Substitua 'servidor_ip' pelo IP real do servidor
    udp_client(host='127.0.0.1', n_packets=20, packet_size=1024)
