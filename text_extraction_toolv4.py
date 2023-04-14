import tkinter as tk
from tkinter import filedialog
import re
import csv

# Função para extrair os campos do laudo
def extrair_campos(texto):
    prontuario_regex = r'Prontuário:(\d+)-'
    prontuario_match = re.search(prontuario_regex, texto)
    prontuario = prontuario_match.group(1) if prontuario_match else ''

    nome_regex = r'Nome:(.*?)Laudo:'
    nome_match = re.search(nome_regex, texto)
    nome = nome_match.group(1).strip() if nome_match else ''

    data_regex = r'Data do Exame:([\d/]+)'
    data_exame_match = re.search(data_regex, texto)
    data_exame = data_exame_match.group(1) if data_exame_match else ''

    indicacao_regex = r'INDICAÇÃO:.*?(seguimento|rastreamento|avaliação de nódulos|' \
                      r'estadiamento|avaliação de resposta|avaliação de prótese)'
    indicacao_match = re.search(indicacao_regex, texto, re.DOTALL | re.IGNORECASE)
    indicacao = indicacao_match.group(1).strip() if indicacao_match else ''

    bi_rads_regex = r'\(Breast Imaging Reporting and Data System\):? (\d[A-Z]?)(\d[A-Z]?)?'
    bi_rads_match = re.search(bi_rads_regex, texto)
    bi_rads_primeira = bi_rads_match.group(1) if bi_rads_match else ''
    bi_rads_segunda = bi_rads_match.group(2) if bi_rads_match and bi_rads_match.group(2) else ''

    conclusao_regex = r'CONCLUSÃO:(.*?)ACR BI-RADS'
    conclusao_match = re.search(conclusao_regex, texto, re.DOTALL)
    conclusao = conclusao_match.group(1).strip() if conclusao_match else ''

    return prontuario, nome, data_exame, indicacao, bi_rads_primeira, bi_rads_segunda, conclusao

# Função para lidar com o botão "Extrair"
def extrair():
    # Obtem o texto do campo de entrada
    texto = entrada_texto.get('1.0', 'end-1c')

    # Extrai os campos do laudo
    prontuario, nome, data_exame, indicacao, bi_rads_primeira, bi_rads_segunda, conclusao = extrair_campos(texto)

    # Define o nome padrão do arquivo CSV como o valor de "prontuario"
    nome_arquivo = prontuario + ".csv"

    # Abre a caixa de diálogo para salvar o arquivo CSV
    nome_arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")],
                                                initialfile=nome_arquivo)

    # Cria o arquivo CSV com o nome escolhido pelo usuário
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # Escreve os campos extraídos no arquivo CSV
        writer.writerow([prontuario, nome, data_exame, indicacao, bi_rads_primeira, bi_rads_segunda, conclusao])


# Cria a janela
janela = tk.Tk()

# Define o título da janela
janela.title("Laudo para CSV")

# Cria um campo de instruções
instrucoes = tk.Label(janela, height=4, width=80, text="Aperte CTRL+A no PDF do laudo, depois CTRL+C na área \n"
                                                       "selecionada e CTRL+V na caixa de texto abaixo. Bom trabalho! :)")
instrucoes.pack()

# Cria o campo de entrada de texto
entrada_texto = tk.Text(janela, height=10, width=55)
entrada_texto.pack()

# Cria o botão "Extrair"
botao_extrair = tk.Button(janela, text="Extrair", command=extrair)
botao_extrair.pack()

# Inicia a janela
janela.mainloop()
