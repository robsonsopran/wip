import subprocess
import sys
import os

# Configurações fixas
REPO_PATH = "/caminho/para/o/repositorio"  # Defina o caminho do repositório Git
BRANCH_LOCAL_MERGE = "1merg"  # Branch local para merge
BRANCH_LOCAL_COMP = "2comp"  # Branch local para comparação
BRANCH_TEMP = "temp"  # Nome do branch temporário
LISTA_ARQUIVOS_TXT = "lista_arquivos.txt"  # Nome do arquivo que contém a lista de arquivos a commitar

def executar_comando(comando):
    """Executa um comando no shell e retorna a saída."""
    try:
        resultado = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True, cwd=REPO_PATH)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar '{comando}': {e.stderr}")
        sys.exit(1)

def apagar_branch_temporario():
    """Apaga o branch temporário, se existir."""
    executar_comando(f"git branch -D {BRANCH_TEMP}")

def criar_branch_temporario():
    """Cria o branch temporário a partir do branch de comparação."""
    executar_comando(f"git checkout {BRANCH_LOCAL_COMP}")
    executar_comando(f"git checkout -b {BRANCH_TEMP}")

def fazer_merge():
    """Faz o merge do branch de merge no branch temporário."""
    executar_comando(f"git checkout {BRANCH_TEMP}")
    resultado_merge = executar_comando(f"git merge {BRANCH_LOCAL_MERGE}")

    if "CONFLICT" in resultado_merge:
        print("⚠️  Merge com conflitos! Resolva antes de continuar.")
        sys.exit(1)

    print("✅ Merge concluído sem conflitos.")

def extrair_nomes_arquivos(caminhos):
    """Remove os paths, mantendo apenas os nomes dos arquivos."""
    return {os.path.basename(arquivo) for arquivo in caminhos}

def commitar_apenas_arquivos_da_lista():
    """Commita apenas os arquivos da lista no branch temporário."""
    with open(os.path.join(REPO_PATH, LISTA_ARQUIVOS_TXT), "r", encoding="utf-8") as f:
        arquivos_permitidos = {linha.strip() for linha in f.readlines() if linha.strip()}

    # Obtém os arquivos modificados no staging
    arquivos_modificados = executar_comando("git diff --name-only --cached").split("\n")
    
    # Remove os paths e compara apenas pelo nome do arquivo
    arquivos_modificados_nomes = extrair_nomes_arquivos(arquivos_modificados)

    # Filtra os arquivos que devem ser commitados
    arquivos_a_commitar = [arquivo for arquivo in arquivos_modificados if os.path.basename(arquivo) in arquivos_permitidos]

    if not arquivos_a_commitar:
        print("❌ Nenhum arquivo da lista foi modificado. Nada a commitar.")
        return

    # Adiciona apenas os arquivos da lista ao commit
    executar_comando(f"git add {' '.join(arquivos_a_commitar)}")
    executar_comando(f'git commit -m "Merge dos arquivos específicos no branch temporário {BRANCH_TEMP}"')

    print("✅ Commit realizado apenas para os arquivos da lista.")

def main():
    apagar_branch_temporario()
    criar_branch_temporario()
    fazer_merge()
    commitar_apenas_arquivos_da_lista()
    print("🚀 Processo finalizado!")

if __name__ == "__main__":
    main()
