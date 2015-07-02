#!/bin/bash


if [ "$JOURNALING" == "no" ]; then
    mongod --storageEngine $STORAGE_ENGINE --smallfiles --nojournal &
else
    mongod --storageEngine $STORAGE_ENGINE --smallfiles &
fi



RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MongoDB service startup"
    sleep 5
    mongo $MONGODB_DATABASE --eval "help" >/dev/null 2>&1
    RET=$?
done

echo "=> Creating an user $MONGODB_USER  with  password ${MONGODB_PASS} in MongoDB $MONGODB_DATABASE"
mongo $MONGODB_DATABASE --eval "db.createUser({user: '$MONGODB_USER', pwd: '$MONGODB_PASS', roles:[{role:'dbOwner',db:'$MONGODB_DATABASE'}]});"
mongo $MONGODB_DATABASE --eval "db.createCollection('test')"

mongo admin --eval "db.shutdownServer();"

echo "=> Done!"
touch /data/db/.mongodb_password_set

echo "========================================================================"
echo "You can now connect to this MongoDB server using:"
echo ""
echo "    mongo $MONGODB_DATABASE -u admin -p $MONGODB_PASS --host <host> --port <port>"
echo ""
echo "Please remember to change the above password as soon as possible!"
echo "========================================================================"
