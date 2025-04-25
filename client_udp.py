import socket
import time
import json


def udp_client(host="127.0.0.1", port=5005, n_packets=5, packet_size=1024):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    client_socket.settimeout(2.0)

    try:
        info_message = f"INFO:{n_packets}:{packet_size}".encode()
        client_socket.sendto(info_message, server_address)
        print(f"Informações enviadas ao servidor: {n_packets} pacotes de {packet_size} bytes")

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

        start_time = time.time()
        packets_lost = 0
        retransmissions = 0
        received_packets = set()

        for i in range(n_packets):
            packet_id = i + 1
            data_dict = {
                "message": f"Pacote{packet_id}",
                "client_info": {
                    "local_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }

            json_data = json.dumps(data_dict)
            if len(json_data) > packet_size:
                json_data = json_data[:packet_size]
            else:
                json_data = json_data.ljust(packet_size)

            packet_with_header = f"{packet_id}:".encode() + json_data.encode()

            ack_received = False
            attempt = 0
            MAX_ATTEMPTS = 5

            while not ack_received and attempt < MAX_ATTEMPTS:
                client_socket.sendto(packet_with_header, server_address)
                print(f"Pacote {packet_id}/{n_packets} enviado (tentativa {attempt + 1})")
                try:
                    ack, _ = client_socket.recvfrom(1024)
                    ack_parts = ack.decode().split(":")
                    if len(ack_parts) == 2 and ack_parts[0] == "ACK" and ack_parts[1] == str(packet_id):
                        print(f"Servidor confirmou recebimento do pacote {packet_id}")
                        received_packets.add(packet_id)
                        ack_received = True
                    else:
                        print(f"Recebida confirmação incorreta: {ack.decode()}")
                except socket.timeout:
                    retransmissions += 1
                    attempt += 1
                    print(f"Timeout aguardando ACK do pacote {packet_id}, retransmitindo...")

                time.sleep(0.01)

            if not ack_received:
                print(f"Falha ao enviar pacote {packet_id} após {MAX_ATTEMPTS} tentativas.")
                packets_lost += 1

        end_time = time.time()
        total_time = end_time - start_time
        data_transferred = n_packets * packet_size * 8 / 1e6
        transmission_rate = data_transferred / total_time if total_time > 0 else 0

        print(f"\nResumo da transmissão:")
        print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")
        print(f"Retransmissões totais: {retransmissions}")
        print(f"Pacotes perdidos: {packets_lost}")
        print(f"Pacotes recebidos fora de ordem: {n_packets - len(received_packets)}")
        print(f"Processo de envio de {n_packets} pacotes concluído")

    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client(host="127.0.0.1", n_packets=1, packet_size=60000)
