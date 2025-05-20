#!/usr/bin/env python3
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime
import os  # Importa o módulo os para manipulação de arquivos e diretórios

# Define o diretório onde os gráficos serão salvos
OUTPUT_DIR = "script/results"

def ensure_output_directory():
    """Garante que o diretório de saída exista."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def simulate_convergence_time():
    """Simula o tempo de convergência conforme número de falhas"""
    print("Simulando tempos de convergência...")

    # Dados simulados (substitua por dados reais se possível)
    failures = [1, 2, 3, 4, 5]
    convergence_times = [2.1, 3.8, 6.2, 8.5, 11.3]  # Em segundos

    plt.figure(figsize=(10, 6))
    plt.plot(failures, convergence_times, 'bo-', linewidth=2, markersize=8)
    plt.title("Tempo de Convergência vs Número de Falhas", fontsize=14)
    plt.xlabel("Número de Roteadores com Falha Simultânea", fontsize=12)
    plt.ylabel("Tempo de Convergência (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    filename = os.path.join(OUTPUT_DIR, "convergence_time.png")
    plt.savefig(filename)
    print(f"Gráfico de convergência salvo em {filename}")

def simulate_lsa_throughput():
    """Testa a capacidade de processamento de LSAs"""
    print("Testando throughput de LSAs...")

    # Valores simulados (substitua por testes reais)
    lsa_counts = [10, 50, 100, 150, 200]
    processing_times = [0.5, 2.1, 4.8, 8.3, 15.2]  # Tempo para processar

    throughput = [count/time for count, time in zip(lsa_counts, processing_times)]

    plt.figure(figsize=(10, 6))
    plt.bar([str(x) for x in lsa_counts], throughput, color='orange')
    plt.title("Throughput de Processamento de LSAs", fontsize=14)
    plt.xlabel("Número de LSAs Enviados", fontsize=12)
    plt.ylabel("LSAs Processados por Segundo", fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    filename = os.path.join(OUTPUT_DIR, "lsa_throughput.png")
    plt.savefig(filename)
    print(f"Gráfico de throughput salvo em {filename}")

def simulate_resource_usage():
    """Simula o uso de CPU/memória sob carga"""
    print("Simulando uso de recursos...")

    time_points = range(0, 300, 30)  # 5 minutos de teste
    cpu_usage = [random.uniform(10, 80) for _ in time_points]
    mem_usage = [random.uniform(200, 700) for _ in time_points]  # Em MB

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:red'
    ax1.set_xlabel('Tempo (segundos)', fontsize=12)
    ax1.set_ylabel('Uso de CPU (%)', color=color, fontsize=12)
    ax1.plot(time_points, cpu_usage, color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Uso de Memória (MB)', color=color, fontsize=12)
    ax2.plot(time_points, mem_usage, color=color, marker='s')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Uso de Recursos sob Carga (Simulado)", fontsize=14)
    fig.tight_layout()
    filename = os.path.join(OUTPUT_DIR, "resource_usage.png")
    plt.savefig(filename)
    print(f"Gráfico de recursos salvo em {filename}")

if __name__ == "__main__":
    print(f"\n🚀 Iniciando testes de performance em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    ensure_output_directory()
    simulate_convergence_time()
    simulate_lsa_throughput()
    simulate_resource_usage()

    print("\n📊 Resultados dos testes:")
    print(f"1. {os.path.join(OUTPUT_DIR, 'convergence_time.png')} - Tempo para rede se estabilizar após falhas")
    print(f"2. {os.path.join(OUTPUT_DIR, 'lsa_throughput.png')} - Capacidade de processamento de pacotes")
    print(f"3. {os.path.join(OUTPUT_DIR, 'resource_usage.png')} - Consumo de CPU/memória sob carga")
    print("\n⚠️ Para dados reais, substitua as funções de simulação por monitoramento real dos containers")