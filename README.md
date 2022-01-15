## API REST - TWITTER 

No momento este case segue em desenvolvimento com diversos pontos a melhorar, como implementação de métricas, gerencimaneto de secrets, serviços de mensagerias, melhorias no código, novas funcionalidades, além da arquitetura que precisa ser revista. Visto que precisa aumentar a confiabilidade e segurança do ambiente.

Esta aplicação tem como finalidade consumir a "API/V2" do Twitter pesquisando por termos ("hashtag") e inserir o retorno no banco. O formato de retorno dos dados do api_rest_twitter é em JSON.

O que é possível fazer com esta aplicação?

- Inserir tags de forma dinâmica no banco de dados através da api.
- Listar de forma dinâmica e separada os Tweet por "idioma/língua". 
- Consultar o total de postagens, agrupadas por hora do dia indepente da #hashtag.
- Consultar o total de postagens, agrupadas por hora do dia de forma dinâmica a #hashtag.

Este ambiente foi provisionado com "Docker-Compose" e para seu desenvolvimento foi utilizado Python, Shell Script, Flask e MySQL. 
Uma observação importante é que as secrets keys e tokens contidos nestes projeto estão públicos, porém, efêmeros com data prevista para se tornarem obsoletas.

## Pré-Requisitos

Para o provisiomento deste ambiente é necessário que seu sistema operacional seja Linux, tenha Git e "Docker-Compose" instalado e configurado.

## Configuração do Ambiente

Para iniciar o ambiente é necessário clonar este reposório, acessar o diretório e executar o script:
```
# git clone https://github.com/gustavoli1/api_rest_twitter.git
# cd api_rest_twitter
#./setup.sh
```

## Estrutura do Docker-Compose

 - db_twitter - ("Bando de Dados")
 - prometheus - ("Sistema de coleta de métricas de aplicações e serviços para armazenamento em timestamp")
 - loki - ("Centralizador de Logs")
 - promtail - ("Scrap coletor de saídas de logs")
 - grafana - ("Dashboard utilizado para consultar Logs com EXPLORE e métricas")
 - api_rest_twitter - ("Responsável por consumir a API do Twitter, inserir e consultar os dados do banco")

## Armazenando tag de forma dinâmica no banco através da API 

Para coletar e armazenar as mensagens na base de dados de forma dinâmica, basta executar este curl abaixo e substitur o valor da tag para openbankig por exemplo.
```
curl http://localhost:5000/insert?hashtag=TAG
```

O script abaixo coleta e armazena as mensagens na base de dados, para as seguintes tags: "#openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing". 

```
#./hashtags_insert.sh
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/print-insert.png)


## Como consultar tag armazenada através da API

Consultar o total de tweet por usuário para cada uma das #tag por "idioma/língua":

```
curl http://localhost:5000/tag_by_lang?hashtag=TAG
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/print-lang.png)


## LOGS da aplicação e do ambiente - STACK (LOKI+PROMTAIL+GRAFANA)

O Grafana é basicamente uma ferramenta que utliza de diversas fontes de dados para provisionar paíneis de métricas e LOGs. Nesta stack utlizaremos o LOKI como  centralizador de LOGs e utilizar o Explore do Grafana para consultar logs. 

Segue os dados de acesso: USER="admin" - PASSWD="p0o9i8u7y6".

[http://localhost:3000/explore](http://localhost:3000/explore)


Para coletar os logs de saída de um container em específico, pode utilizar os exemplos das query abaixo:
Exemplos de Query:

{container_name="api_rest_twitter"}

[Modelo de consulta](http://localhost:3000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22refId%22:%22A%22,%22expr%22:%22%7Bcontainer_name%3D%5C%22api_rest_twitter%5C%22%7D%22%7D%5D)

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/explore_1.png)

## Postman - Collection

Para utilizar Postman é necessário importar o aquivo "Twitter - API.postman_collection" e inserir o valor da "tag" na chave hashtag para inserir ou conultar o termo.

