import socket
import time
import sys

def iniciar_servidor(servidor_host='', servidor_porta=12345, buffer_size=65535):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Aumentar o buffer de recepção para evitar perdas
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**24)
    
    try:
        # Associar o socket à porta
        servidor_socket.bind((servidor_host, servidor_porta))
        print(f"Servidor UDP iniciado em {servidor_host if servidor_host else '0.0.0.0'}:{servidor_porta}")
        
        # Inicializar contadores
        pacotes_recebidos = 0
        bytes_recebidos = 0
        clientes = {}
        tempo_inicio = time.time()
        
        # Loop para receber dados
        while True:
            try:
                dados, endereco = servidor_socket.recvfrom(buffer_size)
                
                # Atualizar contadores
                pacotes_recebidos += 1
                bytes_recebidos += len(dados)
                
                
                # Processar os dados recebidos
                try:
                    mensagem = dados.decode('utf-8')
                    seq_num = mensagem.split('-')[0] if '-' in mensagem else 'N/A'
                    # Exibir informações para cada pacote
                    print(f"Pacote #{pacotes_recebidos} (Seq: {seq_num}) de {endereco}: {len(dados)} bytes")

                    if pacotes_recebidos % 10 == 0:  # Mostra estatísticas de taxa a cada 10 pacotes
                        tempo_atual = time.time()
                        tempo_decorrido = tempo_atual - tempo_inicio
                        taxa_kb_por_segundo = (bytes_recebidos / 1024) / tempo_decorrido if tempo_decorrido > 0 else 0
                        print(f"Taxa média: {taxa_kb_por_segundo:.2f} KB/s ({(taxa_kb_por_segundo*1024):.2f} B/s)")
                except UnicodeDecodeError:
                    print(f"Recebido pacote binário de {endereco}: {len(dados)} bytes")
                
                # Enviar resposta de confirmação
                resposta = f"ACK:{seq_num}"
                servidor_socket.sendto(resposta.encode('utf-8'), endereco)
                
            except ConnectionResetError:
                print("Erro 10054: Conexão resetada pelo host remoto. Continuando...")
                time.sleep(0.1)
                continue
                
            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(0.1)
                continue
                
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
        

        tempo_total = time.time() - tempo_inicio
        print("\n" + "=" * 50)
        print("ESTATÍSTICAS DO SERVIDOR:")
        print(f"Tempo de execução: {tempo_total:.2f} segundos")
        print(f"Total de pacotes recebidos: {pacotes_recebidos}")
        print(f"Total de bytes recebidos: {bytes_recebidos} ({bytes_recebidos/1024/1024:.2f} MB)")
        
        if tempo_total > 0:
            taxa_kb_por_segundo = (bytes_recebidos / 1024) / tempo_total
            taxa_bytes_por_segundo = taxa_kb_por_segundo * 1024
            taxa_mbps = (bytes_recebidos * 8) / tempo_total / 1024 / 1024
            
            print(f"Taxa média de transferência: {taxa_kb_por_segundo:.2f} KB/s ({taxa_bytes_por_segundo:.2f} MB/s)")
            print(f"Taxa média de transferência: {taxa_mbps:.2f} Mbps")
        
        print("=" * 50)
    
    finally:
        servidor_socket.close()

if __name__ == "__main__":

    iniciar_servidor(servidor_host = '', servidor_porta = 12345, buffer_size=65535)
