from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///gorky.db")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/juego" , methods=["GET", "POST"])
#@login_required
def juego():
    if request.method == "POST":
        if not request.form.get("usuario"):
            return apology("Debe ingresar su nombre", 403)
        userE = db.execute("SELECT Nombre FROM Usuario WHERE Nombre = :username",username=request.form.get("usuario"))
        if not userE :
            db. execute("Insert into Usuario(Id, Nombre) values (NULL,:usuario)", usuario= request.form.get("usuario"))
        else:
            return apology("El usuario ya existe",400 )
        nombre = db.execute("SELECT Id FROM Usuario WHERE Nombre = :username",username=request.form.get("usuario"))

        session["usuario"] = nombre[0]["Id"]
        return render_template("juego.html")

@app.route("/puntuaciones")
def puntuaciones():
    rows = db.execute("SELECT * fRoM Usuario")
    return render_template("puntuaciones.html", rows=rows)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/logoutt/<puntuacion>")
def logoutt(puntuacion):
    """Log user out"""
    punt = puntuacion
    db.execute("update Usuario set Puntuacion = :score where id=:id",score=punt,id=session["usuario"])
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")