import socket
import time

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
            
            packets_received = 0
            start_time = time.time()  # Inicia o cronômetro
            
            while packets_received < n_packets:
                data = conn.recv(4096)  
                
                if not data:
                    break  
                    
                packets_received += 1
                print(f"Pacote {packets_received}/{n_packets} recebido ({len(data)} bytes)")
                
            end_time = time.time()  # Termina o cronômetro
            total_time = end_time - start_time
            data_transferred = packets_received * len(data) * 8 / 1e6  # Dados transferidos em Megabits
            transmission_rate = data_transferred / total_time  # Taxa de transmissão em Mbps
            
            print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")

if __name__ == "__main__":
    tcp_server()