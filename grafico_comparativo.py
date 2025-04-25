import matplotlib.pyplot as plt

# Dados fornecidos
packet_sizes_kb = [1, 10, 20, 30, 40, 50, 60]
tcp_mbps = [0.75, 7.39, 14.79, 22.16, 29.90, 37.02, 44.73]
udp_mbps = [0.71, 7.26, 14.00, 21.12, 28.50, 35.67, 41.88]

# Plot do gráfico
plt.figure(figsize=(10, 6))
plt.plot(packet_sizes_kb, tcp_mbps, marker='o', label='TCP', color='blue')
plt.plot(packet_sizes_kb, udp_mbps, marker='s', label='UDP', color='green')

plt.title('Taxa de Transmissão vs Tamanho do Pacote (5 Pacotes)')
plt.xlabel('Tamanho do Pacote (KB)')
plt.ylabel('Taxa de Transmissão (Mbps)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
