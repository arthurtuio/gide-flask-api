# GIDE PROJECT

## Lógica do algoritmo ##

1. Usuário insere X linhas de dados, referentes à X faturas de energia,
 no endpoint (que ainda temos que planejar)
 
2. Esses dados chegam em uma lista, onde cada posicao é uma linha. Aí começa a lógica de ETL.

3. Pra cada primeiro item de cada empresa diferente presente nessa lista,
 preciso consultar o banco de dados passando o ID/nome da empresa, 
 pegar os dados da fatura anterior, e usar pra fazer os calculos.

4. Feito os calculos pro primeiro item, faço pros demais, 
usando os parametros sempre da posicao anterior carregados na memoria
(assim nao preciso me conectar direto ao banco). 

5. Feitos todos os calculos pra todas as linhas, envio tudo isso no banco.

6. Uma vez no banco, outra classe (que ainda nao criei) pega esses dados de lá, salva num 
outro endpoint, posteriormente sendo enviado para nossa aplicação na WEGnology,
 via requisição de API, feita do lado de lá.

### Lógica do código de ETL ###
1. Classe principal recebe o payload
2. Esse payload é enviado pra classe controller, lá, todos os cálculos são feitos
 (mais detalhado a seguir), já inserindo os dados no banco de dados.
 
### Módulos: ###

#### - `controller.py` ####
Modulo que armazena as regras de negócio.
Detalhado:
1. recebeu payload
    - Agrupa os itens por empresa. Cria novas listas pra cada empresa. 
    **Isso porque pra cada 1º registro de uma empresa, ele precisa pegar os dados no banco**
    - Cria essa nova lista com X posicoes, sendo cada posicao os dados de uma empresa, algo como:
    `[Empresa_1, Empresa_2, Empresa_3]`, e cada empresa é uma lista das linhas de dados da empresa.
2. itera em cada uma dessas listas (`for item in company_payload`)
    - Se for o 1o item, busca no banco de dados o ID/nome da empresa
    - Pros demais usa sempre a linha anterior de base
3. Calcula pra cada item o que precisa ser calculado, salva na memoria, append em lista de dict
4. Insere essa lista com as linhas pra serem inseridas no banco de dado.

#### - `repository.py` ####
Modulo que armazena a comunicação com os bancos de dados. Métodos:
- `get_latest_company_data(company_id/company_name)`: 
Metodo que pega o ultimo registro da empresa, usado pelo controller pra realizar calculos.
- `ìnsert_ALGO` (pensar no nome, algo como `ìnsert_all_input_data`:
    - Metodo que insere tudo que ta na memoria, ou seja, os dados calculados de todas
as empresas que vieram no input, no banco de dados. 
    - Observação: Mais pra frente vale avaliar enviar em batch,
quando começarmos a enviar mto, pra não onerar memória
 

## Arquitetura do banco de dados ##

**Ter as seguintes tabelas:**
1. Uma para armazenar apenas as informações que o usuário inputa;
2. Outra pra receber as colunas calculadas a partir da tabela de input, 
  apenas com os dados calculados) e com uma coluna como company_id e id da anterior
  para fazer posteriormente um Join
3. Outra que é o join dessas duas
4. Uma para armazenar as regras de tarifação da aneel/celesc  (TUSD, TE)
5. Uma para PIS, COFINS, ICMS (impostos)
6. Uma para bandeiras

**Possíveis nomes para as tabelas:**
1. companies_inputed_data
2. companies_calculated_data
3. companies_joined_data
4. fares_rules
5. taxes_rules
