#!/bin/bash

hashtags=(openbanking remediation devops sre microservices observability oauth metrics logmonitoring opentracing)

for i in "${hashtags[@]}"

do
   :
   time curl "http://localhost:5000/insert?hashtag=$i"
   echo ""
   echo "####################   Hashtag $i inserida com sucesso na base de dados!   ###########################"
   sleep 2
done
