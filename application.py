from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AppkeyX'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Models
job_skills = db.Table('jobs_skills',
                      db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
                      db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')))

class Organisation (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    jobs = db.relationship('Job', backref='organisation', lazy='dynamic')

class Job (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(3000))
    image = db.Column(db.String(200))
    category = db.Column(db.String(100))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    skills = db.relationship('Skill', secondary=job_skills,
                             backref=db.backref('jobs'), lazy='dynamic')

class Skill (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(100), unique=True)
    skills = db.relationship('IndividualSkill', foreign_keys='IndividualSkill.user_id', backref=db.backref('users'), lazy='dynamic')

class IndividualSkill (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill = db.relationship('Skill')
    rating = db.Column(db.String(100))
    change = db.Column(db.String(100))
    # users = db.relationship('User', foreign_keys='IndividualSkill.user_id', backref=db.backref('skills', lazy='dynamic'))

@app.route('/jobs', methods=['GET'])
@cross_origin()
def get_jobs():
    jobs = Job.query.all()
    output = []
    for job in jobs:
        skills = []
        for skill in job.skills.all():
            skills.append({
                'id': skill.id,
                'name': skill.name
            })
        output.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'image': job.image,
            'category': job.category,
            'organisation_id': job.organisation_id,
            'skills': skills
        })
    return jsonify({'job': output})


@app.route('/user', methods=['GET'])
@cross_origin()
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'email': user.email,
            'name': user.name,
            'username': user.username,
            'password': user.password
        })
    return jsonify({'users': output})

@app.route('/user/<id>', methods=['GET'])
@cross_origin()
def get_user(id):
    user = User.query.filter_by(public_id=id).first()
    if not user:
        return make_response(
            'Not Found',
            404
        )
        
    skills = []
    for skill in user.skills.all():
        skills.append({
            'id': skill.id,
            'skill_id': skill.skill_id,
            'skill_name': skill.skill.name,
            'rating': skill.rating,
            'change': skill.change
        })

    output = {
        'public_id': user.public_id,
        'email': user.email,
        'name': user.name,
        'username': user.username,
        'skills': skills
    }

    return jsonify({'user': output})

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    logreq = request.form

    if not logreq or not logreq.get('username') or not logreq.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query .filter_by(username=logreq.get('username')) .first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, logreq.get('password')):
        return make_response('Successfull log in. Welcome ' + user.name + '! ', 201)

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.form

    name, username = data.get('name'), data.get('username')
    password = data.get('password')
    email = data.get('email')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


if __name__ == "__main__":
    app.run(debug=True)