import re
from collections import defaultdict

def filter_diff(diff_text):

    file_pattern = r'^\+\+\+\s+b/(.+)$'
    line_pattern = r'^[+-]\s*(\w+\s+)?(ICD_DATA\s+)?SA_\w+'

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

    additions = defaultdict(int)
    removals = defaultdict(int)
    final_state = defaultdict(str)

    for file, lines in changes.items():
        for line in lines:
            normalized = normalize_variable(line[1:].strip())
            if line.startswith("+"):
                additions[normalized] += 1
                final_state[normalized] = '+'  # Variable present in the final state
            elif line.startswith("-"):
                removals[normalized] += 1
                final_state[normalized] = '-'  # Variable potentially removed

    # Filter variables that remain in the code
    result = []
    result.append("Resumo de mudanças por variável:")

    for variable in set(additions.keys()).union(removals.keys()):
        added_count = additions[variable]
        removed_count = removals[variable]
        final_marker = "Presente" if final_state[variable] == '+' else "Removida"
        result.append(f"Variável: {variable}, Adicionada: {added_count} vezes, Removida: {removed_count} vezes, Estado final: {final_marker}")

    return "\n".join(result)

def main():
    diff_file = "C:\\GIT\\MEC\\ldra\\PlatformSoftware\\develop.diff"
    try:
        with open(diff_file, "r") as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{diff_file}' não encontrado.")
        return

    result = filter_diff(diff_content)

    # Exibe o resultado
    print("Linhas filtradas:")
    print(result)

if __name__ == "__main__":
    main()
