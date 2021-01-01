# ref: https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask # pra fazer tudo que envolve GET e entender
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask # pra POST agora que ja entendo Flask - mas isso por si só n garante


import simplejson as json

from flask import Flask, request, abort

from lib.postgres_connector import PostgresConnector
from lib.companies_inputs_inserter import CompaniesInputsInserter
from lib.repository import (
    EmpresasValoresInputadosRepository,
    ValorTarifasRepository,
    ValorBandeirasRepository,
    ValorImpostosRepository
)

app = Flask(__name__)
app.config["DEBUG"] = True


conn_params = "dbname=postgres user=postgres password=postgres host=localhost"


@app.route('/', methods=['GET'])
def home():
    return """
        <h1>API GIDE Autonomus</h1>
        <p>API que possibilita consultar os registros do banco de dados,
        e também inserir dados de novas empresas.</p>
        
        <h3>Para fazer a consulta, use algum destes endpoints:</h3>
        <p> 
        - Tarifas: /api/v1/get/tarifas/all
        - Impostos: /api/v1/get/impostos/all
        - Bandeiras: /api/v1/get/bandeiras/all 
        - Empresas: /api/v1/get/empresas_inputadas/all
        </p>
        
        <h3>Para inserir dados de novas empresas, este:</h3>
        <p> - /api/v1/insert/empresas_inputadas/ </p>
    """


@app.route('/api/v1/get/empresas_inputadas/all', methods=['GET'])
def api_empresas_inputadas_all():
    with PostgresConnector().connect_using_default_credentials() as pg_conn:
        all_values = EmpresasValoresInputadosRepository(pg_conn).get_all_rows('estagio.empresas_valores_inputados')

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/tarifas/all', methods=['GET'])
def api_tarifas_all():
    with PostgresConnector().connect_using_default_credentials() as pg_conn:
        all_values = ValorTarifasRepository(pg_conn).get_all_rows('estagio.valor_tarifas')

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/impostos/all', methods=['GET'])
def api_impostos_all():
    with PostgresConnector().connect_using_default_credentials() as pg_conn:
        all_values = ValorImpostosRepository(pg_conn).get_all_rows('estagio.valor_impostos')

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/bandeiras/all', methods=['GET'])
def api_bandeiras_all():
    with PostgresConnector().connect_using_default_credentials() as pg_conn:
        all_values = ValorBandeirasRepository(pg_conn).get_all_rows('estagio.valor_bandeiras')

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/insert/empresas_inputadas', methods=['POST'])
def insert_company():
    if not request.json:
        abort(400)

    payload = {
        "data_referencia": request.json["data_referencia"],
        "fornecedora": request.json["fornecedora"],
        "unidade_consumidora": request.json["unidade_consumidora"],
        "nome_cliente": request.json["nome_cliente"],
        "modalidade": request.json["modalidade"],
        "subgrupo": request.json["subgrupo"],
        "consumo_ponta": request.json["consumo_ponta"],
        "consumo_fora_ponta": request.json["consumo_fora_ponta"],
        "demanda_medida_ponta": request.json["demanda_medida_ponta"],
        "demanda_medida_fora_ponta": request.json["demanda_medida_fora_ponta"],
    }

    CompaniesInputsInserter().parse_and_insert_API_json_payload(payload)

    return f"""
        O seguinte registro foi inserido no banco:
        {type(json.loads(json.dumps(payload)))}
        {json.dumps(payload)}
    """


if __name__ == '__main__':
    app.run()
