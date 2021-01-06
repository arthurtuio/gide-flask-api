# GIDE Flask API #

Este repo contém o código necessário para a criação da API da GIDE, usando a biblioteca Flask, de Python.

## Arquivos que você vai encontrar nesse repo ##
- app.py: Código principal do repositório. É nele que foi criado todos os endereços web da API;
- Procfile: Arquivo necessário para que esse repo rode no Heroku (servidor web);
- requirements.txt: Arquivo contendo as bibliotecas usadas neste repositório
- pasta lib: Contém diversos códigos auxiliares para o uso da API, de forma que deixando eles lá, o código principal
  (app.py) fica bem abstrato, e mais fácil de ser entendido.
  
## Explicando a lógica da API ##
Uma API nada mais é do que uma forma de comunicar dois serviços, como por exemplo um restaurante, onde
temos a cozinha e as mesas com os clientes, e a API são os garçons, que levam informações/comidas de um
lugar para o outro.

Neste caso, a API é responsável por entrar em contato com o banco de dados da GIDE, sendo ela o 
único caminho para buscar ou inserir informações no mesmo.

**O que a API faz:**
- Se conecta ao banco de dados por meio do arquivo `lib/postgres_connector.py`;
- Realiza operações de escrita e leitura no banco de dados, todas listadas no arquivo `lib/repository.py`. Ex:
>- Buscar registros especificos de tarifas, ou impostos, ou bandeiras, ou empresas;
>- Inserir novas empresas

Sobre o banco de dados, ele está num servidor na nuvem, criado por meio do serviço RDS, da AWS.
No proximo topico é descrito um tutorial super breve sobre como criar um banco de dados usando este serviço.

### Criando um servidor de banco de dados usando o AWS RDS ###
Referência: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
Em resumo: Lançar ele na AWS, sem segredo nisso, único detalhe são as portas!
- Adicionar uma> {Type: All Traffic, Protocol: Vai automatico, Port Range: Vai automatico, Source: Anywhere}

### Outra possibilidade de criação de servidor para a API ###
Ao invés de usar o Heroku (que é mais para testar e não botar algo definitivo), é muito mais 
recomendado o uso de uma máquina virtual, conectada a um servidor na nuvem. A AWS possui um serviço perfeito para
isto, que é o EC2. Abaixo encontra-se um tutorial de como configurar uma instância no mesmo:

#### Configurando uma instância EC2 ####

Referencia: https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc
Outra ref (to usando mais essa): https://www.twilio.com/blog/deploy-flask-python-app-aws

TL, DR:
1. Se basear pelo link pra criar a instancia EC2
2. Usar o KeyPair que criei pro TCC, que ta salvo no home da maquina e tbm no 1pass.
3. Pra logar usar ```ec2-user@IPV4``` , nao como tá no 1o link. Sempre lembrando que o IVP4 muda toda hora que a instancia é pausada.
4. Nao tem apt-get, tem que usar **yum**. Instalar o pip3 com isso, depois o git (```sudo yum install git-all```). Pra instalar o pip3: ```sudo yum -y install python3-pip```
5. Fazer clone do repo (nao precisa mais pq ja fiz), e dar pull no que tem la. Repo precisa estar publico pra isso
6. Na EC2, entrar na pasta do repo (```cd tcc-app```), rodar o streamlit, pegar o external url, e dale.
  
Pra deixar ele aberto sempre ler mais o post.

## Proximos passos ##
- Criar a lógica de calculo da GIDE, num arquivo `controller.py` (cujo nome é uma boa prática para
  centralizar as regras de negócio)
  >- Pra isso criar uma nova tabela, contendo as colunas de valores calculados;
  >- Adicionar classe no repository.py para comunicação com essa tabela;
  >- Adicionar os métodos de calculo no controller
  >- Adicionar novos endpoints na API para realizar o calculo
