import socket
import time


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

        # Cria um pacote de dados com o tamanho especificado
        packet_data = b"X" * packet_size

        # Envia os N pacotes
        for i in range(n_packets):
            # Adiciona um cabeçalho com o número do pacote
            packet_with_header = f"{i+1}:".encode() + packet_data

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
