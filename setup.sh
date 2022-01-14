#!/bin/bash

echo "######################## Inicializando o Ambiente ##########################"

service docker stop

cp config/daemon.json /etc/docker/daemon.json

service docker start

docker-compose up -d

docker-compose ps

sleep 30

docker exec -i db_twitter sh -c 'exec mysql -utwitter_user -pp0o9i8u7y6 twitter_db << EOF 
create table twitter_db (author varchar(280), created_at varchar(280), text text, id varchar(280), author_id varchar(280), lang varchar(5), hashtag varchar(280)); 
EOF'



