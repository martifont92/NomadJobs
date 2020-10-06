from flask import Flask, render_template, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # STRIPE
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_T7FKDbqcVOQByT6Cl6YBgPFj00y52ZO2hb'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_uLduAGXEEL228gykOuUPktgu00sQrbP8KM'
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

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

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .newjob import newjob as newjob_blueprint
    app.register_blueprint(newjob_blueprint)

    return app