import shutil
import os

# Caminho do arquivo de origem (hardcoded)
origem = "/caminho/para/origem/arquivo.txt"
# Caminho do destino (hardcoded) com novo nome
destino = "/caminho/para/destino/novo_nome.txt"

# Verifica se o arquivo de destino já existe e remove se necessário
if os.path.exists(destino):
    os.remove(destino)
    print(f"Arquivo existente {destino} removido.")

# Copia o arquivo renomeando para o destino
shutil.copy2(origem, destino)
print(f"Arquivo copiado de {origem} para {destino}.")