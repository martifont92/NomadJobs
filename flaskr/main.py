from flask import Blueprint, render_template, request, redirect, request, url_for
from .models import db, Job
from sqlalchemy import desc

import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET','POST'])
def index():
	'''
	expiration_days = 1
	limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
	Job.query.filter(Job.created < limit).delete()
	db.session.commit()
	'''
	jobs = Job.query.filter_by(active=1).order_by(desc(Job.created)).all()
	return render_template('index.html', jobs=jobs)

@main.route('/thanks')
def thanks():
    return render_template('thanks.html')

@main.route('/details/<int:id>', methods=['GET'])
def details(id):
	details = Job.query.get_or_404(id)
	return render_template('details.html', details=details)

@main.route('/category/<string:category>', methods=['GET'])
def category(category):
	jobs = Job.query.order_by(desc(Job.created)).filter_by(category=category).all()
	return render_template('category.html', jobs=jobs, category=category)

