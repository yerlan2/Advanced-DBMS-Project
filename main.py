from flask import Flask, g, request, session, render_template, redirect, url_for
import sqlite3, hashlib, os

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


def execute_commit(conn, param, query):
    cur = conn.cursor()
    cur.execute(query, param)
    conn.commit()
    return cur.lastrowid


def execute_query(conn, sql):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    return cur


def execute_query_param_tuple(conn, param, query):
    cur = conn.cursor()
    cur.execute(query, param)
    return cur


def execute_query_param(conn, param, query):
    conn.row_factory = sqlite3.Row
    return execute_query_param_tuple(conn, param, query)


@app.route('/')
@app.route('/p/<int:page>')
def index(page=1):
    if not session.get('logged_in'):
        return redirect("/login")
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    posts = execute_query_param(conn, ((page-1)*10,), '''
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM posts p, postimages pi, images i, accounts a, categories c
        WHERE p.id=pi.post_id 
        AND pi.image_id=i.id 
        AND p.account_id=a.id 
        AND p.category_id=c.id 
        GROUP BY pi.post_id
        LIMIT 10 OFFSET ? '''
    ).fetchall()
    return render_template("main/home.html", categories=categories, posts=posts)


@app.route('/category/<int:id>')
@app.route('/category/<int:id>/p/<int:page>')
def post_category(id, page=1):
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    posts = execute_query_param(conn, (id, (page-1)*10), """
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM posts p, postimages pi, images i, accounts a, categories c
        WHERE p.id=pi.post_id 
        AND pi.image_id=i.id 
        AND p.account_id=a.id 
        AND p.category_id=c.id 
        GROUP BY pi.post_id
        HAVING c.id=?
        LIMIT 10 OFFSET ? """
    ).fetchall()
    return render_template("main/home.html", categories=categories, posts=posts)

    
@app.route('/post/<int:id>')
def post_detail(id):
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    post = execute_query_param(conn, (id,), """
        SELECT p.id id, a.name account_name, i.path image_path, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM posts p, accounts a, categories c, images i
        WHERE p.account_id=a.id 
        AND p.category_id=c.id 
        AND a.image_id=i.id 
        AND p.id=? """
    ).fetchone()
    comments = execute_query_param(conn, (id,), """
        SELECT c.id as id, c.post_id as post_id, a.name as account_name, c.content as content, c.added_date as added_date 
        FROM comments c, accounts a 
        WHERE c.account_id=a.id AND c.post_id=? ORDER BY added_date DESC """
    ).fetchall()
    images = execute_query_param(conn, (id,), """
        SELECT i.id, i.path 
        FROM images i, postimages pi, posts p 
        WHERE i.id=pi.image_id 
        AND pi.post_id=p.id and p.id=? """
    ).fetchall()
    execute_commit(conn, (id,), "UPDATE posts SET view_count = view_count + 1 WHERE id = ?")
    return render_template("main/post_detail.html", post=post, comments=comments, images=images, categories=categories)


@app.route('/accounts')
def account_list():
    if not session.get('logged_in'):
        return redirect("/login")
    account_id = session['account'][0]
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (account_id,), 
        "SELECT * FROM accounts WHERE id!=? ORDER BY id DESC"
    ).fetchall()
    return render_template("main/account_list.html", categories=categories, accounts=accounts)


@app.route('/account/<int:id>')
@app.route('/account/<int:id>/p/<int:page>')
def account_detail(id, page=1):
    follower_id = session['account'][0]
    conn = get_db()
    posts = execute_query_param(conn, (id, (page-1)*10), """
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.created_date created_date, p.like_count like_count, p.view_count like_count 
        FROM posts p, postimages pi, images i, accounts a, categories c
        WHERE p.id=pi.post_id 
        AND pi.image_id=i.id 
        AND p.account_id=a.id 
        AND p.category_id=c.id 
        GROUP BY pi.post_id
        HAVING a.id=?
        LIMIT 10 OFFSET ? """
    ).fetchall()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    return render_template("main/account_detail.html", posts=posts, account_id=id, check_follow=check_follow(conn, follower_id, id),
        categories=categories)


@app.route('/authors')
def author_list():
    if not session.get('logged_in'):
        return redirect("/login")
    follower_id = session['account'][0]
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (follower_id,), """
        SELECT a.id, a.name, a.email, a.password, a.image_id
        FROM subscriptions s, accounts a
        WHERE s.author_id = a.id
        AND s.follower_id=?
        ORDER BY a.id DESC """
    ).fetchall()
    return render_template("main/account_list.html", categories=categories, accounts=accounts)


@app.route('/followers')
def follower_list():
    if not session.get('logged_in'):
        return redirect("/login")
    follower_id = session['account'][0]
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (follower_id,), """
        SELECT a.id, a.name, a.email, a.password, a.image_id
        FROM subscriptions s, accounts a
        WHERE s.follower_id = a.id
        AND s.author_id=?
        ORDER BY a.id DESC """
    ).fetchall()
    return render_template("main/account_list.html", categories=categories, accounts=accounts)


def check_follow(conn, follower_id, author_id):
    rows = execute_query_param(conn, (follower_id, author_id), """
        SELECT * FROM subscriptions 
        WHERE follower_id=? 
        AND author_id=? """
    ).fetchall()
    return True if rows else False


@app.route('/follow', methods=['POST', 'GET'])
def follow():
    if request.method == "POST":
        follower_id = session['account'][0]
        author_id = request.form['author_id']
        conn = get_db()
        if not check_follow(conn, follower_id, author_id):
            with conn:
                follow_id = execute_commit(conn, (follower_id, author_id), "INSERT INTO subscriptions(follower_id, author_id) VALUES(?,?)")
            return redirect(f"/account/{author_id}")


@app.route('/unfollow', methods=['POST', 'GET'])
def unfollow():
    if request.method == "POST":
        follower_id = session['account'][0]
        author_id = request.form['author_id']
        conn = get_db()
        if check_follow(conn, follower_id, author_id):
            with conn:
                execute_commit(conn, (follower_id, author_id), "DELETE FROM subscriptions WHERE follower_id=? AND author_id=?")
            return redirect(f"/account/{author_id}")


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
        account = session.get('account')
        if account:
            with conn:
                comment = (post_id, account[0], content)
                comment_id = execute_commit(conn, comment, "INSERT INTO comments(post_id, account_id, content) VALUES(?,?,?)")
            return redirect(f"/post/{post_id}")
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
        account = execute_query_param_tuple(conn, account, "SELECT * FROM accounts WHERE email=? AND password=?").fetchone()
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
                    account_id = execute_commit(conn, account, """ INSERT INTO accounts(name, email, password) VALUES(?,?,?) """)
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


@app.template_filter('strftime')
def _jinja2_filter_datetime(datestr):
    from datetime import date
    date_time = date.fromisoformat(datestr[:10])
    date_time_obj = date_time.strftime("%b %d")
    return date_time_obj


@app.route('/admin')
def admin():
    return render_template("admin/dashboard.html")



if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
