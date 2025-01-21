# Programa para abrir um arquivo de texto e remover todas as linhas que não contêm ".html"

def filtrar_linhas_com_html(caminho_arquivo):
    """
    Abre um arquivo de texto e remove todas as linhas que não contêm '.html'.
    Sobrescreve o arquivo original com as linhas filtradas.
    
    :param caminho_arquivo: Caminho do arquivo de texto
    """
    try:
        # Abre o arquivo para leitura
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        # Filtra apenas as linhas que contêm ".html"
        linhas_filtradas = [linha for linha in linhas if '.html' in linha]
        
        # Sobrescreve o arquivo original com as linhas filtradas
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(linhas_filtradas)
        
        print(f"Linhas sem '.html' removidas do arquivo '{caminho_arquivo}' com sucesso!")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Programa principal
if __name__ == "__main__":
    # Solicita o caminho do arquivo ao usuário
    caminho = input("Digite o caminho do arquivo de texto: ").strip()
    
    # Chama a função para filtrar as linhas
    filtrar_linhas_com_html(caminho)
