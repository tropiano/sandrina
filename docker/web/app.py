import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


DBUSER = 'sandrina'
DBPASS = 'v5sYvBKw'
DBHOST = 'postgresql'
DBPORT = '5432'
DBNAME = 'sandrina'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class comuni(db.Model):
    
    __table__ = db.Model.metadata.tables['comuni']


class salute(db.Model):
    
    __table__ = db.Model.metadata.tables['salute']


@app.route('/', methods=['GET'])
def home():
    
    cur=db.session.query(comuni).limit(3)
    return render_template('home_datum.html', entries=cur)


@app.route('/<nome_regione>/comuni', methods=['GET'])
def show_comuni(nome_regione):
    
    cur=db.session.query(comuni).filter(comuni.regione == nome_regione)
    return render_template('analytics_datum.html', entries=cur.all(), regione=nome_regione)




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')