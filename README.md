<h1 align="center" style="font-weight: bold;">  Sistemas Distribuídos - Comunicação TCP vs UDP <h1>

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

## 📊 Relatório Técnico

O arquivo `Relatório.pdf` apresenta uma análise comparativa entre os protocolos TCP e UDP sob duas condições:

- **Sem perda nem atraso (condições ideais)**:
  - TCP e UDP apresentam desempenho semelhante, com o TCP superando ligeiramente para pacotes maiores.
  - O gráfico mostra crescimento linear da taxa de transferência com o aumento do tamanho dos pacotes.

- **Com perda e atraso simulados via Clumsy (1000ms de latência e 10% de perda)**:
  - O desempenho do UDP é severamente impactado, quase nulo para pacotes pequenos.
  - O TCP mantém desempenho crescente, demonstrando maior robustez mesmo sob condições adversas.

> A conclusão do relatório reforça que a escolha entre TCP e UDP depende das características da aplicação e das condições da rede.

