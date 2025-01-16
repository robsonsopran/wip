import re
from collections import defaultdict

def filter_diff(diff_text):

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
        return re.sub(r'(\w+\s+)?(ICD_DATA\s+)?(SA_\w+)', r'\1\3', line)

    additions defaultdict(set)
    removals defaultdict(set)

    for file, lines in changes.items():
        for line in lines:
            normalized = normalize_variable(line [1:].strip())
            if line.startswith("+"):
                additions[file].add(normalized)
            elif line.startswith("-"):
                removals[file].add(normalized)

    filtered_changes = defaultdict(list)

    for file, removed_lines in removals.items():
        for line in removed_lines:
            if not any(line in added_lines for added_lines in additions.values()):
                filtered_changes[file].append("-" + line)
                
        for file, added_lines in additions.items():
            for line in added_lines:
                if not any(line in removed_lines for removed_lines in removals.values()):
                    filtered_changes[file].append("+"+ line)

    result = []
    for file, lines in filtered_changes.items():
        result.append(f"Arquivo: {file}")
        result.extend(lines)
        
    return "\n".join(result)

def process_diff_output(filtered_diff):

    lines = filtered_diff.splitlines()
    variable_count = defaultdict(int)
    line_count = defaultdict(list)

    for line in lines:
        var = line[2:].strip()
        line_count[var].append(line)
        if line.startswith("+"):
            variable_count[var] += 1
        elif line.startswith("-"):
            variable_count[var] -= 1
        
    filtered_changes = []
    
    for var, count in variable_count.items():
        if abs(count) % 2 == 1:
            filtered_changes.append(line_count[var][-1])

    result = "\n".join(filtered_changes)
    
    return result
    
def filter_single_occurrences(filtered_result):
    lines = filtered_result.splitlines()
    variable_count = defaultdict(int)

    for line in lines:
        if '=' in line:
            var = line[2:].split('=')[0].strip()
        elif';' in line:
            var = line[2:].split(';')[0].strip()
        else:
            var = line[2:].strip()


        variable_count[var] + 1

    filtered_changes = [line for line in lines if variable_count[line[2:].split('=')[0].strip() if '' in line else line[2:].split(';')[0].strip()] == 1]
    
    result = "\n".join(filtered_changes)
    return result

def main():
    diff_file = "C:\\GIT\\MEC\\ldra\\PlatformSoftware\\2_0_1to2_0.diff"

    try:
        with open (diff_file, "r") as file:
            diff_content = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{diff_file}' não encontrado.")
        return
        
    result = filter_diff(diff_content)
    #print(result)
    filtered_result = process_diff_output(result)
    #print(filtered_result)
    
    filtered_single_result = filter_single_occurrences(filtered_result)

    print("variáveis de SA:")
    print(filtered_single_result)

if __name__ == "__main__":
    main()