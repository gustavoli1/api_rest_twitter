## API REST - TWITTER 

Esta aplicação tem como finalidade consumir a API do Twitter, pesquisando por termos ("hashtag") e inserindo os retornos no banco de dados. O formato de retorno da api_rest_twitter é em JSON. No momento, este projeto segue em desenvolvimento.

O que é possível fazer com esta aplicação?

- Inserir tags de forma dinâmica no banco de dados através da API.
- Listar de forma dinâmica e separada os Tweets por "idioma/língua". 
- Consultar o total de postagens, agrupadas por hora do dia, independente da #hashtag.
- Consultar o total de postagens, agrupadas por hora do dia, de forma dinâmica através de qualquer #hashtag.

Este ambiente foi provisionado com o "Docker-Compose" e para seu desenvolvimento foi utilizado Python, Shell Script, Flask e MySQL. 
Uma observação importante é que as "Secrets Keys" e "Tokens" contidos neste projeto estão públicos, porém, efêmeros com data prevista para se tornarem obsoletos.

## Pré-Requisitos

Para o provisionamento deste ambiente é necessário sistema operacional Linux ("Debian-Like"), Git e "Docker-Compose" instalados e configurados corretamente.

## Configuração do Ambiente

Para iniciar o ambiente é necessário clonar este reposório, acessar o diretório e executar o script:
```
# git clone https://github.com/gustavoli1/api_rest_twitter.git
# cd api_rest_twitter
#./setup.sh
```

## Estrutura do Docker-Compose

 - db_twitter - ("Banco de Dados")
 - prometheus - ("Sistema de coleta de métricas de aplicações e serviços para armazenamento em timestamp")
 - loki - ("Centralizador de Logs")
 - promtail - ("Scrap coletor de saídas de logs")
 - grafana - ("Dashboard utilizado para consultar Logs com EXPLORE e métricas")
 - api_rest_twitter - ("Responsável por consumir a API do Twitter, inserir e consultar os dados do banco")

## Armazena tag de forma dinâmica no banco através da API 

Para coletar e armazenar as mensagens na base de dados, basta executar este curl abaixo e substituir o valor da string "TAG" para qualquer palavra desejada, como por exemplo: "openbankig".
```
curl http://localhost:5000/insert?hashtag=TAG
```

O script abaixo coleta e armazena as mensagens na base de dados, para as seguintes tags: "#openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing". 

```
#./hashtags_insert.sh
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/insert.png)


## Como consultar uma tag no banco de dados, através da API, classificando por idioma/língua

Consultar o total de tweet por idioma/ língua, de cada #Hashtag, sendo necessária apenas a substituição da string TAG:

```
curl http://localhost:5000/tag_by_lang?hashtag=TAG
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/tag_by_lang.png)


## Como consultar o total de postagens

Consultar o total de tweet agrupados por hora do dia, independente da #hashtag:

```
curl http://localhost:5000/group_by_hour
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/group_by_hour.png)


Consultar o total de tweet de #hashtag específica, agrupado por hora do dia, substutíndo a string "TAG":

```
curl http://localhost:5000/group_by_hour_tag?hashtag=TAG
```

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/group_by_hour_tag.png)


## Métricas de aplicação e de ambiente

Nesta Stack utilizaremos Prometheus como nosso banco de dados timestamp, Node-Exporter para coletar as métricas do container e Prometheus-Flask-Exporter, que foi instrumento na aplicação para coletar dados de métricas mais precisos.

[http://localhost:3000/?orgId=1](http://localhost:3000/explore)

Segue os dados de acesso ao Grafana: USER="admin" - PASSWD="p0o9i8u7y6".

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/metrics_2.png)

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/metrics.png)

Para gerar dados e insumos no Prometheus, por gentileza, rodar este comando abaixo em seu terminal. Este comando fará um loop de 5 minutos simulando algumas chamadas na API.
```
# START=`date +%s`;time while [ $(( $(date +%s) - 300 )) -lt $START ]; do curl "http://localhost:5000/{insert?hashtag=metrics,group_by_hour,group_by_hour_tag?hashtag=error,tag_by_lang?hashtag=metrics}"; done
```



Para coletar as métricas de saída, será utilizado o PromQL para fazer query no Prometheus.


Total de Requests por Minuto:
```
increase(flask_http_request_total{status="200"}[1m])
```


Quantidade de Erros - API Rest Twitter:
```
increase(flask_http_request_total{status!="200"}[1m])
```


Latência - Tempo de Execução:
```
rate(flask_http_request_duration_seconds_sum{status="200"}[1m])
/
rate(flask_http_request_duration_seconds_count{status="200"}[1m])
```


Container - Consumo de CPU
```
rate(process_cpu_seconds_total{job="services",instance="api_rest_twitter:5000"}[1m])
```


Container - Consumo de Memória
```
process_resident_memory_bytes{job="services",instance="api_rest_twitter:5000"}
```


Container - Tráfego de Rede
```
node_network_receive_bytes{device="eth0", instance="api_rest_twitter:9100", job="services"}
```


## Logs de aplicação e de ambiente

Nesta Stack utilizaremos Loki como centralizador de logs, Promtail para fazer o scrap de logs do container e da aplicação e o Grafana para consultar logs através do Explore. 

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/error_log.png)

Segue os dados de acesso ao Grafana: USER="admin" - PASSWD="p0o9i8u7y6".

[http://localhost:3000/explore](http://localhost:3000/explore)


Para gerar dados e insumos no Loki, por gentileza rodar este comando abaixo em seu terminal. Este comando fará um loop de 5 minutos simulando algumas chamadas na API.
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

![Example dashboard](https://github.com/gustavoli1/api_rest_twitter/blob/main/images/explore_2.png)

## Postman - Collection

Para utilizar Postman é necessário importar o aquivo "Twitter - API.postman_collection" e inserir o valor da "tag" na chave hashtag para inserir ou consultar o termo.

