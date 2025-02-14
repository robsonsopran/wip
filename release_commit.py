import re
import subprocess

# Caminho do repositório Git (hardcoded)
REPO_PATH = "C:/dir1/dir2"

def get_changed_files(start_commit, end_commit):
    """
    Obtém a lista de arquivos que foram modificados entre dois commits.
    Filtra apenas arquivos .c, .h e .s.
    """
    try:
        changed_files = subprocess.check_output(
            ["git", "-C", REPO_PATH, "diff", "--name-only", start_commit, end_commit], text=True
        ).splitlines()
        
        # Filtrar apenas arquivos .c, .h, .s
        file_pattern = re.compile(r'.*\.(c|h|s)$')
        filtered_files = [file for file in changed_files if file_pattern.match(file)]
        
        print("Arquivos modificados entre os commits:")
        for f in filtered_files:
            print(f"- {f}")
        
        return filtered_files
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter arquivos modificados: {e}")
        return []

def get_sa_variables_from_commit(commit_hash, files):
    """
    Obtém todas as variáveis SA_ em arquivos .c, .h e .s a partir de um commit específico,
    considerando apenas os arquivos que foram modificados.
    """
    variable_pattern = r'\bSA_\w+'
    sa_variables = set()
    
    for file in files:
        try:
            file_content = subprocess.check_output(
                ["git", "-C", REPO_PATH, "show", f"{commit_hash}:./{file}"], text=True, errors='ignore'
            )
            sa_variables.update(re.findall(variable_pattern, file_content))
        except subprocess.CalledProcessError:
            print(f"Erro ao acessar o arquivo {file} no commit {commit_hash}, ignorando...")
    
    return sa_variables

def main():
    start_commit = input("Digite o hash do commit inicial: ").strip()
    end_commit = input("Digite o hash do commit final: ").strip()
    
    # Obter apenas os arquivos modificados
    changed_files = get_changed_files(start_commit, end_commit)

    if not changed_files:
        print("Nenhum arquivo .c, .h ou .s foi modificado entre os commits.")
        return
    
    sa_vars_start = get_sa_variables_from_commit(start_commit, changed_files)
    sa_vars_end = get_sa_variables_from_commit(end_commit, changed_files)
    
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

