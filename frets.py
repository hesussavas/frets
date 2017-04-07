import os
import random

import sys
import traceback

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

from utils.fingering_rules import predict_fingering
from utils.identify import identify, idntf
from utils.utilities import greene_table

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
    output = calculate_output(data['frets'])
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
    """ Function for creating an output for each request. """
    output = dict()
    output['chord_names'] = _get_chord_names(data)
    output['fingers'] = _get_fingers(data)
    output['greene_voicing'] = _get_greene_voicing(data)
    return jsonify(output)


def _get_chord_names(data):
    """
    Returns chord names for specified frets
    """

    try:
        played_notes = idntf.noteForStrings(data)
        names = identify(played_notes, idntf)
    except Exception:
        _handle_exception()
        return None
    return names or None


def _get_fingers(data):
    """
    Returns fingers for specified frets
    """

    try:
        fingers, _ = predict_fingering(data)
    except Exception:
        _handle_exception()
        return None
    return fingers or None


def _get_greene_voicing(data):
    """
    Returns green voicing data if only there are 4 items in the
    chord list ofr specified frets.
    """

    try:
        played_notes = idntf.noteForStrings(data)
        result = random.choice(list(greene_table.keys())) if len(
            played_notes) == 4 else None
    except Exception:
        _handle_exception()
        return None
    return result


def _handle_exception():
    """
    Prints the traceback of the latest exception.
    Used in cases where logic code fails
    """

    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)


if __name__ == '__main__':
    app.run()
