import socket
import time


def udp_server(host="0.0.0.0", port=5005):
    # Criação do socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor UDP aguardando pacotes em {host}:{port}...")

    while True:
        try:
            # Recebe o primeiro pacote que contém informações sobre N e T
            data, addr = server_socket.recvfrom(1024)
            info = data.decode().split(":")

            if len(info) == 3 and info[0] == "INFO":
                n_packets = int(info[1])
                packet_size = int(info[2])
                print(
                    f"Cliente {addr} vai enviar {n_packets} pacotes de tamanho {packet_size}"
                )

                # Envia ACK para o pacote de informação
                server_socket.sendto("ACK:INFO".encode(), addr)

                # Define um timeout para receber pacotes
                server_socket.settimeout(5.0)  # 5 segundos de timeout

                # Contador real de pacotes recebidos
                packets_received = 0
                received_ids = set()  # Conjunto para verificar ordem de entrega
                retransmissions = 0  # Contador de retransmissões
                start_time = time.time()  # Inicia o cronômetro

                # Recebe os pacotes
                try:
                    for i in range(n_packets):
                        packet_data, _ = server_socket.recvfrom(
                            packet_size + 20
                        )  # Buffer extra para o cabeçalho

                        # Extrai o ID do pacote
                        header_end = packet_data.find(b":")
                        if header_end != -1:
                            packet_id = packet_data[:header_end].decode()
                            data = packet_data[header_end + 1 :]

                            packets_received += 1
                            print(
                                f"Recebido pacote {packet_id}/{n_packets} de {addr} ({len(data)} bytes)"
                            )

                            # Verifica se o pacote já foi recebido
                            if packet_id in received_ids:
                                retransmissions += 1
                            else:
                                received_ids.add(packet_id)

                            # Envia ACK para este pacote
                            ack_message = f"ACK:{packet_id}".encode()
                            server_socket.sendto(ack_message, addr)

                except socket.timeout:
                    print(f"Timeout após receber {packets_received} pacotes")

                finally:
                    # Restaura o comportamento sem timeout
                    server_socket.settimeout(None)

                    # Verifica se recebeu todos os pacotes prometidos
                    if packets_received == n_packets:
                        print(f"Todos os {n_packets} pacotes foram recebidos de {addr}")
                    else:
                        print(
                            f"Recebidos apenas {packets_received}/{n_packets} pacotes de {addr}"
                        )

                    end_time = time.time()  # Termina o cronômetro
                    total_time = end_time - start_time
                    data_transferred = packets_received * packet_size * 8 / 1e6  # Dados transferidos em Megabits
                    transmission_rate = data_transferred / total_time  # Taxa de transmissão em Mbps
                    
                    print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")
                    print(f"Pacotes perdidos: {n_packets - packets_received}")
                    print(f"Retransmissões: {retransmissions}")
                    print(f"Pacotes recebidos fora de ordem: {n_packets - len(received_ids)}")

        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    udp_server()