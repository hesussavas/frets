# initializing and activating virtualenv
mkdir -p .venv
cd .venv
virtualenv --python=python3.5 frets
cd ..
source .venv/frets/bin/activate

# setting up the app
export FLASK_APP=frets.py
pip install -r requirements.txt

# run the migration
flask db upgrade

# start the app
flask run


