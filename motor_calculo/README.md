# Motor de Cálculo #

**Observação:** Esta pasta por enquanto se encontra dentro do repositório da API, mas
a ideia é que o motor de cálculo seja algo totalmente isolado. A API apenas leva informação
de um lado a outro, e sua relação com o motor de cálculo é apenas o de chamá-lo, e pegar
o resultado do mesmo.

## Lógica do Motor ##

Principal classe recebe os seguintes argumentos de entrada:
- Nome da Empresa ou UC
- Data referencia

Com isso ele calcula os valores de demanda máx, min, etc etc, e retorna esse payload,
em forma de dicionário, que por sua vez é usado em outra classe (similar à `companies_inputs_inserter`)
e inserido no banco de dados, em uma tabela com estas colunas.

## Próximos passos ##
- Criar também a opção de calcular todos os registros de determinada empresa, passando
apenas o nome dela ou a UC, sem passar a data referência. - Isso MUUUITO PRA FRENTE
  
1. Adicionar as regras pra calcular demanda max e min, p e fp. -> Deu boa carajo!!
2. Adicionar as regras pra calcular TUSD FIO reais p e fp -> Proximo passo, ja tenho os valores, so brincar
3. Adicionar as regras pra calcular Ultrapassagem reais Ponta e Fp -> Proximo passo, ja tenho os valores, so brincar
4. Msm coisa pra adicional de bandeira