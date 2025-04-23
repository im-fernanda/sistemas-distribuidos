import socket

def udp_server(host='', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Servidor UDP iniciado em {host}:{port}")
        
        # Recebe informação sobre quantos pacotes serão recebidos
        data, addr = s.recvfrom(1024)
        n_packets = int(data.decode())
        s.sendto(b"Pronto para receber pacotes", addr)
        print(f"Esperando {n_packets} pacotes de {addr}")
        
        # Recebe os pacotes
        for _ in range(n_packets):
            data, addr = s.recvfrom(4096)
            
            # Extrai o ID do pacote (formato: "ID:conteúdo")
            parts = data.split(b':', 1)
            if len(parts) == 2:
                packet_id = parts[0].decode()
                packet_content = parts[1]
                print(f"Pacote {int(packet_id)+1}/{n_packets} recebido ({len(data)} bytes)")
                
                # Envia confirmação
                s.sendto(f"Pacote {int(packet_id)+1} recebido com sucesso".encode(), addr)
            
        print(f"Todos os {n_packets} pacotes foram recebidos")

if __name__ == "__main__":
    udp_server()
