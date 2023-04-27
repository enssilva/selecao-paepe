# Seleção PaEPE
Script para gerar a pontuação dos bolsistas do PaEPE - UFES

# Biblioteca python
As bibliotecas abaixo precisam ser instaladas para executar o script:
* pandas
* csv

Para instalar a biblioteca *pandas* utilize o comando abaixo:
```console
pip install pandas
```

# Executar o script
Para executar o script utilize o comando abaixo:
```console
python3 main.py
```

# Entrada
## assistencia-estudantil.csv
Arquivo CSV contendo informações sobre faixa de renda e PPI dos alunos:

|Matrícula|Nome|PPI|Faixa de Renda|
|---|---|---|---|
|9999999999|João da Silva|NÃO|Até 0,5 sm.|

Os campos devem ser:
* *matricula*: número da matrícula [**int**]
* *nome*: nome completo [**string**]
* *ppi*: SIM ou NÃO [**string**]
* *faixa de renda*: [**string**]
  * Até 0,5 sm.
  * De 0,5 a 1,0 sm.
  * De 1,0 a 1,5 sm.
  * Acima de 1,5 sm.
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

## projeto-paepe.csv
Arquivo CSV contendo informações dos projetos cadastrados no formato:
|Projeto|Tipo|
|---|---|
|Projeto ABC|2|

Os campos devem ser:
* *projeto*: título do projeto cadastrado [**string**]
* *tipo*: indica tipo do PaEPE (1 ou 2) [**int**]

# Saída
## pontuação.csv
|CPF|Nome|Projeto|Pontuação|PPI|Coeficiente normalizado|Matrícula|Curso|Faixa de Renda|E-mail|
|---|---|---|---|---|---|---|---|---|---|
|999.999.999-99|João da Silva|Projeto ABC|4,39|NÃO|5,3|9999999999|Curso XYZ|Até 0,5 sm.|joao@silva.com|