CREATE TABLE estagio.empresas_valores_inputados (
	id bigserial NOT NULL,
	data_referencia text NOT NULL,
	fornecedora text NOT NULL,
	unidade_consumidora int NOT NULL,
	nome_cliente text NOT NULL,
	modalidade text NOT NULL,
	subgrupo text NOT NULL,
	demanda_contratada_ponta int DEFAULT 0 , -- sem not null. Faz mais sentido se nao tiver ser 0, ou null? Botei default 0
	is_teste_ponta bool NOT NULL DEFAULT false,
	demanda_contratada_fora_ponta int DEFAULT 0,
	is_teste_fora_ponta bool NOT NULL DEFAULT false,
	consumo_ponta int NOT NULL,
	consumo_fora_ponta int NOT NULL,
	geracao_ener_ponta numeric NOT null DEFAULT 0,
	geracao_ener_fora_ponta numeric NOT null DEFAULT 0,
	ener_reat_exced_ponta int NOT null DEFAULT 0,
	ener_reat_exced_fora_ponta int NOT null DEFAULT 0,
	demanda_reat_exced_ponta int NOT null DEFAULT 0,
	demanda_reat_exced_fora_ponta int NOT null DEFAULT 0,
	demanda_medida_ponta numeric NOT NULL,
	demanda_medida_fora_ponta numeric NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
)

CREATE TABLE estagio.empresas_valores_calculados (
	id bigserial NOT NULL,
	inputed_data_id INT NOT NULL,
	demanda_max_p NUMERIC NOT NULL,
	demanda_min_p NUMERIC NOT NULL,
	demanda_max_fp NUMERIC NOT NULL,
	demanda_min_fp NUMERIC NOT NULL,
	sobras_p_kw NUMERIC NOT NULL default 0,
	sobras_fp_kw NUMERIC NOT NULL default 0,
	ultrapassagem_p_kw NUMERIC NOT NULL default 0,
	ultrapassagem_fp_kw NUMERIC NOT NULL default 0,
	sobras_p_reais NUMERIC NOT NULL default 0,
	sobras_fp_reais NUMERIC NOT NULL default 0,
	ultrapassagem_ponta_reais NUMERIC NOT NULL default 0,
	ultrapassagem_fponta_reais NUMERIC NOT NULL default 0,
	TUSD_Energia_P_reais NUMERIC NOT NULL,
	Energia_cativo_P_reais NUMERIC NOT NULL,
	TUSD_Energia_FP_reais NUMERIC NOT NULL,
	Energia_cativo_FP_reais NUMERIC NOT NULL,
	Energia_reat_exc_P_reais NUMERIC NOT NULL,
	Energia_reat_exc_FP_reais NUMERIC NOT NULL,
	TUSD_fio_P_reais NUMERIC NOT NULL,
	TUSD_fio_FP_reais NUMERIC NOT NULL,
	-- demanda_reat_exc_reais,
	adicional_band_reais NUMERIC NOT NULL,
	-- reembolso_geracao_reais,
	-- extras_reais,
	fatura_reais numeric NOT NULL
)

CREATE TABLE estagio.valor_tarifas (
	id bigserial NOT NULL,
	vigencia_inicio text NOT NULL,
	vigencia_fim text NOT NULL,
	fornecedora text NOT NULL,
	posto text NOT NULL,
	modalidade text NOT NULL,
	subgrupo text NOT NULL,
    TUSDE numeric NOT NULL,
    TE numeric NOT NULL,
    TU numeric NOT NULL,
    TD numeric NOT NULL,
    TD_exc_reat numeric NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
)

CREATE TABLE estagio.valor_impostos (
	id bigserial NOT NULL,
	data_referencia text NOT NULL,
    ICMS numeric NOT NULL,
    ICMS_reduzido numeric NOT NULL,
    PIS numeric NOT NULL,
    COFINS numeric NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
)

CREATE TABLE estagio.valor_bandeiras (
	id bigserial NOT NULL,
	data_referencia text NOT NULL,
    bandeira text NOT NULL,
    RS_por_kW numeric NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
)