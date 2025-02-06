import shutil
import os

# Definição das pastas e nomes hardcoded
pastas_origem = ["C:/caminho/para/pasta1", "C:/caminho/para/pasta2"]  # Altere para os caminhos corretos
destino = "C:/caminho/para/pasta_destino"  # Altere para o caminho correto
arquivos_renomeados = {
    "arquivo_original1.txt": "arquivo1_novo.txt",
    "arquivo_original2.txt": "arquivo2_novo.txt",
    "arquivo_original3.txt": "arquivo3_novo.txt"
}

# Garante que a pasta de destino existe
os.makedirs(destino, exist_ok=True)

# Percorre as pastas de origem
for pasta in pastas_origem:
    if not os.path.exists(pasta):
        continue  # Pula pastas que não existem
    
    # Lista os arquivos na pasta de origem
    arquivos = os.listdir(pasta)
    
    # Move e renomeia os arquivos especificados
    for arquivo_original, novo_nome in arquivos_renomeados.items():
        if arquivo_original in arquivos:
            caminho_origem = os.path.join(pasta, arquivo_original)
            caminho_destino = os.path.join(destino, novo_nome)
            shutil.move(caminho_origem, caminho_destino)
            print(f"Movido {arquivo_original} para {caminho_destino}")

print("Processo concluído!")