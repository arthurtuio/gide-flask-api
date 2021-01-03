# ref: https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask # pra fazer tudo que envolve GET e entender
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask # pra POST agora que ja entendo Flask - mas isso por si só n garante


import simplejson as json

from flask import Flask, request, abort
from psycopg2.extras import RealDictCursor

from lib.webpage_html_templates import home_template
from lib.postgres_connector import PostgresConnector
from lib.companies_inputs_inserter import CompaniesInputsInserter
from lib.repository import (
    EmpresasValoresInputadosRepository,
    ValorTarifasRepository,
    ValorBandeirasRepository,
    ValorImpostosRepository
)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return home_template()


@app.route('/api/v1/get/tarifas/all', methods=['GET'])
def api_tarifas_all():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = ValorTarifasRepository(pg_conn).get_all_fares(cursor_factory=RealDictCursor)

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/tarifas', methods=['GET'])
def api_tarifas_filtered_by_date():
    if "data_referencia" not in request.args:
        return "Erro: Campo 'data_referencia' não foi enviado no request!!"

    params_list = [
        "fornecedora",
        "posto",
        "modalidade",
        "subgrupo"
    ]

    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        if all(param in request.args for param in params_list):
            # Se todos os params de params_list estão tbm em request.args
            params = {
                "reference_date": request.args["data_referencia"],
                "fornecedora": request.args["fornecedora"],
                "posto": request.args["posto"],
                "modalidade": request.args["modalidade"],
                "subgrupo": request.args["subgrupo"],
            }

            all_values = ValorTarifasRepository(pg_conn).get_fares(
                cursor_factory=RealDictCursor,
                input_params=params
            )

        else:
            all_values = ValorTarifasRepository(pg_conn).get_all_fares_from_an_reference_date(
                cursor_factory=RealDictCursor,
                reference_date=request.args["data_referencia"]
            )

        return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/impostos/all', methods=['GET'])
def api_impostos_all():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = ValorImpostosRepository(pg_conn).get_all_taxes(cursor_factory=RealDictCursor)

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/impostos', methods=['GET'])
def api_impostos_filtered_by_date():
    if "data_referencia" not in request.args:
        return "Erro: Campo 'data_referencia' não foi enviado no request!!"

    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = ValorImpostosRepository(pg_conn).get_taxes(
            cursor_factory=RealDictCursor,
            reference_date=request.args["data_referencia"]
        )

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/bandeiras/all', methods=['GET'])
def api_bandeiras_all():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = ValorBandeirasRepository(pg_conn).get_all_flags(cursor_factory=RealDictCursor)

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/bandeiras', methods=['GET'])
def api_bandeiras_filtered_by_date():
    if "data_referencia" not in request.args:
        return "Erro: Campo 'data_referencia' não foi enviado no request!!"

    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = ValorBandeirasRepository(pg_conn).get_flag_type_and_value(
            cursor_factory=RealDictCursor,
            reference_date=request.args["data_referencia"]
        )

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/empresas_inputadas/all', methods=['GET'])
def api_empresas_inputadas_all():
    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = EmpresasValoresInputadosRepository(pg_conn).get_all_companies(cursor_factory=RealDictCursor)

    return json.dumps(all_values, iterable_as_array=True, default=str)


@app.route('/api/v1/get/empresas_inputadas', methods=['GET'])
def api_empresas_inputadas_filtered_by_date():
    if "data_referencia" not in request.args:
        return "Erro: Campo 'data_referencia' não foi enviado no request!!"

    with PostgresConnector().connect_using_localhost_credentials() as pg_conn:
        all_values = EmpresasValoresInputadosRepository(pg_conn).get_all_companies_from_an_reference_date(
            cursor_factory=RealDictCursor,
            reference_date=request.args["data_referencia"]
        )

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
    app.run(host='0.0.0.0', port=8080)
