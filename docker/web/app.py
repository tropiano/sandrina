from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


DBUSER = 'sandrina'
DBPASS = 'v5sYvBKw'
DBHOST = 'postgresql'
DBPORT = '5432'
DBNAME = 'sandrina'


app = Flask(__name__)
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

    cur = db.session.query(comuni).limit(3)
    return render_template('home_datum.html', entries=cur)


@app.route('/regioni', methods=['GET'])
def show_comuni():

    cur = db.session.query(comuni.regione,
                           func.count(comuni.id).label("n_comuni")
                           ).group_by(comuni.regione
                                      ).order_by(func.count(comuni.id
                                                            ).label("n_comuni"
                                                                    ).desc())

    return render_template('analytics_datum.html', entries=cur.all())


@app.route('/<nome_regione>', methods=['GET'])
def show_regione(nome_regione):

    cur = db.session.query(comuni).filter(comuni.regione == nome_regione)

    cur_1 = db.session.query(comuni, salute
                             ).join(salute,
                                    salute.comune_id == comuni.id
                                    ).filter(comuni.regione == nome_regione
                                             ).filter(salute.anno == 2014)

    negri = []

    for datum in cur_1.all():

        j_datum = datum[1].entry
        comune_name = datum[0].nome
        negri.append(j_datum['Percentuale nati di cittadinanza non italiana'],
                     comune_name)

    negri_max = max(negri, key=lambda item: item[0])
    negri_min = min(negri, key=lambda item: item[0])
    negri_avg = sum(n[0] for n in negri) / float(len(negri))

    return render_template('analytics_regioni_datum.html',
                           entries=cur.all(),
                           regione=nome_regione,
                           negri_max=negri_max,
                           negri_min=negri_min,
                           negri_avg=negri_avg)


@app.route('/<nome_regione>/<nome_comune>', methods=['GET'])
def show_comune(nome_regione, nome_comune):

    cur = db.session.query(comuni,
                           salute).join(salute,
                                        salute.comune_id == comuni.id
                                        ).filter(comuni.nome == nome_comune
                                                 ).filter(salute.anno == 2014)

    negri = 0.
    nascite = 0.
    reddito_res = None
    reddito_con = None
    for datum in cur.all():
        j_datum = datum[1].entry
        reddito_res = j_datum['Reddito imponibile medio per residente']
        reddito_con = j_datum['Reddito imponibile medio per contribuente']
        negri = j_datum['Percentuale nati di cittadinanza non italiana']
        nascite = j_datum['Quoziente di incremento naturale (x 1.000)']

    return render_template('analytics_comuni_datum.html',
                           entries=cur.all(),
                           reddito_res=reddito_res,
                           reddito_con=reddito_con,
                           negri=negri,
                           nome_comune=nome_comune,
                           nascite=nascite / 10.)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
