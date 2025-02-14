import re
import subprocess

# Caminho do repositório Git (hardcoded)
REPO_PATH = "C:/caminho/para/repositorio"

def get_sa_variables_from_commit(commit_hash):
    """
    Obtém todas as variáveis SA_ em arquivos .c, .h e .s a partir de um commit específico do Git.
    """
    file_pattern = r'.*\.(c|h|s)$'
    variable_pattern = r'\bSA_\w+'
    sa_variables = set()
    
    try:
        # Obtém a lista de arquivos no commit
        file_list = subprocess.check_output(["git", "-C", REPO_PATH, "ls-tree", "-r", "--name-only", commit_hash], text=True).splitlines()
        
        for file in file_list:
            if re.match(file_pattern, file):
                try:
                    file_content = subprocess.check_output(["git", "-C", REPO_PATH, "show", f"{commit_hash}:{file}"], text=True, errors='ignore')
                    sa_variables.update(re.findall(variable_pattern, file_content))
                except subprocess.CalledProcessError:
                    pass  # Se o arquivo não existir no commit, ignora
    except subprocess.CalledProcessError as e:
        print(f"Erro ao acessar o repositório Git: {e}")
        return set()
    
    return sa_variables

def main():
    start_commit = input("Digite o hash do commit inicial: ").strip()
    end_commit = input("Digite o hash do commit final: ").strip()
    
    sa_vars_start = get_sa_variables_from_commit(start_commit)
    sa_vars_end = get_sa_variables_from_commit(end_commit)
    
    print("Variáveis SA no commit inicial:")
    print("\n".join(sorted(sa_vars_start)))
    
    print("\nVariáveis SA no commit final:")
    print("\n".join(sorted(sa_vars_end)))
    
    added_vars = sa_vars_end - sa_vars_start
    removed_vars = sa_vars_start - sa_vars_end
    
    if added_vars:
        print("\nVariáveis SA adicionadas no intervalo de commits:")
        print("\n".join(sorted(added_vars)))
    else:
        print("\nNenhuma variável SA foi adicionada.")
    
    if removed_vars:
        print("\nVariáveis SA removidas no intervalo de commits:")
        print("\n".join(sorted(removed_vars)))
    else:
        print("\nNenhuma variável SA foi removida.")

if __name__ == "__main__":
    main()
