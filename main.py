from flask import Flask, g, request, session, render_template, redirect, url_for, make_response, jsonify
import sqlite3
import pandas as pd
import hashlib


app = Flask(__name__)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = create_connection('../db.sqlite3')
    return g.sqlite_db


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


def select_post(conn, post_id):
    sql = ''' SELECT * FROM posts WHERE id=? '''
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (post_id,))
    return dict(cur.fetchone())


def sql_select(conn, query):
    df = pd.read_sql_query(query, conn).to_dict('records')
    return df


@app.route('/')
def index():
    conn = get_db()
    posts = sql_select(conn, "SELECT * FROM posts ORDER BY id DESC")
    return render_template("main/home.html", posts=posts)


@app.route('/p/<int:id>')
def post_detail(id):
    conn = get_db()
    post = select_post(conn, id)
    return render_template("main/post_detail.html", post=post)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        err_msg = []
        conn = get_db()
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
            conn = get_db()
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
