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

def process_diff(result_text):
    """
    Processa o resultado do diff para filtrar as variáveis com base no critério especificado.

    - Remove variáveis cuja soma de adições e remoções é par.
    - Retém apenas a última linha de variáveis cuja soma é ímpar.

    :param result_text: O texto de saída das mudanças filtradas.
    :return: Texto com o processamento final aplicado.
    """
    # Filtra as linhas relevantes que indicam mudanças em variáveis
    diff_lines = [line.strip() for line in result_text.splitlines() if line.startswith("+") or line.startswith("-")]

    # Agrupa as mudanças por variável
    variable_changes = defaultdict(list)
    for line in diff_lines:
        variable = line[1:].strip()  # Remove o prefixo (+/-)
        variable_changes[variable].append(line)

    processed_lines = []

    for variable, changes in variable_changes.items():
        added_count = sum(1 for change in changes if change.startswith("+"))
        removed_count = sum(1 for change in changes if change.startswith("-"))

        if (added_count + removed_count) % 2 == 0:
            # Soma par: remover todas as ocorrências dessa variável
            continue

        # Soma ímpar: manter apenas a última linha da maior categoria
        last_addition = next((line for line in reversed(changes) if line.startswith("+")), None)
        last_removal = next((line for line in reversed(changes) if line.startswith("-")), None)

        if added_count > removed_count and last_addition:
            processed_lines.append(last_addition)
        elif removed_count > added_count and last_removal:
            processed_lines.append(last_removal)

    return "\n".join(processed_lines)

def main():
    diff_file = "C:\\GIT\\MEC\\ldra\\PlatformSoftware\\develop.diff"
    try:
        with open(diff_file, "r") as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{diff_file}' não encontrado.")
        return

    # Obter o resumo do diff
    result = filter_diff(diff_content)

    # Processar o resultado para obter o resultado final
    final_result = process_diff(result)

    # Exibir o resultado processado
    print("Linhas processadas:")
    print(final_result)

if __name__ == "__main__":
    main()
