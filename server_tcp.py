import socket

def tcp_server(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((host, port))
        
        s.listen()
        print(f"Servidor TCP iniciado em {host}:{port}")
        
        # Aceita conexão do cliente
        conn, addr = s.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")
            
            # Recebe informação sobre quantos pacotes serão recebidos
            data = conn.recv(1024)
            if not data:
                return
                
            n_packets = int(data.decode())
            print(f"Esperando {n_packets} pacotes")
            
            # Recebe os pacotes sem enviar confirmação explícita
            packets_received = 0
            
            while packets_received < n_packets:
                data = conn.recv(4096)  
                
                if not data:
                    break  
                    
                packets_received += 1
                print(f"Pacote {packets_received}/{n_packets} recebido ({len(data)} bytes)")
                
            print(f"Todos os {packets_received} pacotes foram recebidos")

if __name__ == "__main__":
    tcp_server()
