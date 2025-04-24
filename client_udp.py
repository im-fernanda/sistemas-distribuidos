import socket
import time
import json, random

def udp_client(host="127.0.0.1", port=5005, n_packets=5, packet_size=1024):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    client_socket.settimeout(2.0)  # Define timeout para receber ACK

    try:
        # Envia informações sobre N e T
        info_message = f"INFO:{n_packets}:{packet_size}".encode()
        client_socket.sendto(info_message, server_address)
        print(
            f"Informações enviadas ao servidor: {n_packets} pacotes de {packet_size} bytes"
        )

        # Espera pelo ACK da mensagem de informação
        try:
            ack, _ = client_socket.recvfrom(1024)
            if ack.decode() == "ACK:INFO":
                print("Servidor confirmou recebimento das informações")
            else:
                print(f"Recebida confirmação inesperada: {ack.decode()}")
                return
        except socket.timeout:
            print("Timeout ao aguardar confirmação das informações. Encerrando.")
            return

        for i in range(n_packets):
            # Dicionário com dados variados
            data_dict = {
                "timestamp": time.time(),
                "message": f"Este é o pacote número {i+1}",
                "random_value": random.randint(1, 1000),
                "client_info": {
                    "hostname": socket.gethostname(),
                    "local_time": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }

            # Converte para JSON
            json_data = json.dumps(data_dict)

            # Ajusta o tamanho
            if len(json_data) > packet_size:
                json_data = json_data[:packet_size]
            else:
                # Preenche com espaços 
                json_data = json_data.ljust(packet_size)

            # Envia os N pacotes

            packet_with_header = f"{i+1}:".encode() + json_data.encode()

            client_socket.sendto(packet_with_header, server_address)
            print(f"Pacote {i+1}/{n_packets} enviado ({packet_size} bytes)")

            # Espera pelo ACK
            try:
                ack, _ = client_socket.recvfrom(1024)
                ack_parts = ack.decode().split(":")

                if (
                    len(ack_parts) == 2
                    and ack_parts[0] == "ACK"
                    and ack_parts[1] == str(i + 1)
                ):
                    print(f"Servidor confirmou recebimento do pacote {i+1}/{n_packets}")
                else:
                    print(f"Recebida confirmação incorreta: {ack.decode()}")
            except socket.timeout:
                print(f"Timeout ao aguardar confirmação do pacote {i+1}")

            time.sleep(0.01) 

            print(f"Processo de envio de {n_packets} pacotes concluído")

    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client(host="127.0.0.1", n_packets=20, packet_size=1024)
