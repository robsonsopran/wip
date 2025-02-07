import subprocess

# Defina o caminho fixo para o executável do Windows Terminal portátil
WT_PATH = r"D:\Portables\WindowsTerminal\wt.exe"  # <-- Defina o caminho correto!

# Defina os diretórios que cada aba do terminal deve abrir e o tipo de shell para cada aba
abas = [
    {"caminho": "C:/Users/Robso/Documents/Arduino", "shell": "gitbash"},  # Git Bash
    {"caminho": "C:/Users/Robso/Documents", "shell": "powershell"},  # PowerShell
    {"caminho": "C:/Users/Robso", "shell": "cmd"},  # Prompt de Comando
    {"caminho": "C:/Users", "shell": "cmd"}  # Prompt de Comando
]

# Caminho fixo para o executável do Git Bash
git_bash_path = r'"C:\Program Files\Git\bin\bash.exe" --login -i'

# Monta o comando para abrir o Windows Terminal com abas específicas
comando = f'"{WT_PATH}"'
for aba in abas:
    caminho = aba["caminho"]
    shell = aba["shell"]
    
    if shell == "gitbash":
        comando += f' new-tab {git_bash_path} -c "cd \\"{caminho}\\" && exec bash" ;'
    elif shell == "powershell":
        comando += f' new-tab powershell -NoExit -Command "Set-Location -Path {caminho}" ;'
    else:  # Para o caso do Prompt de Comando (cmd)
        comando += f' new-tab cmd /k "cd /d {caminho}" ;'

# Executa o comando
subprocess.Popen(comando, shell=True)

print("Windows Terminal aberto com abas específicas de diferentes terminais.")
