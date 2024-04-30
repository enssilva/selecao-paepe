# Seleção PaEPE
Script para gerar a pontuação dos bolsistas do PaEPE - UFES

# Biblioteca python
As bibliotecas abaixo precisam ser instaladas para executar o script:
* pandas

Para instalar a biblioteca *pandas* utilize o comando abaixo:
```bash
pip install pandas
```

# Executar o script
Para executar o script utilize o comando abaixo:
```bash
python3 main.py
```
Se quiser algumas informações sobre parâmetros de entrada do script utilize a opção **-h**:
```console
user@host:~$ python3 main.py -h
usage: main.py [-h] [-di DATA_INICIO] [-df DATA_FIM] [--candidatos CANDIDATOS] [--assistencia_estudantil ASSISTENCIA_ESTUDANTIL] [--projeto_paepe PROJETO_PAEPE]

Gera a lista dos alunos inscritos com suas respectivas notas e agrupados por projeto (pontuação.csv)

options:
  -h, --help            show this help message and exit
  -di DATA_INICIO, --data_inicio DATA_INICIO
                        Data de início do período de inscrição no formato dd/mm/yyyy para filtrar inscritos
  -df DATA_FIM, --data_fim DATA_FIM
                        Data final do período de inscrição no formato dd/mm/yyyy para filtrar inscritos
  --candidatos CANDIDATOS
                        Nome do arquivo com a lista de candidatos contendo as seguintes colunas: CPF, Projeto, Nome, Curso, Coeficiente normalizado, E-mail
  --assistencia_estudantil ASSISTENCIA_ESTUDANTIL
                        Nome do arquivo com a lista de assistência estudantil contendo as seguintes colunas: Matrícula, CPF, Nome, PPI, Faixa de Renda
  --projeto_paepe PROJETO_PAEPE
                        Nome do arquivo com a lista dos projetos contendo as seguintes colunas: Projeto, Tipo
```

# Entrada
## assistencia_estudantil.csv
Arquivo CSV contendo informações sobre faixa de renda e PPI dos alunos:

|Matrícula|CPF|Nome|PPI|Faixa de Renda|
|---|---|---|---|---|
|9999999999|111.111.111-11|João da Silva|NÃO|menor que 0,5 SM|

Os campos devem ser:
* *matricula*: número da matrícula [**int**]
* *cpf*: CPF com ponto e traço [**string**]
* *nome*: nome completo [**string**]
* *ppi*: SIM ou NÃO [**string**]
* *faixa de renda*: [**string**]
  * menor que 0,5 SM
  * maior que 0,5 e menor ou igual a 1,0 SM
  * maior que 1,0 e menor ou igual a 1,5 SM
  * maior que 1,5 SM
  * Não informado

## candidatos.csv
Arquivo CSV contendo informações dos inscritos no formato:

|CPF|Projeto|Nome|Curso|Coeficiente normalizado|E-mail|
|---|---|---|---|---|---|
|999.999.999-99|Projeto ABC|João da Silva|Curso XYZ|5,3|joao@silva.com|

Os campos devem ser:
* *cpf*: número do CPF com os pontos e traço [**string**]
* *projeto*: nome do projeto [**string**]
* *nome*: nome completo [**string**]
* *curso*: nome do curso [**string**]
* *coeficiente normalizado*: coeficiente normalizado [**float**]
* *e-mail*: e-mail [**string**]

As informações podem ser obtidas via o [site](https://www.sistemasweb.ufes.br/proplan/pib/) do PIB:
* *Acesso ao sistema* -> *Acessar* -> *Candidatos*
* Em **Título do Projeto:** selecione **Todos**
* Selecione o resultado mostrado na tela, incluindo o cabeçalho, e cole em uma planilha. Exporte a planilha como arquivo CSV.

## projeto_paepe.csv
Arquivo CSV contendo informações dos projetos cadastrados no formato:
|Projeto|Tipo|
|---|---|
|Projeto ABC|2|

Os campos devem ser:
* *projeto*: título do projeto cadastrado [**string**]
* *tipo*: indica tipo do PaEPE (1 ou 2) [**int**]

# Saída
## pontuação.csv

Arquivo CSV contendo a pontuação de cada candidato com as informações utilizadas para calcular a pontuação:
|PaEPE|CPF|Nome|Projeto|Pontuação|PPI|Coeficiente normalizado|Pontos (renda)|Faixa de Renda|Matrícula|Curso|E-mail|Data de cadastramento|OBS|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|999.999.999-99|João da Silva|Projeto ABC|4,39|NÃO|5,3|3|menor que 0,5 SM|9999999999|Curso XYZ|joao@silva.com|01/04/99||