import os
from flask import Flask, render_template, url_for, request, abort, redirect
from datetime import datetime
import stripe
from .models import db, Job
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = ('pdf', 'png', 'jpg', 'jpeg', 'gif')
UPLOAD_FOLDER = '/Users/martifont/dev/nomadjobs/flaskr/static/uploads'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    db.init_app(app)

    # STRIPE
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_T7FKDbqcVOQByT6Cl6YBgPFj00y52ZO2hb'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_uLduAGXEEL228gykOuUPktgu00sQrbP8KM'
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    # Job
    @app.route('/jobpost')
    def jobpost():
        return render_template('jobpost.html')

    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/jobpost', methods=['POST'])
    def jobpost_post():
        with app.app_context():
            #About the job
            position = request.form.get('position')
            category = request.form.get('category')
            jobType = request.form.get('jobType')
            region = request.form.get('region')
            salary = request.form.get('salary')
            howApply = request.form.get('howApply')
            jobDescription = request.form.get('jobDescription')
            #About the company
            companyName = request.form.get('companyName')
            hq = request.form.get('hq')
            email = request.form.get('email')
            companyDescription = request.form.get('companyDescription')

            file = request.files['file']
            if file.filename == '':
                filename = 'default.png'
            if file and allowed_file(file.filename):
                filename = secure_filename(str(uuid.uuid4()))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_job = Job(
                position = position,
                category = category,
                jobType = jobType,
                region  = region,
                salary = salary,
                howApply = howApply,
                jobDescription = jobDescription,
                companyName = companyName,
                hq = hq,
                email = email,
                file = filename,
                filePath = os.path.abspath('static/uploads/'),
                companyDescription = companyDescription
                )
            db.session.add(new_job)
            db.session.commit()
        return redirect(url_for('main.index'))
    # end Job

    # STRIPE
    @app.route('/stripe_pay')
    def stripe_pay():
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1HZGvRJWJOgWGYPVjgNnxL0Z',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('main.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('main.index', _external=True),
        )
        return {
            'checkout_session_id': session['id'], 
            'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
        }
    
    @app.route('/stripe_webhook', methods=['POST'])
    def stripe_webhook():
        print('WEBHOOK CALLED')
        if request.content_length > 1024 * 1024:
            print('REQUEST TOO BIG')
            abort(400)
        payload = request.get_data()
        sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = 'whsec_x44cnUqgqhLMtRGmd5MUo0YTsC5YBIYS'
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            print('INVALID PAYLOAD')
            return {}, 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print('INVALID SIGNATURE')
            return {}, 400

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print(session)
            line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
            print(line_items['data'][0]['description'])
        return {}
    # end STRIPE


    # Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app