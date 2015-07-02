#!/bin/sh
appname=$(basename `pwd`)
echo "creating docker image: $appname"
sudo docker build  --force-rm=true  --rm=true -t $appname .

DB_PASS=qazwsx
REDIS_PASS=plmokn
MONGODB_PASS=onepiece123
MONGODB_USER=$appname
MONGODB_DATABASE=$appname



mkdir -p ~/mysql_data
echo "starting mysql docker container"
docker stop $appname-mysql 
docker rm $appname-mysql
docker run --name $appname-mysql \
-v ~/mysql_data:/var/lib/mysql/ \
-e MYSQL_ROOT_PASSWORD=pwkdxydl \
-e MYSQL_DATABASE=$appname \
-e MYSQL_USER=$appname \
-e MYSQL_PASSWORD=$DB_PASS \
-d mysql:5.5


mkdir -p ~/mongo_data
echo "starting mongodb docker container"
cd docker/mongo
sudo docker build --rm=true -t $appname-mongo .
docker stop $appname-mongo
docker rm $appname-mongo
docker run --name $appname-mongo \
-p 27017:27017 \
-v ~/mongo_data:/data/db/ \
-e MONGODB_PASS=$MONGODB_PASS \
-e MONGODB_USER=$MONGODB_USER \
-e MONGODB_DATABASE=$MONGODB_DATABASE \
-d $appname-mongo 

cd ../../

echo "starting redis docker container"
docker stop $appname-redis
docker rm $appname-redis
docker run --name $appname-redis -d redis:2.8 redis-server --requirepass $REDIS_PASS

echo "starting webserver"
docker stop $appname
docker rm $appname
docker run --name $appname \
--link $appname-mysql:$appname-mysql \
--link $appname-redis:$appname-redis \
--link $appname-mongo:$appname-mongo \
-e DB_ENGINE=django.db.backends.mysql \
-e DB_NAME=$appname \
-e DB_USER=$appname \
-e DB_PASSWORD=$DB_PASS \
-e DB_HOST=$appname-mysql \
-e DB_PORT=3306 \
-e REDIS_LOCATION=$appname-redis:6379:0 \
-e REDIS_PASSWORD=$REDIS_PASS \
-e MONGO_HOST=$appname-mongo \
-e MONGO_PORT=27017 \
-e MONGO_USER=$MONGODB_USER \
-e MONGODB_DATABASE=$MONGODB_DATABASE \
-e MONGO_PASS=$MONGODB_PASS \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
-p 80:8000 \
-v `pwd`:/code \
-d $appname \
/bin/sh entrypoint.sh
