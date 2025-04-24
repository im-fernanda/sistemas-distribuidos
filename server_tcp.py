import socket
import time


def tcp_server(host="0.0.0.0", port=65432):
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

                # Extrai o ID do pacote e o conteúdo
                header_end = data.find(b":")
                if header_end != -1:
                    packet_id = data[:header_end].decode()
                    packet_content = data[header_end + 1 :]

                    packets_received += 1
                    print(
                        f"Recebido pacote {packet_id}/{n_packets} de {addr} ({len(data)} bytes)"
                    )

                    # Tenta decodificar e mostrar o conteúdo
                    try:
                        message_content = packet_content.decode("utf-8")
                        print(
                            f"Conteúdo do pacote {packet_id}: {message_content[:50]}..."
                        )
                    except UnicodeDecodeError:
                        # Se não for texto decodificável, mostra os primeiros bytes
                        print(
                            f"Conteúdo do pacote {packet_id} (bytes): {packet_content[:20]}..."
                        )
                else:
                    packets_received += 1
                    print(
                        f"Recebido pacote {packets_received}/{n_packets} de {addr} ({len(data)} bytes)"
                    )
                    print(f"Formato de pacote não reconhecido: {data[:50]}...")

            end_time = time.time()  # Termina o cronômetro
            total_time = end_time - start_time

            # Calcula com base no tamanho real dos dados recebidos
            avg_packet_size = (
                1026  # Baseado na sua pergunta anterior (1026 bytes por pacote)
            )
            data_transferred = (
                packets_received * avg_packet_size * 8 / 1e6
            )  # Dados transferidos em Megabits
            transmission_rate = (
                data_transferred / total_time
            )  # Taxa de transmissão em Mbps

            print(f"Taxa de transmissão: {transmission_rate:.2f} Mbps")

            if packets_received == n_packets:
                print(f"Todos os {n_packets} pacotes foram recebidos de {addr}")
            else:
                print(
                    f"Recebidos apenas {packets_received}/{n_packets} pacotes de {addr}"
                )


if __name__ == "__main__":
    tcp_server()
