"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template
from .forms import LogUserForm, secti,masoform,vstupnitestform
from ..data.database import db
from ..data.models import LogUser
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET','POST'])
def vstupnitest():
    from .forms import vstupnitestform
    from ..data.models.vysledky import Vysledky
    from sqlalchemy import func
    form = vstupnitestform()
    if form.validate_on_submit():
        vysledek = 0
        if form.otazka1.data ==2 :
            vysledek = vysledek + 1
        if form.otazka2.data == 0:
            vysledek = vysledek + 1
        if form.otazka3.data.upper() == "ELEPHANT" :
            vysledek = vysledek + 1
            i = Vysledky(username=form.Jmeno.data,hodnoceni= vysledek)
            db.session.add(i)
            db.session.commit()
            dotaz = db.session.query(Vysledky.username, func.count(Vysledky.hodnoceni).label("suma")).group_by(
                Vysledky.username).all()
            return render_template('public/vysledekvystup.tmpl',data=dotaz)
    return render_template('public/vstupnitest.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET'])
def testvstupu():
    from ..data.models.vysledky import Vysledky
    from sqlalchemy import func

    dotaz = db.session.query(Vysledky.username, func.count(Vysledky.hodnoceni).label("suma")).group_by(
        Vysledky.jmeno).all()
    return render_template('public/vstupnitest.tmpl', data=dotaz)

@blueprint.route('/vystupuzivatele/<jmeno>', methods=['GET'])
def testvstupuuzivatel(jmeno):
    from ..data.models.vysledky import Vysledky
    dotaz = db.session.query(Vysledky.username, Vysledky.hodnoceni).\
        filter(Vysledky.username == jmeno).all()
    return render_template('public/vysledekvystupuzivatel.tmpl', data=dotaz, jmeno = jmeno)



@blueprint.route('/nactenijson', methods=['GET'])
def nactenijson():
    from flask import jsonify
    import requests, os
    os.environ['NO PROXY'] = '127.0.0.1'
    proxies = {
        "http": None,
        "https": "https://192.168.1.1:800"
    }
    response = requests.get("http://192.168.10.1:5000/nactenijson",proxies = proxies)
    json_res = response.json()
    data = []
    for radek in json_res["list"]:
        print radek["main"]['temp']
    return jsonify(json_res)


from flask import Flask
from flask import render_template
from datetime import time

app = Flask(__name__)


@blueprint.route("/simple_chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)


if __name__ == "__main__":
    app.run(debug=True)

@blueprint.route("/line_chart")
def line_chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('line_chart.html', values=temperatures, labels=times, legend=legend)

@blueprint.route("/time_chart")
def time_chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = [time(hour=11, minute=14, second=15),
             time(hour=11, minute=14, second=30),
             time(hour=11, minute=14, second=45),
             time(hour=11, minute=15, second=00),
             time(hour=11, minute=15, second=15),
             time(hour=11, minute=15, second=30),
             time(hour=11, minute=15, second=45),
             time(hour=11, minute=16, second=00),
             time(hour=11, minute=16, second=15),
             time(hour=11, minute=16, second=30),
             time(hour=11, minute=16, second=45),
             time(hour=11, minute=17, second=00),
             time(hour=11, minute=17, second=15),
             time(hour=11, minute=17, second=30),
             time(hour=11, minute=17, second=45),
             time(hour=11, minute=18, second=00),
             time(hour=11, minute=18, second=15),
             time(hour=11, minute=18, second=30)]
    return render_template('time_chart.html', values=temperatures, labels=times, legend=legend)


