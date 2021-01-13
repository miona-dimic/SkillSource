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

## Get all users from database (GET request) http://localhost:5000/user

    curl -H 'Accept: application/json' http://localhost:5000/user

## Get all jobs from database (GET request) http://localhost:5000/jobs

    curl -GET 'Accept: application/json' http://localhost:5000/jobs

## Get user together with his skills from database (GET request) http://localhost:5000/user/id
    public id from user is sent within request
    example:
         curl -GET 'Accept: application/json' http://localhost:5000/user/7d06935a-56ef-4499-be7e-77445f544a11
    
## check data in database
    sqlite3 database.db
    sqlite> .tables
    sqlite> .header on
    sqlite> select * from user;
    sqlite> select * from organisation;
    sqlite> select * from job;
    sqlite> select * from skill;
    sqlite> select * from jobs_skills;
    sqlite> select * from  individual_skill;
    sqlite> select * from users_skills;



    

