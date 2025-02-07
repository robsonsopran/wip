import subprocess

# Caminho fixo para o Windows Terminal portátil
WT_PATH = r"D:\Portables\WindowsTerminal\wt.exe"  # <-- Defina o caminho correto!

# Defina as abas com diretórios, tipos de shell e títulos personalizados
abas = [
    {"caminho": "C:/Users/Robso/Documents/Arduino", "shell": "gitbash", "titulo": "Arduino Dev"},  # Git Bash
    {"caminho": "C:/Users/Robso/Documents", "shell": "powershell", "titulo": "Docs PowerShell"},  # PowerShell
    {"caminho": "C:/Users/Robso", "shell": "cmd", "titulo": "User CMD"},  # Prompt de Comando
    {"caminho": "C:/Users", "shell": "cmd", "titulo": "Root CMD"}  # Prompt de Comando
]

# Caminho fixo para o executável do Git Bash
git_bash_path = r'"C:\Program Files\Git\bin\bash.exe" --login -i'

# Monta o comando para abrir o Windows Terminal com abas específicas e títulos
comando = f'"{WT_PATH}"'
for aba in abas:
    caminho = aba["caminho"]
    shell = aba["shell"]
    titulo = aba["titulo"]
    
    if shell == "gitbash":
        comando += f' new-tab --title "{titulo}" {git_bash_path} -c "cd \\"{caminho}\\" && exec bash" ;'
    elif shell == "powershell":
        comando += f' new-tab --title "{titulo}" powershell -NoExit -Command "Set-Location -Path {caminho}" ;'
    else:  # Para o caso do Prompt de Comando (cmd)
        comando += f' new-tab --title "{titulo}" cmd /k "cd /d {caminho}" ;'

# Executa o comando
subprocess.Popen(comando, shell=True)

print("Windows Terminal aberto com abas nomeadas e específicas para diferentes terminais.")
