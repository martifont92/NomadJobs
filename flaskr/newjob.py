from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flaskr.models import User
from flaskr import db

newjob = Blueprint('newjob', __name__)

@newjob.route('/jobpost')
def jobpost():
    return render_template('jobpost.html')