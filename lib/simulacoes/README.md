# Simulações usando a API #

Nessa pasta você irá encontrar um código de uma API, criada da mesma forma que GIDE Flask API,
mas com o objetivo de simular o funcionamento de diversas máquinas em tempo (quase) real.

Serão simulados:
- 2 motores
- Mais alguma coisa

Os dados dessas máquinas poderão ser coletados pelas requisições, que estarão no arquivo
`app.py` (a aplicação original), e os códigos responsáveis por simular as máquinas estão 
no arquivo `machines_simulations.py`

## Observação ##
O arquivo de aplicação foi criado dentro da aplicação original pelo seguinte motivo:
**O procfile desse repo aponta pra lá, não consigo ter outro código em Python rodando em main** 
