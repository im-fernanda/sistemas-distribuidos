import socket
import time
import sys

def iniciar_servidor(servidor_host='', servidor_porta=12345, timeout_inativo=10):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # reutilização do endereço/porta
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Aumenta o buffer de recepção para evitar perdas
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**24)
    
    try:
        servidor_socket.bind((servidor_host, servidor_porta))
        
        
        servidor_socket.listen(5)
        print(f"Servidor TCP iniciado em {servidor_host if servidor_host else '0.0.0.0'}:{servidor_porta}")
        print(f"Aguardando conexão... (O servidor fechará após {timeout_inativo} segundos de inatividade)")
        
        # timeout para aceitar conexões
        servidor_socket.settimeout(timeout_inativo)
        
        # contadores globais
        total_pacotes_recebidos = 0
        total_bytes_recebidos = 0
        tempo_inicio_global = time.time()
        
        try:
            # Aceitar conexão
            cliente_socket, endereco = servidor_socket.accept()
            print(f"Conexão estabelecida com {endereco}")
            
            # Inicializa contadores 
            pacotes_recebidos = 0
            bytes_recebidos = 0
            tempo_inicio = time.time()
            ultima_atividade = time.time()
            
            # Configura timeout para o socket do cliente
            cliente_socket.settimeout(timeout_inativo)
            
            while True:
                try:
                    # Recebe o cabeçalho com o tamanho (8 bytes)
                    header = b""
                    while len(header) < 8:
                        chunk = cliente_socket.recv(8 - len(header))
                        if not chunk:
                            print("Cliente encerrou a conexão durante a leitura do cabeçalho.")
                            break
                        header += chunk
                    
                    if not header:
                        print("Cliente encerrou a conexão normalmente.")
                        break
                    
                    # Converte o cabeçalho para obter o tamanho do pacote
                    try:
                        tamanho_pacote = int(header.decode('utf-8'))
                    except ValueError:
                        print(f"Cabeçalho inválido recebido: {header}")
                        break
                    
                    # Se o tamanho for 0, é um pacote de finalização
                    if tamanho_pacote == 0:
                        print("Recebido pacote de finalização. Encerrando conexão.")
                        break
                    
                    # Recebe o pacote completo
                    dados = b""
                    while len(dados) < tamanho_pacote:
                        chunk = cliente_socket.recv(min(65535, tamanho_pacote - len(dados)))
                        if not chunk:
                            print(f"Cliente encerrou a conexão durante a leitura do pacote. Recebidos {len(dados)}/{tamanho_pacote} bytes.")
                            break
                        dados += chunk
                    
                    if len(dados) < tamanho_pacote:
                        print("Pacote incompleto recebido. Encerrando conexão.")
                        break
                    
                
                    pacotes_recebidos += 1
                    total_pacotes_recebidos += 1
                    bytes_recebidos += len(dados)
                    total_bytes_recebidos += len(dados)
                    ultima_atividade = time.time()
                    
                    # Processando os dados recebidos
                    try:
                        mensagem = dados.decode('utf-8')
                        seq_num = mensagem.split('-')[0] if '-' in mensagem else 'N/A'
                        
                        # Exibir informações para cada pacote
                        print(f"Pacote #{pacotes_recebidos} (Seq: {seq_num}) de {endereco}: {len(dados)} bytes")
                        
                        if pacotes_recebidos % 10 == 0:  # Mostra estatísticas a cada 10 pacotes
                            tempo_atual = time.time()
                            tempo_decorrido = tempo_atual - tempo_inicio
                            taxa_bytes_por_segundo = bytes_recebidos / tempo_decorrido if tempo_decorrido > 0 else 0
                            taxa_kb_por_segundo = taxa_bytes_por_segundo / 1024
                            
                            print(f"Taxa média desta conexão: {taxa_bytes_por_segundo:.2f} B/s ({taxa_kb_por_segundo:.2f} KB/s)")
                    
                    except UnicodeDecodeError:
                        print(f"Recebido pacote binário de {endereco}: {len(dados)} bytes")
                    
                except socket.timeout:
                    tempo_inativo = time.time() - ultima_atividade
                    print(f"Nenhuma atividade por {tempo_inativo:.2f} segundos. Encerrando servidor.")
                    break
                
                except ConnectionResetError:
                    print(f"Conexão resetada por {endereco}")
                    break
                
                except Exception as e:
                    print(f"Erro na conexão com {endereco}: {e}")
                    break
            
            
            tempo_conexao = time.time() - tempo_inicio
            print(f"\nConexão com {endereco} encerrada")
            print(f"Tempo de conexão: {tempo_conexao:.2f} segundos")
            print(f"Pacotes recebidos: {pacotes_recebidos}")
            print(f"Bytes recebidos: {bytes_recebidos} ({bytes_recebidos/1024/1024:.2f} MB)")
            
            if tempo_conexao > 0:
                taxa_bytes_por_segundo = bytes_recebidos / tempo_conexao
                taxa_kb_por_segundo = taxa_bytes_por_segundo / 1024
                taxa_mb_por_segundo = taxa_kb_por_segundo / 1024
                print(f"Taxa média: {taxa_bytes_por_segundo:.2f} B/s ({taxa_kb_por_segundo:.2f} KB/s, {taxa_mb_por_segundo:.2f} MB/s)")
            
        except socket.timeout:
            print("Timeout ao aguardar conexão. Encerrando servidor.")
        
        finally:
            # Fechar o socket do cliente se estiver aberto
            try:
                cliente_socket.close()
            except:
                pass
        
        # Exibir estatísticas globais
        tempo_total = time.time() - tempo_inicio_global
        print("\n" + "=" * 50)
        print("ESTATÍSTICAS GLOBAIS DO SERVIDOR:")
        print(f"Tempo de execução: {tempo_total:.2f} segundos")
        print(f"Total de pacotes recebidos: {total_pacotes_recebidos}")
        print(f"Total de bytes recebidos: {total_bytes_recebidos} ({total_bytes_recebidos/1024/1024:.2f} MB)")
        
        if tempo_total > 0:
            taxa_bytes_por_segundo = total_bytes_recebidos / tempo_total
            taxa_kb_por_segundo = taxa_bytes_por_segundo / 1024
            taxa_mb_por_segundo = taxa_kb_por_segundo/ 1024
            taxa_mbps = (total_bytes_recebidos * 8) / tempo_total / 1024 / 1024
            
            print(f"Taxa média de transferência: {taxa_bytes_por_segundo:.2f} B/s ({taxa_kb_por_segundo:.2f} KB/s, {taxa_mb_por_segundo:.2f} MB/s)")
            print(f"Taxa de transmissão: {taxa_mbps:.2f} Mbps")
        
        print("=" * 50)
    
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    
    except Exception as e:
        print(f"Erro no servidor: {e}")
    
    finally:
        # Fechar o socket do servidor
        servidor_socket.close()
        print("Servidor encerrado.")

if __name__ == "__main__":

    iniciar_servidor(servidor_host='', servidor_porta=12345, timeout_inativo=10)
