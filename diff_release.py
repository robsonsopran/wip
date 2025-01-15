import re
from collections import defaultdict

def filter_diff (diff_text):

    file_pattern = r'^\+\+\+\s+b/(.+)$'
    line_pattern = r'^[+]\s*(\w+\s+)?(ICD_DATA\s+)?SA_\w+'
    
    changes = defaultdict(list)
    current_file = None
    
    for line in diff_text.splitlines():
        file_match = re.match(file_pattern, line)
        if file_match:
            current_file = file_match.group(1)
        elif current_file and re.match(line_pattern, line):
            changes[current_file].append(line)
    
    def normalize_variable(line):
        return re.sub(r'(\w+\s+)?(ICD_DATA\s+)?(SA_\w+)', r'\3', line)
    
    additions = defaultdict(set)
    removals = defaultdict(set)

    for file, lines in changes.items():
        for line in lines:
            normalized = normalize_variable(line[1:].strip())
            if line.startswith("+"):
                additions[file].add(normalized)
            elif line.startswith("-"):
                removals[file].add(normalized)

    filtered_changes = defaultdict(list)

    for file, removed_lines in removals.items():
        for line in removed_lines:
            if not any (line in added_lines for added_lines in additions.values()):
                filtered_changes[file].append("- " + line)

    for file, added_lines in additions.items():
        for line in added_lines:
            if not any(line in removed_lines for removed_lines in removals.values()):
                filtered_changes[file].append("+ " + line)

    result = []
    for file, lines in filtered_changes.items():
        result.append(f"Arquivo: {file}")
        result.extend(lines)
    
    return "\n".join(result)

def process_diff_output(filtered_diff):
    lines = filtered_diff.splitlines()
    file_changes = defaultdict(list)
    
    current_file = None
    temp_changes = defaultdict(list)

    # Organizar as linhas por arquivo
    for line in lines:
        if line.startswith("Arquivo:"):
            current_file = line.split(":")[1].strip()
        else:
            temp_changes[current_file].append(line)
    
    # Processar as alterações de cada arquivo
    for file, lines in temp_changes.items():
        variable_count = defaultdict(int)  # Contagem de variáveis
        line_count = defaultdict(list)  # Armazena as linhas associadas a cada variável
        
        for line in lines:
            var = line[2:].strip()  # Retira o "+" ou "-" e pega a variável
            line_count[var].append(line)
            if line.startswith("+"):
                variable_count[var] += 1
            elif line.startswith("-"):
                variable_count[var] -= 1
        
        # Filtrar as linhas baseadas na contagem das variáveis
        for var, count in variable_count.items():
            if abs(count) % 2 == 1:  # Se a soma for ímpar
                # Se a contagem for positiva, mantém a última adição, caso contrário, a última remoção
                if count > 0:
                    file_changes[file].append(line_count[var][-1])
                else:
                    file_changes[file].append(line_count[var][0])
    
    # Montar a saída no formato esperado
    result = []
    for file, lines in file_changes.items():
        result.append(f"Arquivo: {file}")
        result.extend(lines)
    
    return "\n".join(result)

def main():
    diff_file = "C:\\GIT\\MEC\\ldra\\PlatformSoftware\\develop.diff

    try:
        with open (diff_file, "r") as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{diff_file}' não encontrado.")
        return
    
    result = filter_diff(diff_content)
    filtered_result = process_diff_output(result)
    
    # Exibe o resultado
    print("Linhas filtradas:")
    #print(result)
    print(filtered_result)

if __name__ == "__main__":
    main()
