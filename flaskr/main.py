from flask import Blueprint, render_template, request, redirect, request
from .models import db, Job

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
	jobs = Job.query.order_by(Job.created).all()
	return render_template('index.html', jobs=jobs)

@main.route('/thanks')
def thanks():
    return render_template('thanks.html')

@main.route('/details/<int:id>', methods=['GET'])
def details(id):
	details = Job.query.get_or_404(id)
	return render_template('details.html', details=details)

