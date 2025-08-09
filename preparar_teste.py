import os
import shutil
import subprocess

# Caminho do arquivo e pasta
arquivo = "app/messages.db"
pasta = "migrations"

# Excluir arquivo
if os.path.exists(arquivo):
    os.remove(arquivo)
    print(f"Arquivo '{arquivo}' excluído.")
else:
    print(f"Arquivo '{arquivo}' não encontrado.")

# Excluir pasta
if os.path.exists(pasta):
    shutil.rmtree(pasta)
    print(f"Pasta '{pasta}' excluída.")
else:
    print(f"Pasta '{pasta}' não encontrada.")

# Rodar comandos do Flask-Migrate
comandos = [
    ["flask", "db", "init"],
    ["flask", "db", "migrate", "-m", "criando db"],
    ["flask", "db", "upgrade"]
]

for cmd in comandos:
    print(f"\nRodando comando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)