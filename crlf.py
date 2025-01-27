def converter_lf_para_crlf(lista_arquivos_txt):
    try:
        # Lê o arquivo que contém a lista de arquivos a serem processados
        with open(lista_arquivos_txt, 'r', encoding='utf-8') as lista_arquivos:
            arquivos = lista_arquivos.readlines()

        for arquivo in arquivos:
            arquivo = arquivo.strip()  # Remove espaços ou quebras de linha extras
            if not arquivo:
                continue  # Ignora linhas vazias

            try:
                # Lê o conteúdo do arquivo e converte LF para CRLF
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read().replace('\n', '\r\n')

                # Salva o conteúdo de volta no arquivo com o formato CRLF
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)

                print(f"Convertido com sucesso: {arquivo}")
            except Exception as e:
                print(f"Erro ao processar o arquivo {arquivo}: {e}")

    except Exception as e:
        print(f"Erro ao abrir a lista de arquivos: {e}")


# Exemplo de uso:
# Substitua 'lista_de_arquivos.txt' pelo caminho para o arquivo que contém a lista de arquivos a serem processados.
converter_lf_para_crlf('lista_de_arquivos.txt')
