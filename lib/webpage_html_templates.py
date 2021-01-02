

def home_template():
    return """
        <h1>API GIDE Autonomus</h1>
        <p>API que possibilita consultar os registros do banco de dados,
        e também inserir dados de novas empresas.</p>
        
        <p><b>Essa página não foi criada para ser usada
        como principal, ela é apenas a API!!</b></p>
        
        <p><b>Para consultar os dados dela, inserir CSVs, etc, acesse a página
        oficial (que por baixo dos panos usa essa API):
        link da pagina do streamlit OU wegnology
        </b></p>
        
        <h2>Usando a API para inserir e buscar:</h2>
        
        <h3>Para fazer a consulta, use algum destes endpoints:</h3>
         
        <p> - Tarifas: /api/v1/get/tarifas/all </p>
        <p> - Impostos: /api/v1/get/impostos/all </p>
        <p> - Bandeiras: /api/v1/get/bandeiras/all </p>
        <p> - Empresas: /api/v1/get/empresas_inputadas/all</p>
        
        
        <h3>Para inserir dados de novas empresas, este:</h3>
        <p> - /api/v1/insert/empresas_inputadas/ </p>        
    """

