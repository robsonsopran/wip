import shutil
import os

# Definição das pastas e nomes hardcoded
origem = "C:/caminho/para/pasta_origem"  # Altere para o caminho correto
 destino = "C:/caminho/para/pasta_destino"  # Altere para o caminho correto
novos_nomes = ["arquivo1_novo.txt", "arquivo2_novo.txt", "arquivo3_novo.txt"]

# Garante que a pasta de destino existe
os.makedirs(destino, exist_ok=True)

# Lista os arquivos na pasta de origem
arquivos = os.listdir(origem)

# Filtra apenas os três primeiros arquivos
arquivos_para_mover = arquivos[:3]

# Move e renomeia os arquivos
for i, arquivo in enumerate(arquivos_para_mover):
    caminho_origem = os.path.join(origem, arquivo)
    caminho_destino = os.path.join(destino, novos_nomes[i])
    shutil.move(caminho_origem, caminho_destino)
    print(f"Movido {arquivo} para {caminho_destino}")

print("Processo concluído!")
