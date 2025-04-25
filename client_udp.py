import socket
import time
import random
import string
import sys

def gerar_payload(tamanho):
    """Gera uma string aleatória com o tamanho especificado em bytes"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanho))

def enviar_pacotes_udp(servidor_host, servidor_porta, num_pacotes, tamanho_pacote, max_retransmissoes=3, timeout=2):
    # Criar o socket UDP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.settimeout(timeout)  # Definir timeout em segundos
    
    # Aumentar o buffer de envio
    cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**24)
    
    # Inicializar métricas
    pacotes_enviados = 0
    pacotes_recebidos = 0
    pacotes_perdidos = 0
    total_retransmissoes = 0
    tempos_resposta = []
    bytes_enviados = 0
    
    # Gerar payload com o tamanho especificado (uma vez só para economizar processamento)
    payload_base = gerar_payload(tamanho_pacote)
    
    print(f"Iniciando envio de {num_pacotes} pacotes de {tamanho_pacote} bytes cada")
    print("-" * 50)
    
    tempo_inicio_total = time.time()
    
    for i in range(num_pacotes):
        # Adicionar número de sequência ao início do payload
        payload = f"{i:08d}-" + payload_base[:tamanho_pacote - 9]  # -9 para o prefixo "00000000-"
        
        retransmissoes = 0
        pacote_recebido = False
        
        while retransmissoes <= max_retransmissoes and not pacote_recebido:
            try:
                inicio = time.time()
                
                # Enviar dados para o servidor
                bytes_enviados_pacote = cliente_socket.sendto(payload.encode('utf-8'), (servidor_host, servidor_porta))
                bytes_enviados += bytes_enviados_pacote
                pacotes_enviados += 1
                
                # Receber resposta
                dados, endereco = cliente_socket.recvfrom(1024)
                resposta = dados.decode('utf-8')
                
                fim = time.time()
                tempo_resposta = (fim - inicio) * 1000  # Converter para milissegundos
                tempos_resposta.append(tempo_resposta)
                
                print(f"Pacote {i+1}/{num_pacotes}: Enviado {bytes_enviados_pacote} bytes, recebido em {tempo_resposta:.2f}ms")
                pacotes_recebidos += 1
                pacote_recebido = True
                
            except socket.timeout:
                retransmissoes += 1
                total_retransmissoes += 1
                print(f"Pacote {i+1}/{num_pacotes}: Timeout! Tentativa de retransmissão {retransmissoes}/{max_retransmissoes}")
                
                if retransmissoes > max_retransmissoes:
                    print(f"Pacote {i+1}/{num_pacotes}: Falha após {max_retransmissoes} tentativas")
                    pacotes_perdidos += 1
        
        # Pequena pausa entre pacotes para não sobrecarregar
        time.sleep(0.01)
    
    tempo_total = time.time() - tempo_inicio_total
    
    # Fechar o socket
    cliente_socket.close()
    
    # Calcular estatísticas
    taxa_perda = (pacotes_perdidos / num_pacotes) * 100 if num_pacotes > 0 else 0
    tempo_medio = sum(tempos_resposta) / len(tempos_resposta) if tempos_resposta else 0
    
    # Calcular taxa de transferência
    bytes_total = bytes_enviados
    kb_total = bytes_total / 1024
    mb_total = kb_total / 1024
    
    taxa_bytes_por_segundo = bytes_total / tempo_total
    taxa_kb_por_segundo = kb_total / tempo_total
 
    taxa_bits_por_segundo = (bytes_total * 8) / tempo_total
    taxa_mbits_por_segundo = taxa_bits_por_segundo / (1024 * 1024)
    
    # Exibir métricas finais
    print("\n" + "=" * 50)
    print("ESTATÍSTICAS DE TRANSMISSÃO:")
    print(f"Tempo total: {tempo_total:.2f} segundos")
    print(f"Total de dados enviados: {bytes_total} bytes ({mb_total:.2f} MB)")
    print(f"Total de pacotes enviados: {pacotes_enviados}")
    print(f"Pacotes recebidos com sucesso: {pacotes_recebidos}")
    print(f"Pacotes perdidos: {pacotes_perdidos}")
    print(f"Taxa de perda de pacotes: {taxa_perda:.2f}%")
    print(f"Total de retransmissões: {total_retransmissoes}")
    print(f"Tempo médio de resposta: {tempo_medio:.2f}ms")
    print(f"Taxa de transferência: {taxa_bytes_por_segundo:.2f} B/s ({taxa_kb_por_segundo:.2f} KB/s)")
    print(f"Taxa de transmissão: {taxa_mbits_por_segundo:.2f} Mbps")
    print("=" * 50)

if __name__ == "__main__":
    enviar_pacotes_udp(servidor_host='127.0.0.1', servidor_porta=12345, num_pacotes=5, tamanho_pacote=60*1024, max_retransmissoes=3, timeout=5)
