from flask import Flask, request, session, render_template, redirect, url_for, make_response, jsonify
import sqlite3
import pandas as pd
import hashlib


app = Flask(__name__)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as err:
        print('Error while creating the connection ', err)
    return conn


def create_account(conn, account):
    sql = ''' INSERT INTO accounts(name, email, password) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, account)
    conn.commit()
    return cur.lastrowid


def select_account(conn, account):
    sql = ''' SELECT email, password FROM accounts WHERE email=? AND password=? '''
    cur = conn.cursor()
    cur.execute(sql, account)
    return cur.fetchone()


def sql_select(query):
    try:
        conn = sqlite3.connect('../db.sqlite3')
        df = pd.read_sql_query(query, conn).to_dict('records')
    except Exception as err:
        print('Error while creating the connection ', err)
    finally:
        conn.close()
    return df


@app.route('/')
def index():
    posts = sql_select("SELECT * FROM posts")
    return render_template("main/home.html", posts=posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        err_msg = []
        conn = create_connection("../test.db")
        account = (email, hashlib.sha1(password.encode()).hexdigest())
        if select_account(conn, account):
            return redirect("/")
        else:
            return render_template("auth/login.html", err_msg=["Email or password incorrect."])
    else:
        return render_template("auth/login.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        err_msg = []
        if password != password_confirm:
            err_msg.append("Password incorrect.")

        if not err_msg:
            conn = create_connection("../test.db")
            with conn:
                account = (username, email, hashlib.sha1(password.encode()).hexdigest())
                try:
                    account_id = create_account(conn, account)
                except sqlite3.IntegrityError as err:
                    err_msg.append("Email exists.")
    
        if err_msg:
            return render_template("auth/signup.html", err_msg=err_msg)
        return redirect("/")
    else:
        return render_template("auth/signup.html")


if __name__=="__main__":
    app.run(debug=True)
