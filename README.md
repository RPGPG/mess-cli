# mess-cli
Containerized messaging CLI app running on FastAPI and Redis with Python client

# Server installation
Just download docker-compose.yml and use
```
docker-compose up -d
```

# Client usage
```
./mess-cli.py -i or --init - create credentials file
./mess-cli.py -g or --get [username] - get conversation with specified user
./mess-cli.py -s or --send [username] ['some message'] - send message to user
./mess-cli.py -r or --register - create new account on server
```

Client is by default set to connect to http://localhost:8000 - it can be changed by setting address in srv variable in mess-cli.py

# Redis
Users and messages are stored as Redis hashes, users as user:[username], messages are grouped into conversations as m:[user1]@[user2].
Server uses SHA512 to store password hashes.
Base can be browsed by using
```
docker exec -it [redis_name] redis-cli
```
