#!/usr/bin/python3

import requests
import sys
import os


srv = "http://localhost:8000"
cred_dir = os.path.expanduser("~/.mess-cli/")


def get_creds():
    try:
        f = open(os.path.join(cred_dir, "cred"), "r")
    except:
        print("No credentials found. Do --init first.")
        exit()
    creds = []
    raw_creds = f.readlines()
    f.close()
    creds.append(raw_creds[0].strip())
    creds.append(raw_creds[1].strip())
    return creds


def get_conv(srv, username, password, another_user):
    try:
        raw_conversation = requests.get(f"{srv}/G:{username}:{password}:{another_user}")
    except:
        print("Cannot connect to server. Set srv variable in this file to server address.")
        exit()
    try:
        raw_conversation = raw_conversation.json()
        for key, value in raw_conversation.items():
            print(f"{key} --- {value}")
    except:
        print(raw_conversation)


def send(srv, username, password, another_user, message):
    try:
        raw_conversation = requests.get(f"{srv}/S:{username}:{password}:{another_user}:{message}")
    except:
        print("Cannot connect to server. Set srv variable in this file to server address.")
        exit()
    try:
        raw_conversation = raw_conversation.json()
        for key, value in raw_conversation.items():
            print(f"{key} --- {value}")
    except:
        try:
            print(raw_conversation.text)
        except:
            print(raw_conversation)


def register(srv, username, password):
    try:
        register_result = requests.get(f"{srv}/R:{username}:{password}")
    except:
        print("Cannot connect to server. Set srv variable in this file to server address.")
        exit()
    try:
        print(register_result.text)
    except:
        print(register_result)


if len(sys.argv) == 1:
    print("Usage:")
    print("-i or --init - create credentials file")
    print("-g or --get [username] - get conversation with specified user")
    print("-s or --send [username] ['some message'] - send message to user")
    print("-r or --register - create new account on server")
    exit()

if sys.argv[1] == "-i" or sys.argv[1] == "--init":
    try:
        os.mkdir(cred_dir, 0o700)
    except:
        pass
    f = open(os.path.join(cred_dir, "cred"), "w")
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()
    f.write(f"{username}\n{password}\n")
    f.close()
    exit()

if (sys.argv[1] == "-g" or sys.argv[1] == "--get") and len(sys.argv) == 3:
    username = get_creds()[0]
    password = get_creds()[1]
    get_conv(srv, username, password, sys.argv[2])
    exit()

if sys.argv[1] == "-s" or sys.argv[1] == "--send":
    if len(sys.argv) != 4:
        print("Usage:")
        print("-s or --send [username] ['some message'] - send message to user")
        print("Enclose message in '' to use multiple words.")
        exit()
    username = get_creds()[0]
    password = get_creds()[1]
    send(srv, username, password, sys.argv[2], sys.argv[3])
    exit()

if sys.argv[1] == "-r" or sys.argv[1] == "--register":
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()
    print("Input password again: ")
    password2 = input()
    if password != password2:
        print("Passwords do not match.")
        exit()
    register(srv, username, password)
    exit()


