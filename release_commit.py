import re
import subprocess
from collections import defaultdict

def get_sa_variables_from_git(commit_hash):
    """
    Obtém todas as variáveis SA_ em arquivos .c, .h e .s a partir de um commit específico do Git.
    """
    file_pattern = r'.*\.(c|h|s)$'
    variable_pattern = r'\bSA_\w+'
    
    sa_variables = set()
    
    try:
        # Obtém a lista de arquivos no commit
        file_list = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", commit_hash], text=True).splitlines()
        
        for file in file_list:
            if re.match(file_pattern, file):
                file_content = subprocess.check_output(["git", "show", f"{commit_hash}:{file}"], text=True)
                sa_variables.update(re.findall(variable_pattern, file_content))
    except subprocess.CalledProcessError as e:
        print(f"Erro ao acessar o repositório Git: {e}")
        return set()
    
    return sa_variables

def main():
    commit_hash1 = input("Digite o primeiro hash do commit: ").strip()
    sa_vars_1 = get_sa_variables_from_git(commit_hash1)
    print("Variáveis SA encontradas no primeiro commit:")
    print("\n".join(sorted(sa_vars_1)))
    
    commit_hash2 = input("Digite o segundo hash do commit: ").strip()
    sa_vars_2 = get_sa_variables_from_git(commit_hash2)
    print("Variáveis SA encontradas no segundo commit:")
    print("\n".join(sorted(sa_vars_2)))
    
    added_vars = sa_vars_2 - sa_vars_1
    removed_vars = sa_vars_1 - sa_vars_2
    
    if added_vars:
        print("\nVariáveis SA adicionadas no segundo commit:")
        print("\n".join(sorted(added_vars)))
    else:
        print("\nNenhuma variável SA foi adicionada.")
    
    if removed_vars:
        print("\nVariáveis SA removidas no segundo commit:")
        print("\n".join(sorted(removed_vars)))
    else:
        print("\nNenhuma variável SA foi removida.")

if __name__ == "__main__":
    main()
