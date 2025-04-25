import socket


def udp_server(host="0.0.0.0", port=5005):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor UDP aguardando pacotes em {host}:{port}...")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            info = data.decode().split(":")

            if len(info) == 3 and info[0] == "INFO":
                n_packets = int(info[1])
                packet_size = int(info[2])
                print(f"Cliente {addr} vai enviar {n_packets} pacotes de tamanho {packet_size}")

                server_socket.sendto("ACK:INFO".encode(), addr)
                server_socket.settimeout(5.0)

                packets_received = 0
                seen_ids = set()
                retransmissions_detected = 0

                try:
                    for _ in range(n_packets * 2):
                        packet_data, _ = server_socket.recvfrom(packet_size + 20)

                        header_end = packet_data.find(b":")
                        if header_end != -1:
                            packet_id = packet_data[:header_end].decode()
                            data = packet_data[header_end + 1:]

                            if packet_id in seen_ids:
                                retransmissions_detected += 1
                                print(f"Retransmissão detectada do pacote {packet_id}")
                            else:
                                seen_ids.add(packet_id)
                                packets_received += 1
                                print(f"Recebido pacote {packet_id}/{n_packets} de {addr} ({len(data)} bytes)")

                                try:
                                    message_content = data.decode("utf-8")
                                    print(f"Conteúdo do pacote {packet_id}: {message_content[:50]}...")
                                except UnicodeDecodeError:
                                    print(f"Conteúdo do pacote {packet_id} (bytes): {data[:20]}...")

                            ack_message = f"ACK:{packet_id}".encode()
                            server_socket.sendto(ack_message, addr)

                        if packets_received == n_packets:
                            break

                except socket.timeout:
                    print(f"Timeout após receber {packets_received} pacotes")

                finally:
                    server_socket.settimeout(None)
                    print(f"\nResumo da recepção:")
                    print(f"Pacotes recebidos: {packets_received}/{n_packets}")
                    print(f"Retransmissões detectadas: {retransmissions_detected}")
                    print("Aguardando novo cliente...\n")

        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    udp_server()
