## Ligando uma EC2:

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

## Pro RDS ##
Lançar ele na AWS, sem segredo nisso, único detalhe são as portas!
- Adicionar uma> {Type: All Traffic, Protocol: Vai automatico, Port Range: Vai automatico, Source: Anywhere}
Referência: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
