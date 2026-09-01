from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_logement", methods=["GET","POST"])
def add_one_logement():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into logement (title,description) values (:title,:description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from logement')


        return render_template("logementform.html", logements=user, one_user=one_user, the_title="add new logement")


    user = query_db('select * from logement')
    one_user = query_db("select * from logement limit 1", one=True)
    return render_template("logementform.html", logements=user, one_user=one_user, the_title="add new logement")

@app.route("/add_one_logementhasuser", methods=["GET","POST"])
def add_one_logementhasuser():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into logementhasuser (user_id,logement_id) values (:user_id,:logement_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from logementhasuser')


        return render_template("logementhasuserform.html", logementhasusers=user, one_user=one_user, the_title="add new logementhasuser")


    user = query_db('select * from logementhasuser')
    one_user = query_db("select * from logementhasuser limit 1", one=True)
    return render_template("logementhasuserform.html", logementhasusers=user, one_user=one_user, the_title="add new logementhasuser")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        touslesmusicstyle= query_db("select * from musicstyle")

        one_user = query_db("insert into user (username,password,email,phone,country_id,musicstyle_id) values (:username,:password,:email,:phone,:country_id,:musicstyle_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','password','email','phone','country_id','musicstyle_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesmusicstyle=touslesmusicstyle)


    touslescountry= query_db("select * from country")

    touslesmusicstyle= query_db("select * from musicstyle")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesmusicstyle=touslesmusicstyle)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','password','email','phone','country_id','musicstyle_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','password','email','phone','country_id','musicstyle_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_userhasjob", methods=["GET","POST"])
def add_one_userhasjob():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into userhasjob (user_id,job_id,logement_id) values (:user_id,:job_id,:logement_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from userhasjob')


        return render_template("userhasjobform.html", userhasjobs=user, one_user=one_user, the_title="add new userhasjob")


    user = query_db('select * from userhasjob')
    one_user = query_db("select * from userhasjob limit 1", one=True)
    return render_template("userhasjobform.html", userhasjobs=user, one_user=one_user, the_title="add new userhasjob")

@app.route("/add_one_job", methods=["GET","POST"])
def add_one_job():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into job (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from job')


        return render_template("jobform.html", jobs=user, one_user=one_user, the_title="add new job")


    user = query_db('select * from job')
    one_user = query_db("select * from job limit 1", one=True)
    return render_template("jobform.html", jobs=user, one_user=one_user, the_title="add new job")

@app.route("/add_one_musicstyle", methods=["GET","POST"])
def add_one_musicstyle():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into musicstyle (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from musicstyle')


        return render_template("musicstyleform.html", musicstyles=user, one_user=one_user, the_title="add new musicstyle")


    user = query_db('select * from musicstyle')
    one_user = query_db("select * from musicstyle limit 1", one=True)
    return render_template("musicstyleform.html", musicstyles=user, one_user=one_user, the_title="add new musicstyle")

@app.route("/add_one_pianoaccompaniedpiece", methods=["GET","POST"])
def add_one_pianoaccompaniedpiece():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesmusicalinstrument= query_db("select * from musicalinstrument")

        touslesmusicstyle= query_db("select * from musicstyle")

        one_user = query_db("insert into pianoaccompaniedpiece (musicalinstrument_id,title,composer,musicstyle_id) values (:musicalinstrument_id,:title,:composer,:musicstyle_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from pianoaccompaniedpiece')


        return render_template("pianoaccompaniedpieceform.html", pianoaccompaniedpieces=user, one_user=one_user, the_title="add new pianoaccompaniedpiece", touslesmusicalinstrument=touslesmusicalinstrument, touslesmusicstyle=touslesmusicstyle)


    touslesmusicalinstrument= query_db("select * from musicalinstrument")

    touslesmusicstyle= query_db("select * from musicstyle")

    user = query_db('select * from pianoaccompaniedpiece')
    one_user = query_db("select * from pianoaccompaniedpiece limit 1", one=True)
    return render_template("pianoaccompaniedpieceform.html", pianoaccompaniedpieces=user, one_user=one_user, the_title="add new pianoaccompaniedpiece", touslesmusicalinstrument=touslesmusicalinstrument, touslesmusicstyle=touslesmusicstyle)

@app.route("/add_one_musicalinstrument", methods=["GET","POST"])
def add_one_musicalinstrument():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into musicalinstrument (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from musicalinstrument')


        return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")


    user = query_db('select * from musicalinstrument')
    one_user = query_db("select * from musicalinstrument limit 1", one=True)
    return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")

