import os
import random

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask.globals import request
from flask.helpers import url_for
from flask.json import jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()


class User(db.Model):
    """ User model to store users which will be allowed to use the API"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=12)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


class RegistrationForm(FlaskForm):
    """ Simple registration form """
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


@app.route('/', methods=['GET', 'POST'])
def register():
    """ View for registering users via UI"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        return redirect(url_for('success'))
    return render_template('register.html', form=form)


@app.route('/sucess')
def success():
    return render_template('success.html')

# mocked outputs - for start
MOCKS = [{"fingers": [0, 0, 2, 4, 1, 3],
          "caged": "E",
          "chord_names": ["Emaj", "G#m(b13)", "Badd11", "Eb+sus(b9)"],
          "voicing": "drop 2",
          "greene_voicing": "V-2"},
         {"fingers": [0, 1, 4, 2, 3, 0],
          "caged": "C",
          "chord_names": ["C7", "E#m(b13)", "Badd13"],
          "voicing": "drop 3",
          "greene_voicing": "V-2"},
         {"fingers": [0, 1, 3, 2, 0, 0],
          "caged": "A",
          "chord_names": ["Amin", "B#m(b13)"],
          "voicing": "drop 2",
          "greene_voicing": None}
         ]


# simple 'hello world' for the sake of test
# TODO - remove before deploy
@app.route('/hello')
def hello_world():
    return 'Hello World!'


@auth.verify_password
def verify_password(email, password):
    if email and password:
        user = User.query.filter_by(email=email).first()
    if not user:
        return False
    return user.verify_password(password)


# basic api method for getting frets
@app.route('/api/v1/frets/', methods=['POST'])
@auth.login_required
def frets():
    # get the data
    data = request.json
    # validate it
    validate_frets_input(data)
    # create the output
    output = calculate_output(data)
    return output


def validate_frets_input(data):
    """ Validates that input contains frets as an 6-integers array"""
    if data and 'frets' in data:
        _frets = data['frets']
        # check that frets values are packed into array
        if not type(_frets) == list:
            raise BadRequest(
                'Invalid frets. You should provide a 6-elements array')
        # must be 6 values (integers)
        if len(_frets) != 6:
            raise BadRequest('Invalid frets. You should provide 6 values')
        for f in _frets:
            try:
                int(f)
            except ValueError:
                raise BadRequest('Inputted frets must be integers')
    else:
        raise BadRequest('Input data is invalid. No frets provided.')


def calculate_output(data):
    """ Function for creating an output for each request. Will be mocked up
        for a while
    """
    return jsonify(random.choice(MOCKS))


if __name__ == '__main__':
    app.run()
