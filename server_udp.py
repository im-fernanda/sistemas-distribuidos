import socket

def udp_server(host='0.0.0.0', port=5005):
    # Criação do socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print(f"Servidor UDP aguardando pacotes em {host}:{port}...")
    
    while True:
        try:
            # Recebe o primeiro pacote que contém informações sobre N e T
            data, addr = server_socket.recvfrom(1024)
            info = data.decode().split(':')
            
            if len(info) == 3 and info[0] == "INFO":
                n_packets = int(info[1])
                packet_size = int(info[2])
                print(f"Cliente {addr} vai enviar {n_packets} pacotes de tamanho {packet_size}")
                
                # Envia ACK para o pacote de informação
                server_socket.sendto("ACK:INFO".encode(), addr)
                
                # Recebe os N pacotes
                for i in range(n_packets):
                    packet_data, _ = server_socket.recvfrom(packet_size + 20)  # Buffer extra para o cabeçalho
                    
                    # Extrai o ID do pacote
                    header_end = packet_data.find(b':')
                    if header_end != -1:
                        packet_id = packet_data[:header_end].decode()
                        data = packet_data[header_end+1:]
                        
                        print(f"Recebido pacote {packet_id}/{n_packets} de {addr} ({len(data)} bytes)")
                        
                        # Envia ACK para este pacote
                        ack_message = f"ACK:{packet_id}".encode()
                        server_socket.sendto(ack_message, addr)
                
                print(f"Foram recebidos {n_packets} pacotes recebidos de {addr}")
            
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    udp_server()
