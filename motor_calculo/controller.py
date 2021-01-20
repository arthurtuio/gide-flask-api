from lib.postgres_connector import PostgresConnector
from lib.repository import (
    EmpresasValoresInputadosRepository,
    ValorTarifasRepository,
    ValorBandeirasRepository,
    ValorImpostosRepository
)


class Controller:
    def __init__(self, company_name, reference_date):
        """
    Classe que realiza todos os cálculos para as colunas da tabela empresas_valores_calculados.
    É chamada sempre passando na entrada os dados de uma empresa, em um mês, ou seja, quase
    uma linha do banco.

    Com esses dados ela busca os demais dados da empresa no banco, e usa eles pra realizar
    os calculos necessários.
    """
        self.company_name = company_name
        self.reference_date = reference_date

    def execute(self):
        db_connection = PostgresConnector().connect_using_localhost_credentials()

        with db_connection as pg_conn:
            empresas_repository = EmpresasValoresInputadosRepository(pg_conn)
            tarifas_repository = ValorTarifasRepository(pg_conn)
            bandeiras_repository = ValorBandeirasRepository(pg_conn)
            impostos_repository = ValorImpostosRepository(pg_conn)

            company_month_data = self._get_company_month_data(empresas_repository)
            company_params = self._get_company_params(company_month_data)

            print(f"company_month_data: {company_month_data}")
            print(f"company_params: {company_params}")

            # Calculos daqui pra baixo #
            tusde_p_and_fp_reais = self._calculate_tusd_energia_reais(
                company_month_data, company_params, tarifas_repository
            )

            energia_cativo_p_and_fp_reais = self._calculate_energia_cativo_reais(
                company_month_data, company_params, tarifas_repository
            )


    # def _calculate_sobras_and_ultrapassagem_reais(self, empresas_repository):
    #     self._calculate_sobras_and_ultrapassagem_kw(empresas_repository)

    # def _calculate_sobras_and_ultrapassagem_kw(self, empresas_repository):
    #     """
    #     Pega os dados da empresa e mês em questão,
    #     e aí calcula:
    #     - IF MODALIDADE = AZUL, calcula Sobra e Ultrapassagem na Ponta, e tbm FP
    #         - Se for VERDE, apenas fora da ponta
    #
    #     Precisa dos valores de demanda_contratada minima e max, pra ponta e fp. isso por
    #     sua vez precisa ser feito com base nas regras desse slide>
    #     https://docs.google.com/presentation/d/1xU6kjrg1Zz1NQm2152Rc4whT6MZ1byOAuWRYb5i1DV8/edit#slide=id.gadad5d60d2_0_87
    #     """
    #     company_data = self._get_company_month_data(empresas_repository)
    #
    #     sobra_p_kw = 0,
    #     sobra_fp_kw = 0
    #
    #     if company_data["modalidade"] == "Azul":
    #         sobra_p_kw = dem_contratada_min_p - dem_medida_p
    #         sobra_fp_kw = 2*(dem_contratada_min_fp - dem_medida_fp)
    #
    #     ultrapassagem_p_kw = dem_contratada_max_fp - dem_medida_p
    #     ultrapassagem_fp_kw = 2*(dem_contratada_max_fp - dem_medida_fp)
    #
    #     return {
    #         "sobra_p_kw": sobra_p_kw,
    #         "sobra_fp_kw": sobra_fp_kw,
    #         "ultrapassagem_p_kw": ultrapassagem_p_kw,
    #         "ultrapassagem_fp_kw": ultrapassagem_fp_kw,
    #     }

    def _calculate_demanda_max_e_min(self, company_month_data, empresas_repository):
        """
        - Demanda mínima:
        Ex:
        [Mês | dem contratada | periodo teste? | Dem mín | Justificativa                                     ]
        [1   |             30 | FALSE          |      30 | É a mesma da contratada, pq não é período de teste]
        [2   |             75 | TRUE           |      30 | É a do último mês antes de ser teste              ]
        [3   |             75 | TRUE           |      30 | Como a do mês 2 é igual a desse mês, a demanda min ainda é a do mês anterior ao teste]
        [4   |             90 | TRUE           |      75 | Como a do mês 3 é DIFERENTE a desse mês, a demanda min passa a ser do mês anterior]

        Ou seja:
        - if periodo de testes:
            -> demanda minima é igual a demanda contratada do ultimo mês com troca
        - else = demanda contratada

        - Demanda MÁXIMA FP:
            - Se não for período de teste, é = demanda contratada*1,05
            - Se for, é a demanda contratada atual*1,05 + 0,3*(diferença entre demanda contratada ATUAL e a ANTERIOR/ref)
        """
        is_teste_p = company_month_data["is_teste_ponta"]
        is_teste_fp = company_month_data["is_teste_fora_ponta"]

        # Demanda Fora Ponta #
        if not is_teste_fp:
            demanda_min_fp = company_month_data["demanda_contratada_fora_ponta"]
            demanda_max_fp = demanda_min_fp*1.05

        else:
            demanda_contratada_ref = empresas_repository.get_latest_register_with_changes_on_demanda_contratada(
                tipo_dem_contratada="Fora Ponta"
            )
            demanda_contratada_atual = company_month_data["demanda_contratada_fora_ponta"]

            demanda_min_fp = demanda_contratada_ref["demanda_contratada_fora_ponta"]
            demanda_max_fp = (demanda_contratada_atual * 1.05) + (demanda_contratada_atual - demanda_contratada_ref)*0.3

        # Demanda Ponta #
        if not is_teste_p:
            demanda_min_p = company_month_data["demanda_contratada_ponta"]
            demanda_max_fp = demanda_min_p * 1.05

        else:
            demanda_contratada_ref = empresas_repository.get_latest_register_with_changes_on_demanda_contratada(
                tipo_dem_contratada="Ponta"
            )
            demanda_contratada_atual = company_month_data["demanda_contratada_ponta"]

            demanda_min_p = demanda_contratada_ref["demanda_contratada_ponta"]
            demanda_max_p = (demanda_contratada_atual * 1.05) + (demanda_contratada_atual - demanda_contratada_ref)*0.3

        return {
            "demanda_min_fp": demanda_min_fp,
            "demanda_max_fp": demanda_max_fp,
            "demanda_min_p": demanda_min_p,
            "demanda_max_p": demanda_max_p,
        }

    def _calculate_tusd_energia_reais(
            self, company_month_data, company_params, tarifas_repository
    ):
        """
        Calcula TUSD energia pra ponta e fp.
        """
        tarifas_month_data_p = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Ponta"
        )

        tarifas_month_data_fp = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Fora Ponta"
        )

        tusd_energia_p = tarifas_month_data_p["tusde"]
        tusd_energia_fp = tarifas_month_data_fp["tusde"]

        consumo_p = company_month_data["consumo_ponta"]
        consumo_fp = company_month_data["consumo_fora_ponta"]

        tusd_energia_p_reais = consumo_p*tusd_energia_p
        tusd_energia_fp_reais = consumo_fp*tusd_energia_fp

        return {
            "tusd_energia_p_reais": tusd_energia_p_reais,
            "tusd_energia_fp_reais": tusd_energia_fp_reais
        }

    def _calculate_energia_cativo_reais(
            self, company_month_data, company_params, tarifas_repository
    ):
        tarifas_month_data_p = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Ponta"
        )

        tarifas_month_data_fp = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Fora Ponta"
        )

        te_p = tarifas_month_data_p["te"]
        te_fp = tarifas_month_data_fp["te"]

        consumo_p = company_month_data["consumo_ponta"]
        consumo_fp = company_month_data["consumo_fora_ponta"]

        energia_cativo_p_reais = consumo_p*te_p
        energia_cativo_fp_reais = consumo_fp*te_fp

        return {
            "energia_cativo_p_reais": energia_cativo_p_reais,
            "energia_cativo_fp_reais": energia_cativo_fp_reais
        }

    def _calculate_energia_reat_exc_reais(
            self, company_month_data, company_params, tarifas_repository
    ):
        tarifas_month_data_p = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Ponta"
        )

        tarifas_month_data_fp = self._get_fares_month_data(
            tarifas_repository, company_params, posto="Fora Ponta"
        )

        tu_p = tarifas_month_data_p["tu"]
        tu_fp = tarifas_month_data_fp["tu"]

        ener_reat_exc_p = company_month_data["ener_reat_exced_ponta"]
        ener_reat_exc_fp = company_month_data["ener_reat_exced_fora_ponta"]

        ener_reat_exc_p_reais = ener_reat_exc_p*tu_p
        ener_reat_exc_fp_reais = ener_reat_exc_fp*tu_fp

        return {
            "ener_reat_exc_p_reais": ener_reat_exc_p_reais,
            "ener_reat_exc_fp_reais": ener_reat_exc_fp_reais
        }

    def _get_company_month_data(self, empresas_repository):
        return empresas_repository.get_data_using_company_and_reference_date(
            reference_date=self.reference_date, company_name=self.company_name
        )
    
    @staticmethod
    def _get_company_params(company_month_data):
        return {
            "reference_date": company_month_data["data_referencia"],
            "fornecedora": company_month_data["fornecedora"],
            "modalidade": company_month_data["modalidade"],
            "subgrupo": company_month_data["subgrupo"],
        } if company_month_data else "NÃO HÁ DADOS DESSA EMPRESA, FAÇA UM NOVO REQUEST!"

    @staticmethod
    def _get_fares_month_data(tarifas_repository, company_params, posto):
        company_params.update({"posto": posto})

        print(" ")
        print("Tarifas repository::")
        print(tarifas_repository.get_fares(
            input_params=company_params
        )
)

        return tarifas_repository.get_fares(
            input_params=company_params
        )


if __name__ == '__main__':
    Controller(
        company_name="Teste",
        reference_date="01-01-2020"
    ).execute()