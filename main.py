from flask import Flask, g, request, flash, session, render_template, redirect, url_for, make_response, jsonify
import sqlite3
import hashlib
import os


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


def create_comment(conn, comment):
    sql = ''' INSERT INTO comments(post_id, account_id, content) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, comment)
    conn.commit()
    return cur.lastrowid


def select_account(conn, account):
    sql = ''' SELECT email, password FROM accounts WHERE email=? AND password=? '''
    cur = conn.cursor()
    cur.execute(sql, account)
    return cur.fetchone()


def select_account_all(conn, account):
    sql = ''' SELECT * FROM accounts WHERE email=? AND password=? '''
    cur = conn.cursor()
    cur.execute(sql, account)
    return cur.fetchone()


def select_post(conn, post_id):
    sql = ''' SELECT * FROM posts WHERE id=? '''
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (post_id,))
    return cur.fetchone()


def select_post_category(conn, category_id):
    sql = ''' SELECT * FROM posts WHERE category_id=? '''
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (category_id,))
    return cur.fetchall()


def select_comments(conn, post_id):
    sql = ''' 
        SELECT c.id as id, c.post_id as post_id, a.name as account_name, c.content as content, c.added_date as added_date 
        FROM comments c, accounts a 
        WHERE c.account_id=a.id AND c.post_id=? ORDER BY added_date DESC 
        '''
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (post_id,))
    return cur.fetchall()


def select_postimages(conn, post_id):
    sql = ''' SELECT i.id, i.path FROM images i, postimages pi, posts p WHERE i.id=pi.image_id and pi.post_id=p.id and p.id=? '''
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (post_id,))
    return cur.fetchall()


def select_sql(conn, sql):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect("/login")
    conn = get_db()
    categories = select_sql(conn, "SELECT * FROM categories")
    posts = select_sql(conn, "SELECT * FROM posts ORDER BY id DESC")
    return render_template("main/home.html", categories=categories, posts=posts)


@app.route('/c/<int:id>')
def post_category(id):
    conn = get_db()
    categories = select_sql(conn, "SELECT * FROM categories")
    posts = select_post_category(conn, id)
    return render_template("main/home.html", categories=categories, posts=posts)

    
@app.route('/p/<int:id>')
def post_detail(id):
    conn = get_db()
    post = select_post(conn, id)
    comments = select_comments(conn, id)
    images = select_postimages(conn, id)
    return render_template("main/post_detail.html", post=post, comments=comments, images=images)


@app.route('/add-comment', methods=['POST', 'GET'])
def add_comment():
    if request.method == "POST":
        if not session.get('logged_in'):
            return redirect("/login")
        post_id = request.form['post_id']
        content = request.form['content']

        err_msg = []
        conn = get_db()
        conn.row_factory = sqlite3.Row
        account = select_account_all(conn, session.get('account'))
        if account:
            with conn:
                comment = (post_id, account["id"], content)
                comment_id = create_comment(conn, comment)
            return redirect(f"/p/{post_id}")
        else:
            return redirect("/login")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        err_msg = []
        conn = get_db()
        account = (email, hashlib.sha1(password.encode()).hexdigest())
        account = select_account(conn, account)
        if account:
            session['account'] = account
            session['logged_in'] = True
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
        return redirect("/login")
    else:
        return render_template("auth/signup.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/")


if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
