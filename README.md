## SkillSource
## In terminal change current directory to SkillSource folder
    cd path../SkillSource
## create virtual environment
    python3 -m venv env

## activate the virtual enviornment:
    source env/bin/activate
    Note: If you are on windows then it would be Scripts instead of bin

## install the libraries:
    pip install -r requirements.txt

## create database
    python createData.py

## start testing api
    python application.py

## api should be running on http://localhost:5000/

[do in separate terminal]:

## SignUp (POST request) http://localhost:5000/signup 

    required data for registration: name, email, username and password
    this can be tested by typing the folowing command in terminal:
        curl -X POST --data "username=john_doe" --data "password=123" --data "name=John Doe" --data "email=jon.doe@example.com" http://localhost:5000/signup

## LogIn (POST request) http://localhost:5000/login

    required data for logIn: username and password
    this can be tested by typing the folowing command in terminal:
        curl -X POST --data "username=john_doe" --data "password=123" http://localhost:5000/login
        #with successfull logIn access token is returned
    
    to initialize token immediately (to avoid multiple copy-paste in the future)
        TOKEN=$(curl -X POST --data "username=john_doe" --data "password=123" http://localhost:5000/login | jq -r '.token')

## Get all users from database (GET request) http://localhost:5000/user

    only possible for authorized users (with access token)
    curl -H 'Accept: application/json' -H "x-access-token: ${TOKEN}" http://localhost:5000/user

## check data in database
    sqlite3 database.db
    sqlite> .tables
    sqlite> select * from user;

## try