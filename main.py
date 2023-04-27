import pandas
import csv

df_candidatos = pandas.read_csv('candidatos.csv')
df_assit_est = pandas.read_csv('assistencia-estudantil.csv')
paepe = {}
with open('projeto-paepe.csv') as file:
    csv_file = csv.DictReader(file)
    for line in csv_file:
        paepe[line['Projeto']] = line['Tipo']

df_candidatos['Nome'] = df_candidatos['Nome'].apply(lambda name: name[:-1] if name[-1] == ' ' else name)
df_pontuacao = pandas.merge(df_candidatos,df_assit_est, on='Nome', how='left')
incode_point = {
    'Até 0,5 sm.': 4,
    'De 0,5 a 1,0 sm.': 3,
    'De 1,0 a 1,5 sm.': 2,
    'Acima de 1,5 sm.': 1,
    'Não informado': 1,
    'NaN': 1
}

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda cr: float(cr.replace(',','.')) if is_number(cr.replace(',','.')) else 5)
df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda cr: cr if cr <= 10 else cr-10)

def calc_score(projeto, renda, cr):
    ae_point = incode_point[renda] if not pandas.isna(renda) else 1
    if paepe[projeto] == 1:
        score = 0.3*ae_point+0.7*cr
    else:
        score = 0.7*ae_point+0.3*cr
    return score

df_pontuacao['Pontuação'] = df_pontuacao.apply(lambda row: calc_score(row['Projeto'], row['Faixa de Renda'], row['Coeficiente normalizado']), axis=1)

df_pontuacao = df_pontuacao.sort_values(['Projeto', 'Pontuação'], ascending=[True, False])

df_pontuacao['Pontuação'] = df_pontuacao['Pontuação'].apply(lambda point: str(point).replace('.',','))
df_pontuacao['Coeficiente normalizado'] = df_pontuacao['Coeficiente normalizado'].apply(lambda point: str(point).replace('.',','))

df_pontuacao = df_pontuacao[['CPF', 'Nome', 'Projeto', 'Pontuação', 'PPI', 'Coeficiente normalizado', 'Matrícula', 'Curso', 'Faixa de Renda', 'E-mail']]
df_pontuacao.to_csv(path_or_buf='pontuação.csv' ,index=False)
