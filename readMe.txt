Linux:
pip install virtualenv
pip install -r requirements.txt
. venv/bin/activate
export FLASK_APP=app.py
export FLASK_DEBUG=true #developer
flask run


Windows:
pip install virtualenv
python -m virtualenv env
pip install -r requirements.txt
.\env\Scripts\activate
set FLASK_APP=app.py
set FLASK_DEBUG=true #developer
flask run