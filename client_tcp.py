import socket
import time
import random
import string

def gerar_payload(tamanho):
    """Gera uma string aleatória com o tamanho especificado em bytes"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanho))

def enviar_pacotes_tcp(servidor_host, servidor_porta, num_pacotes, tamanho_pacote, timeout=30):
    # Inicializar a variável no início da função
    tempo_inicio_total = time.time()
    
    # Criar o socket TCP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.settimeout(timeout)  # Definir timeout aumentado para 30 segundos
    
    # Aumentar o buffer de envio
    cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**24)
    
    # Inicializar métricas
    pacotes_enviados = 0
    bytes_enviados = 0
    tempos_envio = []
    
    print(f"Iniciando envio de {num_pacotes} pacotes de {tamanho_pacote} bytes cada")
    print("-" * 50)
    
    try:
        # Conectar ao servidor
        print(f"Conectando a {servidor_host}:{servidor_porta}...")
        tempo_conexao_inicio = time.time()
        cliente_socket.connect((servidor_host, servidor_porta))
        tempo_conexao = (time.time() - tempo_conexao_inicio) * 1000
        print(f"Conectado em {tempo_conexao:.2f}ms")
        
        for i in range(num_pacotes):
            # Criar payload com número de sequência
            seq_prefix = f"{i:08d}-"
            # Gerar payload para o restante do tamanho do pacote
            payload_content = gerar_payload(tamanho_pacote - len(seq_prefix))
            # Combinar para formar o pacote completo
            payload = seq_prefix + payload_content
            
            # Garantir que o pacote tenha exatamente o tamanho especificado
            if len(payload) != tamanho_pacote:
                payload = payload[:tamanho_pacote]
            
            # Adicionar cabeçalho com o tamanho do pacote (8 bytes)
            payload_bytes = payload.encode('utf-8')
            tamanho_header = f"{len(payload_bytes):08d}".encode('utf-8')
            pacote_completo = tamanho_header + payload_bytes
            
            try:
                inicio = time.time()
                
                # Enviar dados para o servidor - garantir envio completo
                bytes_enviados_pacote = 0
                
                # Garantir que todo o pacote seja enviado
                while bytes_enviados_pacote < len(pacote_completo):
                    sent = cliente_socket.send(pacote_completo[bytes_enviados_pacote:])
                    if sent == 0:
                        raise RuntimeError("Conexão quebrada")
                    bytes_enviados_pacote += sent
                
                bytes_enviados += bytes_enviados_pacote
                pacotes_enviados += 1
                
                fim = time.time()
                tempo_envio = (fim - inicio)  # Converter para milissegundos
                tempos_envio.append(tempo_envio)
                
                print(f"Pacote {i+1}/{num_pacotes}: Enviado {bytes_enviados_pacote} bytes (payload: {len(payload_bytes)} bytes) em {tempo_envio:.2f}ms")
                
                # Pequena pausa entre pacotes para não sobrecarregar
                time.sleep(0.01)
                
            except socket.timeout:
                print(f"Pacote {i+1}/{num_pacotes}: Timeout! O servidor não respondeu em {timeout} segundos.")
                break
                
            except Exception as e:
                print(f"Pacote {i+1}/{num_pacotes}: Erro - {e}")
                break
        
        # Enviar pacote de finalização (tamanho 0)
        fim_header = "00000000".encode('utf-8')
        cliente_socket.send(fim_header)
        print("Enviado pacote de finalização")
        
        # Fechar a conexão 
        cliente_socket.shutdown(socket.SHUT_RDWR)
        
    except socket.timeout:
        print(f"Timeout ao tentar conectar ao servidor após {timeout} segundos.")
    
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    
    finally:
        # Fechar o socket
        try:
            cliente_socket.close()
        except:
            pass

    tempo_total = time.time() - tempo_inicio_total

    # Calcular estatísticas
    tempo_medio = sum(tempos_envio) / len(tempos_envio) if tempos_envio else 0
    # Calcular taxa de transferência
    bytes_total = bytes_enviados
    kb_total = bytes_total / 1024
    mb_total = kb_total / 1024

    print("\n" + "="*50)
    print("ESTATÍSTICAS DO CLIENTE:")
    print(f"Tempo total de envio: {tempo_total:.2f} segundos")
    print(f"Pacotes enviados: {pacotes_enviados}")
    print(f"Bytes enviados: {bytes_enviados} ({bytes_enviados/1024/1024:.2f} MB)")

    if tempo_total > 0:
        taxa_bps = bytes_enviados / tempo_total
        taxa_kbps = taxa_bps / 1024
        taxa_mbps = taxa_kbps / 1024
        print(f"Taxa média de envio: {taxa_bps:.2f} B/s ({taxa_kbps:.2f} KB/s, {taxa_mbps:.2f} MB/s)")
    
    # Métricas finais
    print("\n" + "=" * 50)
    print("ESTATÍSTICAS DE TRANSMISSÃO TCP:")
    print(f"Tempo total: {tempo_total:.2f} segundos")
    print(f"Total de dados enviados: {bytes_total} bytes ({mb_total:.2f} MB)")
    print(f"Total de pacotes enviados: {pacotes_enviados}")
    print(f"Tempo médio de envio: {tempo_medio:.2f}ms")
    print(f"Taxa de transferência: {taxa_bps:.2f} B/s ({taxa_kbps:.2f} KB/s)")
    print(f"Taxa de transmissão: {taxa_mbps:.2f} Mbps")
    print("=" * 50)

if __name__ == "__main__":
    enviar_pacotes_tcp(servidor_host='127.0.0.1', servidor_porta=12345, num_pacotes=5, tamanho_pacote=10*1024, timeout=10)