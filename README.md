## CASE - TWITTER 

Esta aplicação tem como finalidade consumir a API/V2 do Twitter pesquisando por termos ("hashtag") e inserir no banco de dados para consultas. No momento é possível inserir termos de forma dinâmica através da API da aplicação. Através desta API também é possível listar de forma dinâmica e separada os Tweet por "idioma/língua". Este ambiente foi desevolvido em cima do "Docker-Compose" e para seu desenvolvimento foi utilizado Python, Shell Script, Flask e MySQL. 

## Pré-Requisitos

Para o provisiomento deste ambiente é necessário que seu sistema operacional seja Linux, tenha Git e "Docker-Compose" instalado e configurado.

## Qual é a composição de microsserviços do "Docker-Compose"?

 - db_twitter - ("Bando de Dados")
 - loki - ("Logs Centralizados")
 - promtail - ("Agent responsável por coletar as saídas de logs dos containers")
 - grafana - ("Ferramenta utilizada para consultar os Logs através do EXPLORE")
 - api_rest_twitter - ("API responsável por inserir e/ou consultar os dados do banco")

## Configurar Ambiente

Para iniciar o ambiente é necessário clonar este reposório, acessar o diretório e executar o script:
```
git clone https://github.com/gustavoli1/api_rest_twitter.git
# cd api_rest_twitter
# ./setup.sh
```

## Como armazenar as #tag de forma dinâmica no banco através da API 

Para coletar e armazenar as mensagens na base de dados de forma dinâmica, basta executar este curl abaixo e substitur o valor de TAG para openbankig por exemplo.
```
curl http://localhost:5000/insert?hashtag=TAG
```

## Como consultar #tag armazenada através da API

Qual o total de postagens para cada uma das #tag por "idioma/língua" do usuário que postou:

```
curl http://localhost:5000/lang?hashtag=TAG
```

## STACK LOKI+PROMTAIL+GRAFANA - Consultar logs do ambiente e da aplicação.

Basta acessar o Grafana e utilizar o Explore para consultar os logs. Segue os dados do usuário de acesso ("user:admin" - "passwd:p0o9i8u7y6"). 

```
http://localhost:3000/explore
```
Para coletar os logs de saída de um container em específico, pode utilizar esta query por exemplo como demonstrado na url abaixo: {container_name="api_rest_twitter"}

```
http://localhost:3000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22refId%22:%22A%22,%22expr%22:%22%7Bcontainer_name%3D%5C%22api_rest_twitter%5C%22%7D%22%7D%5D
```

## Postman - Collection

Caso prefira utiliar o Postman é necessário importar o aquivo "Twitter - API.postman_collection" e ao utilizar o método GET inserir a "tag" no valor da chave hashtag.

