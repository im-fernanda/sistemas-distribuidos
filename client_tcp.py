import socket
import time, json


def tcp_client(host="127.0.0.1", port=65432, n_packets=5, packet_size=1024):
    # Cria um pacote de dados com o tamanho especificado

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Conectado ao servidor TCP em {host}:{port}")

        # Envia informação sobre quantos pacotes serão enviados
        s.sendall(f"{n_packets}".encode())

        time.sleep(0.1)

        start_time = time.time()  # Inicia o cronômetro

        # Envia os pacotes sem esperar por confirmação explícita
        for i in range(n_packets):
            # Dicionário com dados variados
            data_dict = {
                "message": f"Pacote{i+1}",
                "client_info": {
                    "local_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }

            # Converte para JSON
            json_data = json.dumps(data_dict)

            # Ajusta o tamanho
            if len(json_data) > packet_size:
                json_data = json_data[:packet_size]
            else:
                # Preenche com espaços
                json_data = json_data.ljust(packet_size)

            # Adiciona um cabeçalho com o número do pacote
            packet_with_header = f"{i+1}:".encode() + json_data.encode()
            s.sendall(packet_with_header)
            print(f"Pacote {i+1}/{n_packets} enviado ({packet_size} bytes)")

            time.sleep(0.01)

        end_time = time.time()  # Termina o cronômetro
        total_time = end_time - start_time
        data_transferred = (n_packets * packet_size * 8 / 1e6)  # Dados transferidos em Megabits
        transmission_rate = data_transferred / total_time  # Taxa de transmissão em Mbps

        print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")

    print(f"Todos os {n_packets} pacotes foram enviados")


if __name__ == "__main__":
    tcp_client(n_packets=5, packet_size=60000)
 