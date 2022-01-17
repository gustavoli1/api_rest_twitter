#!/bin/bash

echo "######################## Inicializando o Ambiente ###########################"
echo ""
echo ""
echo "######################## Parando Serviço do Docker ##########################"
service docker stop
echo ""
echo "############ Copiando os Parâmetros de configurações do Docker ##############"
cp config/daemon.json /etc/docker/daemon.json
echo ""
echo "###################### Inicializando Serviço do Docker ######################"
echo ""
service docker start
echo ""
echo "################### Provisionando - API_REST_TWITTER # ######################"
docker-compose up -d
echo ""
echo "########################### Status dos Componentes ##########################"
docker-compose ps
echo ""
echo "#################### Aguardando 30 Segundos #################################"
sleep 30
echo ""
echo "################## Estrutura da Tabela do Banco de Dados ####################"
docker exec -i db_twitter sh -c 'exec mysql -utwitter_user -pp0o9i8u7y6 twitter_db << EOF 
create table twitter_db (author varchar(280), created_at varchar(280), text text, id varchar(280), author_id varchar(280), lang varchar(5), hashtag varchar(280)); 
EOF'
echo ""
echo ""
echo "#############################################################################"
echo "######################### Ambiente Provisionado #############################"
echo "#############################################################################"
echo ""
echo ""
