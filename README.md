## CASE - TWITTER 

No momento este case segue em desenvolvimento com diversos pontos a melhorar, como implementação de métricas, gerencimaneto de secrets, serviços de mensagerias, melhorias no código, novas funcionalidades, além da arquitetura que precisa ser revista. Visto que precisa aumentar a confiabilidade e segurança do ambiente.

Esta aplicação tem como finalidade consumir a "API/V2" do Twitter pesquisando por termos ("hashtag") e inserir o retorno dos dados no banco. No momento é possível inserir tags de forma dinâmica através da aplicação, também é possível listar de forma dinâmica e separada os Tweet por "idioma/língua". 

Este ambiente foi provisionado com "Docker-Compose" e para seu desenvolvimento foi utilizado Python, Shell Script, Flask e MySQL. 
Uma observação importante é que as secrets keys e tokens contidos nestes projeto estão públicos, porém, efêmeros com data prevista para se tornarem obsoletas.

## Pré-Requisitos

Para o provisiomento deste ambiente é necessário que seu sistema operacional seja Linux, tenha Git e "Docker-Compose" instalado e configurado.

## Composição do Docker-Compose

 - db_twitter - ("Bando de Dados")
 - loki - ("Logs Centralizados")
 - promtail - ("Agent responsável por coletar as saídas de logs dos containers")
 - grafana - ("Ferramenta utilizada para consultar os Logs através do EXPLORE")
 - api_rest_twitter - ("API responsável por inserir e/ou consultar os dados do banco")

## Configuração do Ambiente

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

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/print-insert.png)


## Como consultar #tag armazenada através da API

Consultar o total de tweet por usuário para cada uma das #tag por "idioma/língua":

```
curl http://localhost:5000/lang?hashtag=TAG
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/print-lang.png)


## LOGS do ambiente e da API - STACK (LOKI+PROMTAIL+GRAFANA)

O Grafana é basicamente uma ferramenta que utliza de diversas fontes de dados para provisionar paíneis de métricas e LOGs. Nesta stack utlizaremos o LOKI como  centralizador de LOGs e utilizar o Explore do Grafana para consultar logs. 

Segue os dados de acesso ("USER=admin" - "PASSWD=p0o9i8u7y6").

[http://localhost:3000/explore](http://localhost:3000/explore)


Para coletar os logs de saída de um container em específico, pode utilizar como exemplo esta query {container_name="api_rest_twitter"} como demonstrado nesta URL: 

[http://localhost:3000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22refId%22:%22A%22,%22expr%22:%22%7Bcontainer_name%3D%5C%22api_rest_twitter%5C%22%7D%22%7D%5D](http://localhost:3000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22refId%22:%22A%22,%22expr%22:%22%7Bcontainer_name%3D%5C%22api_rest_twitter%5C%22%7D%22%7D%5D)

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/explore_1.png)

## Postman - Collection

Para utilizar Postman é necessário importar o aquivo "Twitter - API.postman_collection" e inserir o valor da "tag" na chave hashtag para encontrar o termo.

