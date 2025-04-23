import socket

def tcp_client(host='127.0.0.1', port=65432, n_packets=5, packet_size=1024):
    packet = b'X' * packet_size
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Conectado ao servidor TCP em {host}:{port}")

        s.sendall(f"{n_packets}".encode())
        s.recv(1024) 
        
        for i in range(n_packets):
            s.sendall(packet)
            print(f"Pacote {i+1}/{n_packets} enviado ({packet_size} bytes)")
            

            ack = s.recv(1024)
            print(f"Confirmação recebida: {ack.decode()}")
            
    print(f"Todos os {n_packets} pacotes foram enviados e confirmados")

if __name__ == "__main__":
    tcp_client(n_packets=5, packet_size=1024)
