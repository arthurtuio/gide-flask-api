

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


def simulation_home_template():
    return """
        <h1>API Machines Simulation</h1>
        <p>API que possibilita consultar dados de máquinas simuladas,
        em tempo real.</p>
        
        <p><b>O objetivo dessa API é usá-la como coleta de dados
        para uma aplicação de testes no WEGnology</b></p>


        <h3>Para fazer a consulta, use algum destes endpoints:</h3>

        <p> - Motor 1: /api/v1/get/motor1 </p>
        <p> - Motor 2: /api/v1/get/motor2 </p>
        <p> - Outra maq: `a ser criado` </p>

        <h3>Os parâmetros que são retornados de qualquer uma das requisições são:</h3>
        <p> - Corrente [A], tipo Int. Ex: corrente=223 </p>
        <p> - Tensão [V], tipo Int. Ex: tensao=21 </p>
        <p> - Timestamp atual da medição, tipo Timestamp </p>
    """

