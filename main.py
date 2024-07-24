import pandas
from datetime import datetime
import argparse

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

# incode_point = {
#     'menor que 0,5 SM': 4,
#     'maior que 0,5 e menor ou igual a 1,0 SM': 3,
#     'maior que 1,0 e menor ou igual a 1,5 SM': 2,
#     'maior que 1,5 SM': 1,
#     'Não informado': 1,
#     'NaN': 1
# }
incode_point = {
    'até 0,5 salário mínimo': 4,
    'entre 0,5 e 1 salário mínimo': 3,
    'entre 1 e 1,5 salário mínimo': 2,
    'acima de 1,5 salário mínimo': 1,
    'Não informado': 1,
    'NaN': 1,
    '-': 1
}
def calcula_pontuacao(paepe, renda, crn):
    ae_point = incode_point[renda] if not pandas.isna(renda) else 1
    if paepe == 1:
        score = 0.3*ae_point+0.7*crn
    else:
        score = 0.7*ae_point+0.3*crn
    return score

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Gera a lista dos alunos inscritos com suas respectivas notas e agrupados por projeto (pontuação.csv)'
    )
    parser.add_argument('-di', '--data_inicio', type=str, required=False,
                        help='Data de início do período de inscrição no formato dd/mm/yyyy para filtrar inscritos')
    parser.add_argument('-df', '--data_fim', type=str, required=False,
                        help='Data final do período de inscrição no formato dd/mm/yyyy para filtrar inscritos')
    parser.add_argument('--candidatos', type=str, required=False, default='candidatos.csv',
                        help='Nome do arquivo com a lista de candidatos contendo as seguintes colunas: CPF, Projeto, Nome, Curso, Coeficiente normalizado, Data de cadastramento, E-mail')
    parser.add_argument('--assistencia_estudantil', type=str, required=False, default='assistencia_estudantil.csv',
                        help='Nome do arquivo com a lista de assistência estudantil contendo as seguintes colunas: Matrícula, CPF, Nome, PPI, Faixa de Renda')
    parser.add_argument('--projeto_paepe', type=str, required=False, default='projeto_paepe.csv',
                        help='Nome do arquivo com a lista dos projetos contendo as seguintes colunas: Projeto, Tipo')
    
    args = parser.parse_args()
    
    # verifica se a data está no formato correto
    try:
        if args.data_inicio is not None:
            DATA_INSCRICAO_INICIO = datetime.strptime(args.data_inicio, '%d/%m/%Y')
        if args.data_fim is not None:
            DATA_INSCRICAO_FIM = datetime.strptime(args.data_fim, '%d/%m/%Y')
    except ValueError:
        print('Data no formato errado.')
        exit(1)

    # lê o arquivo com os candidatos
    df_candidatos = pandas.read_csv(args.candidatos, parse_dates=['Data de cadastramento'], date_format="%d/%m/%Y")
    # lê o arquivo da assistência estudantil
    df_assit_est = pandas.read_csv(args.assistencia_estudantil, dtype={'Matrícula': 'Int32'})
    # lê o arquivo com os projetos e seus tipos
    df_projeto_paepe = pandas.read_csv(args.projeto_paepe)

    # junta as listas de candidatos e da assistência estudantil a partir do CPF
    df_pontuacao = pandas.merge(df_candidatos,df_assit_est, on='CPF', how='left')
    # junta a lista resultante com a lista de projetos a partir do nome do projeto
    df_pontuacao = pandas.merge(df_pontuacao,df_projeto_paepe, on='Projeto', how='left')
    # renomeia a coluna Tipo para PaEPE
    df_pontuacao.rename(columns={'Tipo': 'PaEPE'}, inplace=True)

    # renomeia a coluna Nome_x para Nome
    df_pontuacao.rename(columns={'Nome_x': 'Nome'}, inplace=True)
    # remove espaços no início e no final do nome
    df_pontuacao['Nome'] = df_pontuacao['Nome'].apply(lambda nome: nome.strip())

    # ajusta os coeficientes baseados nas regras:
    #   CRN vazio ou com traço: CRN = 0 precisa verificar a situação do candidato
    #   CRN > 10 (estudante finalista): subtrai-se 10 do CRN
    df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda crn: float(crn.replace(',','.')) if is_number(crn.replace(',','.')) else 0)
    df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda crn: crn if crn <= 10 else crn-10)

    # adiciona uma coluna OBS para indicar se algum aluno possui CRN == 0
    df_pontuacao['OBS'] = df_pontuacao.apply(lambda row: 'Verificar CPF e matrícula do estudante. CRN == 0' if row['Coeficiente normalizado'] == 0 else '', axis=1)

    # adiciona uma coluna com a nota de vulnerabilidade socioeconômica
    df_pontuacao['Pontos (renda)'] = df_pontuacao.apply(lambda row: incode_point[row['Faixa de Renda']] if not pandas.isna(row['Faixa de Renda']) else 1, axis=1)

    # calcula a pontuação dos candidatos baseados do tipo do PaEPE (I ou II), faixa de renda e o CRN
    df_pontuacao['Pontuação'] = df_pontuacao.apply(lambda row: calcula_pontuacao(row['PaEPE'], row['Faixa de Renda'], row['Coeficiente normalizado']), axis=1)

    # faz a ordenação descendente da pontuação por projeto, mantendo os projetos do mesmo tipo juntos
    df_pontuacao = df_pontuacao.sort_values(['PaEPE', 'Projeto', 'Pontuação'], ascending=[True, True, False])

    # converte a pontuação e o CRN em string substituindo o '.' por ',' para serem compatíveis com o padrão pt-br
    df_pontuacao['Pontuação'] = df_pontuacao['Pontuação'].apply(lambda point: str(point).replace('.',','))
    df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda point: str(point).replace('.',','))

    # elimina candidados fora do prazo de inscrição
    if args.data_inicio is not None:
        df_pontuacao = df_pontuacao.loc[df_pontuacao['Data de cadastramento'] >= DATA_INSCRICAO_INICIO]
    if args.data_fim is not None:
        df_pontuacao = df_pontuacao.loc[df_pontuacao['Data de cadastramento'] <= DATA_INSCRICAO_FIM]

    # seleciona as colunas que serão exportadas
    df_pontuacao = df_pontuacao[['PaEPE', 'CPF', 'Nome', 'Projeto', 'Pontuação', 'PPI', 'Coeficiente normalizado', 'Pontos (renda)', 'Faixa de Renda', 'Matrícula', 'Curso', 'E-mail', 'Data de cadastramento', 'OBS']]
    # exporta a lista com a pontuação para o arquivo pontuação.csv
    df_pontuacao.to_csv(path_or_buf='pontuação.csv', date_format="%d/%m/%Y", index=False)