from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Job(db.Model):
    #About the job
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    created = db.Column(db.DateTime(), default = datetime.datetime.utcnow)
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
    file = db.Column(db.String(64), nullable=False, default='default.png')
    filePath = db.Column(db.String(264), nullable=True) #absolute path to file
    hq = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    companyDescription = db.Column(db.Text(), nullable=False)

    @classmethod
    def delete_expired(id):
        expiration_days = 1
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        id.query.filter(id.created < limit).delete()
        db.session.commit()

def delete_expired_jobs():
    Job.delete_expired()