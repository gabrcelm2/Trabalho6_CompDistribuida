import subprocess
import os
import csv
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

USER_LEVELS = [100, 250, 500]
DURATION = "50s" # 50 seconds per test as requested

BASE_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

# Definição dos testes: (nome, locustfile, host_java, host_python)
TESTS = [
    ("REST",    "locustfile_rest.py",    "http://localhost:8080", "http://localhost:8000"),
    ("GraphQL", "locustfile_graphql.py", "http://localhost:8080", "http://localhost:8000"),
    ("SOAP",    "locustfile_soap.py",    "http://localhost:8080", "http://localhost:8000"),
    ("gRPC",    "locustfile_grpc.py",    "localhost:9090",        "localhost:9091"),
]

def run_locust(protocol, locustfile, host, language, results_dir, users):
    spawn_rate = max(1, int(users * 0.2)) # Spawn rate 20%
    prefix = os.path.join(results_dir, f"{language}_{protocol}")
    locustfile_path = os.path.join(os.path.dirname(__file__), locustfile)

    cmd = [
        sys.executable, "-m", "locust",
        "-f", locustfile_path,
        "--host", host,
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", DURATION,
        "--headless",
        "--csv", prefix,
    ]

    print(f"[{users} Usuários] Rodando: {language.upper()} - {protocol}...")
    
    # Run synchronously
    subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))

    return prefix

def parse_stats(csv_path):
    stats_file = csv_path + "_stats.csv"
    if not os.path.exists(stats_file):
        return None

    with open(stats_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name') == 'Aggregated':
                val = row.get('95%', '0')
                if val == 'N/A':
                    return 0.0
                return float(val or 0)
    return 0.0

def generate_charts_for_level(level_results, users, results_dir):
    protocols = ["REST", "GraphQL", "SOAP", "gRPC"]
    java_avg = []
    python_avg = []

    for proto in protocols:
        j = level_results.get(f"java_{proto}", 0)
        p = level_results.get(f"python_{proto}", 0)
        java_avg.append(j)
        python_avg.append(p)

    x = np.arange(len(protocols))
    width = 0.35

    # 1. Gráfico Python (Apenas Python)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(protocols, python_avg, color='#E67E22')
    ax.set_ylabel('Tempo P95 (ms)')
    ax.set_title(f'Desempenho APIs em PYTHON ({users} Usuários)')
    ax.bar_label(bars, fmt='%.1f')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f'1_python_desempenho_{users}users.png'))
    plt.close()

    # 2. Gráfico Java (Apenas Java)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(protocols, java_avg, color='#4A90D9')
    ax.set_ylabel('Tempo P95 (ms)')
    ax.set_title(f'Desempenho APIs em JAVA ({users} Usuários)')
    ax.bar_label(bars, fmt='%.1f')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f'2_java_desempenho_{users}users.png'))
    plt.close()

    # 3. Gráfico Comparativo Agrupado
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, java_avg, width, label='Java', color='#4A90D9')
    bars2 = ax.bar(x + width/2, python_avg, width, label='Python', color='#E67E22')
    ax.set_ylabel('Tempo P95 (ms)')
    ax.set_title(f'Comparativo Java vs Python ({users} Usuários)')
    ax.set_xticks(x)
    ax.set_xticklabels(protocols)
    ax.legend()
    ax.bar_label(bars1, fmt='%.1f')
    ax.bar_label(bars2, fmt='%.1f')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f'3_comparativo_{users}users.png'))
    plt.close()

def main():
    print("=" * 60)
    print(" INICIANDO TESTES DE CARGA (100, 500, 800)")
    print("=" * 60)

    for users in USER_LEVELS:
        level_dir = os.path.join(BASE_RESULTS_DIR, f"{users}_users")
        os.makedirs(level_dir, exist_ok=True)
        level_results = {}

        for protocol, locustfile, host_java, host_python in TESTS:
            # Python
            prefix_py = run_locust(protocol, locustfile, host_python, "python", level_dir, users)
            level_results[f"python_{protocol}"] = parse_stats(prefix_py)

            # Java
            prefix_ja = run_locust(protocol, locustfile, host_java, "java", level_dir, users)
            level_results[f"java_{protocol}"] = parse_stats(prefix_ja)

        generate_charts_for_level(level_results, users, level_dir)
        print(f"-> Gráficos do cenário {users} usuários gerados com sucesso!\n")

    print("TODOS OS TESTES E GRÁFICOS CONCLUÍDOS!")

if __name__ == "__main__":
    main()
