import re

def arquivos_modificados_com_palavras_chave(arquivo_diff, palavras_chave):
    """
    Processa um arquivo de diff do Git e retorna os arquivos que sofreram alterações 
    em linhas contendo palavras-chave específicas.

    :param arquivo_diff: Caminho para o arquivo de diff do Git
    :param palavras_chave: Lista de palavras-chave para buscar
    :return: Conjunto de arquivos que possuem as palavras-chave nas linhas alteradas
    """
    # Compila o regex para buscar as palavras-chave em linhas adicionadas (+) ou removidas (-)
    padrao = re.compile(r"^[\+\-].*(" + "|".join(re.escape(palavra) for palavra in palavras_chave) + r")", re.MULTILINE)

    # Armazena os arquivos que satisfazem os critérios
    arquivos_modificados = set()

    # Lê o arquivo de diff
    with open(arquivo_diff, "r") as f:
        diff = f.read()

    # Divide o diff por arquivo usando o indicador "diff --git"
    blocos = diff.split("diff --git")
    print(f"Total de blocos encontrados: {len(blocos) - 1}")
    for i, bloco in enumerate(blocos[1:], start=1):  # Ignora o primeiro elemento vazio
        print(f"\nProcessando bloco {i}:")
        linhas = bloco.splitlines()
        
        # Identifica o nome do arquivo (após b/)
        arquivo = None
        for linha in linhas:
            if linha.startswith("--- a/"):
                continue
            if linha.startswith("+++ b/"):
                arquivo = linha[6:]  # Remove o prefixo "+++ b/"
                print(f"Arquivo identificado: {arquivo}")
                break
        
        # Verifica se alguma linha alterada contém as palavras-chave
        if padrao.search("\n".join(linhas)):
            print(f"Palavra-chave encontrada em {arquivo}")
            arquivos_modificados.add(arquivo)
        else:
            print(f"Nenhuma palavra-chave encontrada em {arquivo}")
    
    return arquivos_modificados


if __name__ == "__main__":
    # Caminho para o arquivo .diff (hardcoded)
    arquivo_diff = "exemplo.diff"

    # Palavras-chave para buscar
    palavras_chave = ["@brief", "@details", "@addFault"]

    # Processa o diff e retorna os arquivos modificados
    arquivos = arquivos_modificados_com_palavras_chave(arquivo_diff, palavras_chave)

    # Exibe os arquivos
    print("\nArquivos que sofreram modificações nas linhas contendo as palavras-chave:")
    for arquivo in arquivos:
        print(arquivo)
