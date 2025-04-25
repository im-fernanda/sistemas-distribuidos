import socket 
def tcp_server(host="0.0.0.0", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Servidor TCP iniciado em {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")

            data = conn.recv(1024)
            if not data:
                return

            n_packets = int(data.decode())
            print(f"Esperando {n_packets} pacotes")

            packets_received = 0
            buffer = b""  # Buffer para acumular dados

            while packets_received < n_packets:
                data = conn.recv(4096)
                if not data:
                    break

                buffer += data  # Adiciona os novos dados ao buffer
                
                # Processa o buffer enquanto houver pacotes completos
                while True:
                    # Procura o delimitador do cabeçalho
                    header_end = buffer.find(b":")
                    if header_end == -1:
                        break  # Nenhum cabeçalho encontrado
                    
                    try:
                        packet_id = buffer[:header_end].decode()
                        
                        # Tamanho fixo do conteúdo do pacote (1000 bytes no cliente)
                        packet_size = 1000
                        
                        # Verifica se temos dados suficientes
                        if len(buffer) < header_end + 1 + packet_size:
                            break  # Pacote incompleto, aguarda mais dados
                        
                        # Extrai o conteúdo do pacote
                        packet_content = buffer[header_end + 1:header_end + 1 + packet_size]
                        
                        # Remove o pacote processado do buffer
                        buffer = buffer[header_end + 1 + packet_size:]
                        
                        packets_received += 1
                        print(f"Recebido pacote {packet_id}/{n_packets} de {addr}")
                        
                        try:
                            message_content = packet_content.decode("utf-8")
                            print(f"Conteúdo do pacote {packet_id}: {message_content[:50]}...")
                        except UnicodeDecodeError:
                            print(f"Conteúdo do pacote {packet_id} (bytes): {packet_content[:20]}...")
                    
                    except Exception as e:
                        print(f"Erro ao processar pacote: {e}")
                        # Em caso de erro, avança um byte no buffer para tentar novamente
                        buffer = buffer[1:]

            if packets_received == n_packets:
                print(f"Todos os {n_packets} pacotes foram recebidos de {addr}")
            else:
                print(f"Recebidos apenas {packets_received}/{n_packets} pacotes de {addr}")

if __name__ == "__main__":
    tcp_server()