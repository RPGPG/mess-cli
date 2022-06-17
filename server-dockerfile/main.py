from fastapi import FastAPI
import redis
import datetime
import hashlib


try:
    r = redis.Redis(host='mess-cli-redis', port=6379, db=0)
    r.ping()
except redis.exceptions.ConnectionError:
    print("Error connecting to redis.")
    quit()
app = FastAPI()


@app.get("/")
async def root():
    return "pong"

@app.get("/G:{username}:{password}:{another_user}")
async def get_messages(username, password, another_user):
    try:
        password_from_db = r.hget(f'user:{username}', "password")
        pass_hash = hashlib.new('sha512')
        pass_hash.update(password.encode('ascii'))
        if pass_hash.digest() == password_from_db:
            if not redis_check(f"user:{another_user}"):
                return f"User {another_user} does not exist."
            conversation_name = assemble_conv_name(username, another_user)
            return get_conv(conversation_name)
        else:
            return f"Passwords do not match."
    except redis.exceptions.ConnectionError:
        return "Error connecting to redis."

@app.get("/S:{username}:{password}:{another_user}:{message}")
async def send_message(username, password, another_user, message):
    try:
        password_from_db = r.hget(f'user:{username}', "password")
        pass_hash = hashlib.new('sha512')
        pass_hash.update(password.encode('ascii'))
        if pass_hash.digest() == password_from_db:
            if username == another_user:
                return "You can't message yourself."
            if not redis_check(f"user:{another_user}"):
                return f"User {another_user} does not exist."
            conversation_name = assemble_conv_name(username, another_user)
            return send(conversation_name, username, another_user, message)
        else:
            return f"Passwords do not match."
    except redis.exceptions.ConnectionError:
        return "Error connecting to redis."

@app.get("/R:{username}:{password}")
async def register_user(username, password):
    try:
        user_exists = redis_check(f"user:{username}")
        if user_exists:
            return f"User {username} already exists."
        return register(username, password)
    except redis.exceptions.ConnectionError:
        return "Error connecting to redis."


def redis_check(somekey):
    return r.exists(somekey)

def assemble_conv_name(username, another_user):
    alphabetical_usernames = [username, another_user]
    alphabetical_usernames.sort()
    conversation_name = f"m:{alphabetical_usernames[0]}@{alphabetical_usernames[1]}"
    return conversation_name

def get_conv(conversation_name):
    if redis_check(conversation_name):
        conversation = r.hgetall(conversation_name)
        return conversation
    else:
        return "No conversations."

def send(conversation_name, username, another_user, message):
    mtime = datetime.datetime.now()
    mtime = mtime.strftime("%y-%m-%d %H:%M")
    if redis_check(conversation_name):
        conversation_length = int(r.hlen(conversation_name))
        r.hset(conversation_name, f"{conversation_length + 1} / {mtime} / {username}", message)
        return get_conv(conversation_name)
    else:
        r.hset(conversation_name, f"1 / {mtime} / {username}", message)
        return get_conv(conversation_name)


def register(username, password):
    user_is_alphanumeric = username.isalnum()
    pass_is_alphanumeric = password.isalnum()
    if user_is_alphanumeric and pass_is_alphanumeric:
        pass_hash = hashlib.new('sha512')
        pass_hash.update(password.encode('ascii'))
        r.hset(f"user:{username}", "username", username)
        r.hset(f"user:{username}", "password", pass_hash.digest())
        return "User created."
    else:
        return "Username and password must be alphanumeric. (aA-zZ, 0-9)"

