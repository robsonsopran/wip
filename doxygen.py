import re

def arquivos_modificados_com_palavras_chave(diff, palavras_chave):
    """
    Processa o diff do Git e retorna os arquivos que sofreram alterações 
    em linhas contendo palavras-chave específicas.

    :param diff: String contendo o diff do Git
    :param palavras_chave: Lista de palavras-chave para buscar
    :return: Conjunto de arquivos que possuem as palavras-chave nas linhas alteradas
    """
    # Compila o regex para buscar as palavras-chave em linhas adicionadas (+) ou removidas (-)
    padrao = re.compile(r"^[\+\-].*(" + "|".join(re.escape(palavra) for palavra in palavras_chave) + r")", re.MULTILINE)

    # Armazena os arquivos que satisfazem os critérios
    arquivos_modificados = set()

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
    # Exemplo de diff do Git
    diff_exemplo = """\
diff --git a/arquivo1.cpp b/arquivo1.cpp
index 1234567..89abcde 100644
--- a/arquivo1.cpp
+++ b/arquivo1.cpp
@@ -10,6 +10,7 @@ void exemplo() {
+    // @brief Adicionado exemplo de documentação
-    // @details Removido detalhe antigo
}
diff --git a/arquivo2.h b/arquivo2.h
index abcdef0..1234567 100644
--- a/arquivo2.h
+++ b/arquivo2.h
@@ -15,8 +15,9 @@ void outroExemplo() {
+    // @addFault Nova funcionalidade
}
diff --git a/arquivo3.txt b/arquivo3.txt
index 7654321..abcdef0 100644
--- a/arquivo3.txt
+++ b/arquivo3.txt
@@ -5,6 +5,7 @@ Texto antigo
+Texto sem palavras-chave
"""

    # Palavras-chave para buscar
    palavras_chave = ["@brief", "@details", "@addFault"]

    # Processa o diff e retorna os arquivos modificados
    arquivos = arquivos_modificados_com_palavras_chave(diff_exemplo, palavras_chave)

    # Exibe os arquivos
    print("\nArquivos que sofreram modificações nas linhas contendo as palavras-chave:")
    for arquivo in arquivos:
        print(arquivo)
