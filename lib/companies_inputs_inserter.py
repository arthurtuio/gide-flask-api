import simplejson as json

from lib.repository import EmpresasValoresInputadosRepository
from lib.postgres_connector import PostgresConnector


class CompaniesInputsInserter:
    """
    Pega o payload com 2 possíveis formatos de entrada>
    2 métodos de entrada de dados:
    - API (JSON) - parse_and_insert_API_json_payload - o payload vem direto da API, em JSON
    - CSV - parse_and_insert_CSV_payload - o payload vem como CSV

    Ambos os métodos depois chamam o método _insert_payload_on_db, que trata
    os dados (não o formato), e insere no banco de dados
    """
    def __init__(self):
        """
        :param payload_to_insert: Lista de dicionários
        """
        self._empresas_inputs_repository = None

    def parse_and_insert_API_json_payload(self, api_payload):
        parsed_api_payload = [json.loads(
            json.dumps(api_payload)
        )]

        self._insert_payload_on_db(parsed_api_payload)

    def parse_and_insert_CSV_payload(self, csv_payload): pass

    def _insert_payload_on_db(self, formatted_payload):
        list_to_insert = []

        with PostgresConnector().connect_using_default_credentials() as pg_conn:
            for row in formatted_payload:
                parsed_keys = self._parse_payload_keys(row)
                row.update(parsed_keys)

                list_to_insert.append(row)

            self._empresas_inputs_repository = EmpresasValoresInputadosRepository(pg_conn)
            self._empresas_inputs_repository.insert_inputted_data(list_to_insert)

        print("Registro inserido com sucesso no DB!")

    @staticmethod
    def _parse_payload_keys(row):
        """
        Só faz o tratamento nas chaves que podem receber valor default,
        o resto não precisa porque vai vir do proprio input
        """
        return {
            "demanda_contratada_ponta": row.get("demanda_contratada_ponta") or 0,
            "is_teste_ponta": row.get("is_teste_ponta") or False,
            "demanda_contratada_fora_ponta": row.get("demanda_contratada_fora_ponta") or 0,
            "is_teste_fora_ponta": row.get("is_teste_fora_ponta") or False,
            "geracao_ener_ponta": row.get("geracao_ener_ponta") or 0,
            "geracao_ener_fora_ponta": row.get("geracao_ener_fora_ponta") or 0,
            "ener_reat_exced_ponta": row.get("ener_reat_exced_ponta") or 0,
            "ener_reat_exced_fora_ponta": row.get("ener_reat_exced_fora_ponta") or 0,
            "demanda_reat_exced_ponta": row.get("demanda_reat_exced_ponta") or 0,
            "demanda_reat_exced_fora_ponta": row.get("demanda_reat_exced_fora_ponta") or 0,
        }


if __name__ == '__main__':
    payload = [{
        "data_referencia": "01-01-2020",
        "fornecedora": "CELESC",
        "unidade_consumidora": 1234567,
        "nome_cliente": "Teste",
        "modalidade": "Verde",
        "subgrupo": "A4",
        #"demanda_contratada_ponta": 12345,
        #"is_teste_ponta": True,
        #"demanda_contratada_fora_ponta": 12345,
        #"is_teste_fora_ponta": True,
        "consumo_ponta": 198,
        "consumo_fora_ponta": 2344,
        #"geracao_ener_ponta": 123,
        #"geracao_ener_fora_ponta": 123,
        #"ener_reat_exced_ponta": 123,
        #"ener_reat_exced_fora_ponta": 123,
        #"demanda_reat_exced_ponta": 123,
        #"demanda_reat_exced_fora_ponta": 123,
        "demanda_medida_ponta": 45.72,
        "demanda_medida_fora_ponta": 23.56,
    }]
    CompaniesInputsInserter()._insert_payload_on_db(payload)
