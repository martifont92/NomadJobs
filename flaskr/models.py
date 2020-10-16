from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Job(db.Model):
    #About the job
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    created = db.Column(db.DateTime(), default = datetime.utcnow)
    active = db.Column(db.Integer(), default = 1)
    position = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    jobType = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    howApply = db.Column(db.String(100), nullable=False)
    jobDescription = db.Column(db.Text(), nullable=False)
    #About the company
    companyName = db.Column(db.String(100), nullable=False)
    #logo  
    hq = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    companyDescription = db.Column(db.Text(), nullable=False)