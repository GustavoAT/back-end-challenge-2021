# Back-end Challenge 🏅 2021

Este projeto consiste em uma API REST onde é possível fazer operações de CRUD na classe usuário. Também implementa uma atualização automática de usuários obtidos na API [randomuser](https://randomuser.me/).

Desenvolvido com:
 * Python
 * FastAPI
 * SQLAlchemy
 * MySQL
 * Docker

## Desafio
Este é um desafio para testar conhecimentos em Back-end da Coodesh.
Repositório original: [back-end-challenge-2021](https://lab.coodesh.com/public-challenges/back-end-challenge-2021.git)



## Instalação e uso
Edite as variáveis de ambiente conforme a necessidade em `app/settingsexample.py` e renomeie o arquivo para `settings.py`.
  ### Sem docker
  Use um ambiente virtual, ex.(linux):
  `python -m venv /envs/meuvenv && source /envs/meuvenv/bin/activate`
  
  Instale os requisitos:
  `pip install -r requirements.txt`

  Certifique-se de configurar o url do banco de dados em `app/settingsexample.py` e que o banco esteja rodando. Também pode usar sqlite.

  Crie as tabelas no banco de dados no primeiro uso:
  `python -m app.persistence.models createtables`

  Inicie o uvicorn:
  `uvicorn app.main:app --reload`
  o `--reload` permite que você edite o código sem precisar reiniciar o servidor, as alterações já serão carregadas.

  ### Com Docker
  Certifique-se de configurar o url do banco de dados em `app/settingsexample.py` e que o banco esteja rodando. Também pode usar sqlite.
  
  Crie a imagem:
  `sudo docker build --rm -t imagename .`

  Rode o container:
  `sudo docker run -d -p 80:80 --name containername imagename`

  Crie as tabelas no banco de dados no primeiro uso:
  `sudo docker exec containername python -m app.persistence.models createtables`

  ### Com Docker Compose (recomendado)
  Certifique-se de configurar o url do banco de dados em `app/settingsexample.py` o host como 'db' (o nome do serviço do banco de dados no arquivo docker-compose.yml)
  
  Crie e rode os serviços com:
  `sudo docker-compose up -d`

  Crie as tabelas no banco de dados no primeiro uso:
  `sudo docker-compose exec app python -m app.persistence.models createtables`

  ### Cron
  Se rodando em conteiner, vai ser instalado cron e crontab. Se não desejar usar, remova as linhas referentes ao cron no Dockerfile.
  
  Para que o cron funcione corretamente, é preciso gerar um registro sobre a paginação para consumo do randomuser.
  Ex.:`sudo docker-compose exec app python -m app.apiclient.randomuser initpag 10 100`
  Para serem buscados e inseridos 100 usuários de 10 em 10, ou seja, 10 usuários cada vez que o cron executar o script.
  O crontab está configurado para todo dia às 08:00.
  Você pode verificar o log deste script em `/var/log/cron.log` dentro do conteiner.


Este é um challenge by coodesh.