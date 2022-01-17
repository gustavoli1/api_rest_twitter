## API REST - TWITTER 

No momento este case segue em desenvolvimento com diversos pontos a melhorar, como implementação de métricas, gerencimaneto de secrets, serviços de mensagerias, melhorias no código, novas funcionalidades, além da arquitetura que precisa ser revista. Visto que precisa aumentar a confiabilidade e segurança do ambiente.

Esta aplicação tem como finalidade consumir a API do Twitter pesquisando por termos ("hashtag") e inserir o retorno no banco. O formato de retorno dos dados do api_rest_twitter é em JSON.

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


## Logs de aplicação e de ambiente

Nesta Stack utilizaremos Loki como centralizador de logs, Promtail para fazer o scrap de logs do container e da aplicação, e o Grafana para consultar logs através do Explore. 

Segue os dados de acesso ao Grafana: USER="admin" - PASSWD="p0o9i8u7y6".

[http://localhost:3000/explore](http://localhost:3000/explore)


Para gerar dados e insumos no Grafana, para obter métricas e logs  por gentileza rode este comando abaixo em seu terminal; este comando faz um loop de 5 minutos batendo na API simulando algumas chamadas.
```
# START=`date +%s`;time while [ $(( $(date +%s) - 300 )) -lt $START ]; do curl "http://localhost:5000/{insert?hashtag=metrics,group_by_hour,group_by_hour_tag?hashtag=error,tag_by_lang?hashtag=metrics}"; done
```


Para coletar os logs de saída de um container em específico, utilizaremos o LogQL para fazer query no Loki.


Consultar saída padrão de logs do stdout, contagem de erros com intervalos de tempo de 1h:
```
count_over_time({stream="stdout"} |= "error" [1h])
```

Retornar todas as linhas de log para o container "api_rest_twitter":
```
{container_name="api_rest_twitter"}
```

Consultar linhas de logs que contenham erro no container da aplicação:
```
{container_name="api_rest_twitter"} |= "error"
```

Consultar linhas de logs incluindo o texto "error" ou "info" usando regex no stdout:
```
{stream="stdout"} |~ "error|info"
```

Consultar linhas de logs que contenham exceções:
```
{container_name="api_rest_twitter"} |= "exception" 
```

Consultar linhas de logs que tiverem erro, exceto o que tiverem timeout:
```
{container_name="api_rest_twitter"} |= "error" != "timeout"
```

Consultar logs excluíndo "/metrics"
```
{container_name="api_rest_twitter"} != "/metrics"
```


[Modelo de consulta](http://localhost:3000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22refId%22:%22A%22,%22expr%22:%22%7Bcontainer_name%3D%5C%22api_rest_twitter%5C%22%7D%22%7D%5D)

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/explore_2.png)

## Postman - Collection

Para utilizar Postman é necessário importar o aquivo "Twitter - API.postman_collection" e inserir o valor da "tag" na chave hashtag para inserir ou conultar o termo.

