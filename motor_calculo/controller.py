from lib.postgres_connector import PostgresConnector
from lib.repository import (
    EmpresasValoresInputadosRepository,
    ValorTarifasRepository,
    ValorBandeirasRepository,
    ValorImpostosRepository
)


class Controller:
    """
    Classe que realiza todos os cálculos para as colunas da tabela empresas_valores_calculados.
    """
    def __init__(self):
        pass

    def execute(self):
        db_connection = PostgresConnector().connect_using_localhost_credentials()

        with db_connection as pg_conn:
            empresas_repository = EmpresasValoresInputadosRepository(pg_conn)
            tarifas_repository = ValorTarifasRepository(pg_conn)
            bandeiras_repository = ValorBandeirasRepository(pg_conn)
            impostos_repository = ValorImpostosRepository(pg_conn)

    def _calculate_sobras_and_ultrapassagem_reais(self, empresas_repository):
        self._calculate_sobras_and_ultrapassagem_kw(empresas_repository)

    def _calculate_sobras_and_ultrapassagem_kw(self, empresas_repository):
        """
        Pega os dados da empresa e mês em questão,
        e aí calcula:
        - IF MODALIDADE = AZUL, calcula Sobra e Ultrapassagem na Ponta, e tbm FP
            - Se for VERDE, apenas fora da ponta
        """


