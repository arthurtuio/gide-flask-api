from psycopg2.extras import DictCursor, RealDictCursor


class BaseRepository:
    def __init__(self, pg_conn):
        self._pg_conn = pg_conn

    def get_all_rows(self, sql_table):
        with self._pg_conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(self.select_all_template(sql_table))

            return cursor.fetchall()

    @staticmethod
    def select_all_template(sql_table):
        return f"SELECT * from {sql_table}"


class ValorTarifasRepository(BaseRepository):
    def __init__(self, pg_conn):
        super(ValorTarifasRepository, self).__init__(pg_conn)

    def get_all_fares(self, cursor_factory=DictCursor):
        with self._pg_conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(
                self._get_all_fares_sql_template()
            )

            return cursor.fetchall()

    def get_fares(self, input_params):
        """
        :param input_params: Dicionário com as seguintes chaves:
                reference_date
                fornecedora
                posto
                modalidade
                subgrupo
        """
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                self._get_fares_sql_template(),
                input_params
            )

            return cursor.fetchall()

    @staticmethod
    def _get_all_fares_sql_template():
        return """
            SELECT
                tusde,
                te,
                tu,
                td,
                td_exc_reat
            FROM
                estagio.valor_tarifas
        """

    def _get_fares_sql_template(self):
        return f"""
            {self._get_all_fares_sql_template()}
            WHERE
                vigencia_inicio::date <= %(reference_date)s::date
                AND vigencia_fim::date > %(reference_date)s::date
                AND fornecedora = %(fornecedora)s
                AND posto = %(posto)s
                AND modalidade = %(modalidade)s
                AND subgrupo = %(subgrupo)s
        """


class ValorBandeirasRepository(BaseRepository):
    def __init__(self, pg_conn):
        super(ValorBandeirasRepository, self).__init__(pg_conn)

    def get_all_flags(self, cursor_factory=DictCursor):
        with self._pg_conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(
                self._get_all_flags_sql_template()
            )

            return cursor.fetchall()

    def get_flag_type_and_value(self, reference_date: str):
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                self._get_flag_sql_template(),
                {"reference_date": reference_date}
            )

            return cursor.fetchall()

    @staticmethod
    def _get_all_flags_sql_template():
        return """
            SELECT
                bandeira,
                rs_por_kw
            FROM
                estagio.valor_bandeiras
        """

    def _get_flag_sql_template(self):
        return f"""
            {self._get_all_flags_sql_template()}
            WHERE
                 data_referencia = %(reference_date)s
        """


class ValorImpostosRepository(BaseRepository):
    def __init__(self, pg_conn):
        super(ValorImpostosRepository, self).__init__(pg_conn)

    def get_all_taxes(self, cursor_factory=DictCursor):
        with self._pg_conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(
                self._get_all_taxes_sql_template()
            )

            return cursor.fetchall()

    def get_taxes(self, reference_date: str):
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                self._get_taxes_sql_template(),
                {"reference_date": reference_date}
            )

            return cursor.fetchall()

    @staticmethod
    def _get_all_taxes_sql_template():
        return """
            SELECT
                icms,
                icms_reduzido,
                pis,
                cofins
            FROM
                estagio.valor_impostos
        """

    def _get_taxes_sql_template(self):
        return f"""
            {self._get_all_taxes_sql_template()}
            WHERE
                 data_referencia = %(reference_date)s
        """


class EmpresasValoresInputadosRepository(BaseRepository):
    def __init__(self, pg_conn):
        super(EmpresasValoresInputadosRepository, self).__init__(pg_conn)

    def get_all_companies(self, cursor_factory=DictCursor):
        with self._pg_conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(
                self._get_all_companies_sql_template()
            )

            return cursor.fetchall()

    def insert_inputted_data(self, payload):
        with self._pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.executemany(
                self._get_insert_sql_template(),
                payload
            )

    @staticmethod
    def _get_all_companies_sql_template():
        return """
            SELECT
                data_referencia,
                fornecedora,
                unidade_consumidora,
                nome_cliente,
                modalidade,
                subgrupo,
                demanda_contratada_ponta,
                is_teste_ponta,
                demanda_contratada_fora_ponta,
                is_teste_fora_ponta,
                consumo_ponta,
                consumo_fora_ponta,
                geracao_ener_ponta,
                geracao_ener_fora_ponta,
                ener_reat_exced_ponta,
                ener_reat_exced_fora_ponta,
                demanda_reat_exced_ponta,
                demanda_reat_exced_fora_ponta,
                demanda_medida_ponta,
                demanda_medida_fora_ponta
            FROM
                estagio.empresas_valores_inputados
        """

    @staticmethod
    def _get_insert_sql_template():
        return """
            INSERT INTO estagio.empresas_valores_inputados
            (
                data_referencia,
                fornecedora,
                unidade_consumidora,
                nome_cliente,
                modalidade,
                subgrupo,
                demanda_contratada_ponta,
                is_teste_ponta,
                demanda_contratada_fora_ponta,
                is_teste_fora_ponta,
                consumo_ponta,
                consumo_fora_ponta,
                geracao_ener_ponta,
                geracao_ener_fora_ponta,
                ener_reat_exced_ponta,
                ener_reat_exced_fora_ponta,
                demanda_reat_exced_ponta,
                demanda_reat_exced_fora_ponta,
                demanda_medida_ponta,
                demanda_medida_fora_ponta
            )
            VALUES
            (
                %(data_referencia)s,
                %(fornecedora)s,
                %(unidade_consumidora)s,
                %(nome_cliente)s,
                %(modalidade)s,
                %(subgrupo)s,
                %(demanda_contratada_ponta)s,
                %(is_teste_ponta)s,
                %(demanda_contratada_fora_ponta)s,
                %(is_teste_fora_ponta)s,
                %(consumo_ponta)s,
                %(consumo_fora_ponta)s,
                %(geracao_ener_ponta)s,
                %(geracao_ener_fora_ponta)s,
                %(ener_reat_exced_ponta)s,
                %(ener_reat_exced_fora_ponta)s,
                %(demanda_reat_exced_ponta)s,
                %(demanda_reat_exced_fora_ponta)s,
                %(demanda_medida_ponta)s,
                %(demanda_medida_fora_ponta)s
            )
            -- ON CONFLICT ON CONSTRAINT blip_normalized_messages_message_id_key DO NOTHING
        """

class Repository:
    """
    Classe pra comunicação com o banco de dados.

    Provavelmente usa psycopg2 pra falar com o banco de dados
    """
    def __init__(self, conn_id):
        self.conn_id = conn_id

    def get_company_latest_row(self, company_id):
        """
        Método que pega o registro mais recente do banco, dado
        o ID/nome da empresa que eu quero.

        Esse registro é usado para realizar alguns calculos.
        :param company_id: O ID (ou nome) da empresa que quero consultar
        o ultimo registro.
        :return: Vai retornar a linha com todas as colunas que eu quiser do banco.
        """
        # vai ser uma query esse metodo, que vai usar um WHERE company ID
        # e pegar o ultimo created_at ou updated_at
        pass

    def insert_rows(self):

        """
        Método que vai inserir as linhas ja com os calculos no database.

        É aqui que eu ponho o created_at = now, e outras coisinhas se precisar.

        :return: Vai retornar a query de insert
        """

    def get_corresponding_fares(self):
        """
        Fares = tarifas
        Metodo que vai pegar as tarifas correspondentes no banco
        As tarifas (de acordo com a planilha sao):
            - TUSDE-P (R$/kWh)
            - TE-P (R$/kWh)
            - TUSDE-FP (R$/kWh)
            - TE-FP (R$/kWh)
            - TUFO (R$/kVArh): Tarifa do Consumo de Energia Reativa Excedente na Ponta = B1 Convencional
            - TUFF (R$/kVArh): Tarifa do Consumo de Energia Reativa Excedente Fora de Ponta = B1 Convencional
            - TDNP (R$/kW): Tarifa de Demanda na Ponta
            - TDNF (R$/kW): Tarifa de Demanda Fora de Ponta
            - TDRE (R$/kW): Tarifa de Demanda Excedente de Reativos
            - Adicional Bandeira (R$/kWh)
        :return: Vai retornar a query de SELECT com o WHERE pra pegar certinho as tarifas, com
        base na logica usada da planilha
        """
