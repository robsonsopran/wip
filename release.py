import re
from collections import defaultdict

def process_diff(diff_text):
    """
    Processa o texto de um diff para identificar alterações relevantes
    em variáveis SA_ e retorna as diferenças filtradas.
    """
    file_pattern = r'^\+\+\+\s+b/(.+)$'
    line_pattern = r'^[+-]\s*(?!SA_)(\w+\s+)?(ICD_DATA\s+)?SA_\w+'

    changes = defaultdict(list)
    current_file = None

    for line in diff_text.splitlines():
        file_match = re.match(file_pattern, line)
        if file_match:
            current_file = file_match.group(1)
        elif current_file and re.match(line_pattern, line):
            changes[current_file].append(line)

    def normalize_variable(line):
        """Normaliza a variável removendo prefixos irrelevantes."""
        return re.sub(r'(\w+\s+)?(ICD_DATA\s+)?(SA_\w+)', r'\1\3', line)

    variable_changes = defaultdict(lambda: defaultdict(set))

    for file, lines in changes.items():
        for line in lines:
            normalized = normalize_variable(line[1:].strip())
            if line.startswith("+"):
                variable_changes[file]['added'].add(normalized)
            elif line.startswith("-"):
                variable_changes[file]['removed'].add(normalized)

    filtered_changes = []

    for file, data in variable_changes.items():
        unique_additions = data['added'] - data['removed']
        unique_removals = data['removed'] - data['added']

        for line in unique_additions:
            filtered_changes.append(f"+ {line}")
        for line in unique_removals:
            filtered_changes.append(f"- {line}")

    # Consolidar e filtrar ocorrências únicas
    variable_count = defaultdict(int)
    for line in filtered_changes:
        var = line[2:].strip().split('=')[0].split(';')[0].strip()
        variable_count[var] += 1

    final_result = [line for line in filtered_changes if variable_count[line[2:].strip().split('=')[0].split(';')[0].strip()] == 1]

    return "\n".join(final_result)

def main():
    diff_file = "C:\\GIT\\MEC\\ldra\\PlatformSoftware\\2_0_1to2_0.diff"

    try:
        with open(diff_file, "r") as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{diff_file}' não encontrado.")
        return

    result = process_diff(diff_content)
    print("Variáveis de SA únicas:")
    print(result)

if __name__ == "__main__":
    main()
