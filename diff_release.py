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

    variable_counts = defaultdict(lambda: defaultdict(int))

    for file, lines in changes.items():
        for line in lines:
            normalized = normalize_variable(line[1:].strip())
            if line.startswith("+"):
                variable_counts[file][normalized] += 1
            elif line.startswith("-"):
                variable_counts[file][normalized] -= 1

    filtered_changes = defaultdict(list)

    for file, counts in variable_counts.items():
        for variable, count in counts.items():
            if count % 2 != 0:  # Mantém apenas se o total for ímpar
                state = "+" if count > 0 else "-"
                filtered_changes[file].append(f"{state} {variable}")

    result = []
    for file, lines in filtered_changes.items():
        result.append(f"Arquivo: {file}")
        result.extend(lines)
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
