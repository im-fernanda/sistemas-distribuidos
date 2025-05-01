# Sistemas Distribuídos - Comunicação TCP vs UDP

Este repositório contém uma implementação de um sistema cliente-servidor utilizando os protocolos TCP e UDP, com o objetivo de comparar o desempenho entre eles.

## 📁 Estrutura do Projeto

- `client_tcp.py`: Cliente que se comunica com o servidor via protocolo TCP.
- `client_udp.py`: Cliente que se comunica com o servidor via protocolo UDP e tenta retransmissão em caso de falha.
- `server_tcp.py`: Servidor que aceita conexões de clientes via protocolo TCP.
- `server_udp.py`: Servidor que aceita conexões de clientes via protocolo UDP.
- `grafico_comparativo.py`: Script para gerar gráficos comparativos de desempenho entre TCP e UDP.
- `grafico_mbps.jpg`: Imagem gerada pelo script de comparação, ilustrando a taxa de transferência em Mbps.

## 🚀 Como Executar

### Requisitos

- Python 3.x instalado no sistema.

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/im-fernanda/sistemas-distribuidos.git
   cd sistemas-distribuidos

2. Execute o servidor desejado:
   - Para TCP:
   ```bash
     python server_tcp.py
   
  - Para UDP:
   ```bash
     python server_udppy
   ```

3. Em outro terminal, execute o cliente correspondente.

### 📊 Resultados
O gráfico gerado (grafico_mbps.jpg) apresenta uma comparação da taxa de transferência entre os protocolos TCP e UDP, permitindo analisar qual protocolo oferece melhor desempenho nas condições testadas.


