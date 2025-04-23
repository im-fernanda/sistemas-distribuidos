import socket

def tcp_server(host='', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor TCP iniciado em {host}:{port}")
        
        conn, addr = s.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")
            
            n_packets = int(conn.recv(1024).decode())
            conn.sendall(b"Pronto para receber pacotes")
            print(f"Esperando {n_packets} pacotes")
            

            for i in range(n_packets):
                data = conn.recv(4096) 
                print(f"Pacote {i+1}/{n_packets} recebido ({len(data)} bytes)")
                
 
                conn.sendall(f"Pacote {i+1} recebido com sucesso".encode())
                
            print(f"Todos os {n_packets} pacotes foram recebidos")

if __name__ == "__main__":
    tcp_server()
