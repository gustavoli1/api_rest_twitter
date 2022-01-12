#!/bin/bash
echo "######################## Inicializando o Ambiente ##########################"
docker-compose up -d

sleep 30

docker exec -i db_twitter sh -c 'exec mysql -utwitter_user -pp0o9i8u7y6 twitter_db << EOF 
create table twitter_db (author varchar(280), created_at varchar(280), text text, id varchar(280), author_id varchar(280), lang varchar(5), hashtag varchar(280)); 
EOF'

docker-compose ps

