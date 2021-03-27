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


def execute_query_tuple(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def execute_query(conn, sql):
    conn.row_factory = sqlite3.Row
    return execute_query_tuple(conn, sql)


def execute_query_param_tuple(conn, param, query):
    cur = conn.cursor()
    cur.execute(query, param)
    return cur

def execute_query_param(conn, param, query):
    conn.row_factory = sqlite3.Row
    return execute_query_param_tuple(conn, param, query)


pagination_num=11
post_num=10


@app.route('/')
def index():
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    if  session.get('logged_in'):
        account_id = session['account'][0]
        posts = execute_query_param(conn, (account_id, account_id, limit, offset,), """
            SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
            FROM accounts a, categories c, posts p, subscriptions s 
            LEFT JOIN postimages pi ON pi.post_id = p.id 
            LEFT JOIN images i ON pi.image_id = i.id 
            WHERE p.account_id=a.id 
            AND p.category_id=c.id 
            AND p.account_id=s.author_id
            AND (
                p.account_id=? 
                OR 
                s.author_id IN (SELECT author_id FROM subscriptions WHERE follower_id=?)
            )
            GROUP BY p.id
            ORDER BY p.id DESC
            LIMIT ? OFFSET ? """
        ).fetchall()
    else:
        posts = execute_query_param(conn, (limit, offset,), """
            SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
            FROM accounts a, categories c, posts p 
            LEFT JOIN postimages pi ON pi.post_id = p.id 
            LEFT JOIN images i ON pi.image_id = i.id 
            WHERE p.account_id=a.id 
            AND p.category_id=c.id 
            GROUP BY p.id
            ORDER BY p.id DESC
            LIMIT ? OFFSET ? """
        ).fetchall()
    conn.close()
    next_pages_num = -(-len(posts)//post_num)-1
    return render_template("main/home.html", categories=categories, posts=posts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/other')
def all_posts():
    if not session.get('logged_in'):
        return redirect(url_for('login', next=request.full_path))
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    account_id = session['account'][0]
    posts = execute_query_param(conn, (account_id, account_id, limit, offset,), """
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM accounts a, categories c, posts p, subscriptions s 
        LEFT JOIN postimages pi ON pi.post_id = p.id 
        LEFT JOIN images i ON pi.image_id = i.id 
        WHERE p.account_id=a.id 
        AND p.category_id=c.id 
        AND p.account_id=s.author_id
        AND p.account_id!=?
        AND s.author_id NOT IN (SELECT author_id FROM subscriptions WHERE follower_id=?)
        GROUP BY p.id
        ORDER BY p.id DESC
        LIMIT ? OFFSET ? """
    ).fetchall()
    conn.close()
    next_pages_num = -(-len(posts)//post_num)-1
    return render_template("main/home.html", categories=categories, posts=posts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/category/<int:id>')
def post_category(id):
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    posts = execute_query_param(conn, (id, limit, offset,), """
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM accounts a, categories c, posts p 
        LEFT JOIN postimages pi ON pi.post_id = p.id 
        LEFT JOIN images i ON pi.image_id = i.id 
        WHERE p.account_id=a.id 
        AND p.category_id=c.id 
        GROUP BY p.id
        HAVING c.id=?
        ORDER BY p.id DESC
        LIMIT ? OFFSET ? """
    ).fetchall()
    conn.close()
    next_pages_num = -(-len(posts)//post_num)-1
    return render_template("main/home.html", categories=categories, posts=posts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/post/<int:id>')
def post_detail(id):
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    post = execute_query_param(conn, (id,), """
        SELECT p.id id, a.id account_id, a.name account_name, i.path image_path, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM posts p, accounts a, categories c
        LEFT JOIN images i ON a.image_id = i.id
        WHERE p.account_id=a.id 
        AND p.category_id=c.id 
        AND p.id=? """
    ).fetchone()
    like_result = False
    if session.get('logged_in'):
        account_id = session['account'][0]
        like_result = check_like(conn, id, account_id)
    comments = execute_query_param(conn, (id,), """
        SELECT c.id as id, c.post_id as post_id, a.name as account_name, i.path image_path, c.content as content, c.added_date as added_date 
        FROM comments c, accounts a 
        LEFT JOIN images i ON a.image_id = i.id
        WHERE c.account_id=a.id 
        AND c.post_id=? 
        ORDER BY added_date DESC """
    ).fetchall()
    images = execute_query_param(conn, (id,), """
        SELECT i.id, i.path 
        FROM images i, postimages pi, posts p 
        WHERE i.id=pi.image_id 
        AND pi.post_id=p.id and p.id=? """
    ).fetchall()
    execute_commit(conn, (id,), "UPDATE posts SET view_count = view_count + 1 WHERE id = ?")
    conn.close()
    return render_template("main/post_detail.html", post=post, check_like=like_result, comments=comments, images=images, categories=categories)


def check_like(conn, post_id, account_id):
    rows = execute_query_param(conn, (post_id, account_id), "SELECT * FROM likes WHERE post_id=? AND account_id=?").fetchall()
    return True if rows else False


@app.route('/like', methods=['POST', 'GET'])
def like():
    account_id = session['account'][0]
    post_id = request.args.get('post_id')
    conn = get_db()
    like_result = False
    post = 0
    with conn:
        if not check_like(conn, post_id, account_id):
            execute_commit(conn, (post_id, account_id), "INSERT INTO likes(post_id, account_id) VALUES(?,?)")
            execute_commit(conn, (post_id,), "UPDATE posts SET like_count = like_count + 1 WHERE id = ?")
            like_result = True
        else:
            execute_commit(conn, (post_id, account_id), "DELETE FROM likes WHERE post_id=? AND account_id=?")
            execute_commit(conn, (post_id,), "UPDATE posts SET like_count = like_count - 1 WHERE id = ?")
        post = execute_query_param(conn, (post_id,), "SELECT like_count FROM posts WHERE id=?").fetchone()
    return render_template("small_templates/like.html", post=post, check_like=like_result)


@app.route('/search', methods=['GET'])
def search():
    if request.method == "GET":
        q = request.args.get('q')
        query = f"%{q}%"
        page = 1 if request.args.get('p') is None else int(request.args.get('p'))
        offset = (page-1)*post_num
        limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
        conn = get_db()
        categories = execute_query(conn, "SELECT * FROM categories").fetchall()
        posts = execute_query_param(conn, (query, query, query, limit, offset,), """
            SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
            FROM accounts a, categories c, posts p 
            LEFT JOIN postimages pi ON pi.post_id = p.id 
            LEFT JOIN images i ON pi.image_id = i.id 
            WHERE p.account_id=a.id 
            AND p.category_id=c.id 
            GROUP BY p.id
            HAVING LOWER(p.title) LIKE LOWER(?)
            OR LOWER(p.content) LIKE LOWER(?)
            OR LOWER(c.name) LIKE LOWER(?)
            ORDER BY p.id DESC
            LIMIT ? OFFSET ? """
        ).fetchall()
        conn.close()
        next_pages_num = -(-len(posts)//post_num)-1
        return render_template("main/home.html", categories=categories, posts=posts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/accounts')
def account_list():
    if not session.get('logged_in'):
        return redirect(url_for('login', next=request.full_path))
    account_id = session['account'][0]
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (account_id, limit, offset,), """
        SELECT a.id id, a.name name, i.path image_path
        FROM accounts a
        LEFT JOIN images i ON a.image_id = i.id
        WHERE a.id!=?
        ORDER BY id DESC
        LIMIT ? OFFSET ? """
    ).fetchall()
    conn.close()
    next_pages_num = -(-len(accounts)//post_num)-1
    return render_template("main/account_list.html", categories=categories, accounts=accounts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/account/<int:id>')
def account_detail(id):
    if not session.get('logged_in'):
        return redirect(url_for('login', next=request.full_path))
    follower_id = session['account'][0]
    p = request.args.get('p')
    page = 0 if p is None else (int(p)-1)*10
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    posts = execute_query_param(conn, (id, page,), """
        SELECT p.id id, i.id image_id, i.path image_path, a.name account_name, c.name category_name, p.title title, p.content content, p.created_date created_date, p.like_count like_count, p.view_count view_count 
        FROM accounts a, categories c, posts p 
        LEFT JOIN postimages pi ON pi.post_id = p.id 
        LEFT JOIN images i ON pi.image_id = i.id 
        WHERE p.account_id=a.id 
        AND p.category_id=c.id 
        GROUP BY p.id
        HAVING a.id=?
        ORDER BY p.id DESC
        LIMIT 10 OFFSET ? """
    ).fetchall()
    account = execute_query_param(conn, (id,), """
        SELECT a.id id, a.name name, a.email email,  i.path image_path 
        FROM accounts a
        LEFT JOIN images i
        ON a.image_id = i.id 
        WHERE a.id=? """
    ).fetchone()
    follow_result = check_follow(conn, follower_id, id)
    conn.close()
    return render_template("main/account_detail.html", categories=categories, posts=posts, check_follow=follow_result, account=account)


@app.route('/authors')
def author_list():
    if not session.get('logged_in'):
        return redirect(url_for('login', next=request.full_path))
    follower_id = session['account'][0]
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (follower_id, limit, offset,), """
        SELECT a.id id, a.name name, i.path image_path
        FROM subscriptions s, accounts a
        LEFT JOIN images i ON a.image_id = i.id
        WHERE s.author_id = a.id
        AND s.follower_id=?
        ORDER BY a.id DESC
        LIMIT ? OFFSET ? """
    ).fetchall()
    conn.close()
    next_pages_num = -(-len(accounts)//post_num)-1
    return render_template("main/account_list.html", categories=categories, accounts=accounts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


@app.route('/followers')
def follower_list():
    if not session.get('logged_in'):
        return redirect(url_for('login', next=request.full_path))
    follower_id = session['account'][0]
    page = 1 if request.args.get('p') is None else int(request.args.get('p'))
    offset = (page-1)*post_num
    limit = -(-pagination_num//2)*post_num if page >= -(-pagination_num//2) else (pagination_num-page+1)*post_num
    conn = get_db()
    categories = execute_query(conn, "SELECT * FROM categories").fetchall()
    accounts = execute_query_param(conn, (follower_id, limit, offset,), """
        SELECT a.id id, a.name name, i.path image_path
        FROM subscriptions s, accounts a
        LEFT JOIN images i ON a.image_id = i.id
        WHERE s.follower_id = a.id
        AND s.author_id=?
        ORDER BY a.id DESC
        LIMIT ? OFFSET ? """
    ).fetchall()
    conn.close()
    next_pages_num = -(-len(accounts)//post_num)-1
    return render_template("main/account_list.html", categories=categories, accounts=accounts[:post_num], page=page, pagination_num=pagination_num, next_pages_num=next_pages_num)


def check_follow(conn, follower_id, author_id):
    rows = execute_query_param(conn, (follower_id, author_id), "SELECT * FROM subscriptions WHERE follower_id=? AND author_id=?").fetchall()
    return True if rows else False


@app.route('/follow', methods=['POST', 'GET'])
def follow():
    if request.method == "POST":
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
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
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
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
            return redirect(url_for('login', next=request.full_path))
        post_id = request.form['post_id']
        content = request.form['content']
        err_msg = []
        conn = get_db()
        account = session.get('account')
        if account:
            with conn:
                comment = (post_id, account[0], content)
                comment_id = execute_commit(conn, comment, "INSERT INTO comments(post_id, account_id, content) VALUES(?,?,?)")
            return redirect(f"/post/{post_id}")
        return redirect(url_for('login', next=request.full_path))


@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
        account_id = session['account'][0]
        category_id = request.form['category_id']
        title = request.form['title']
        content = request.form['content']
        images_paths = request.form['images_paths'].split()
        post_id = None
        conn = get_db()
        with conn:
            post = (account_id, category_id, title, content)
            post_id = execute_commit(conn, post, 
                "INSERT INTO posts(account_id, category_id, title, content) VALUES(?,?,?,?)"
            )
            for image_path in images_paths:
                image_id = execute_commit(conn, (image_path,), 
                    "INSERT INTO images(path) VALUES(?)"
                )
                execute_commit(conn, (post_id, image_id), 
                    "INSERT INTO postimages(post_id, image_id) VALUES(?,?)"
                )
        return redirect(f"/post/{post_id}")
    else:
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
        conn = get_db()
        categories = execute_query(conn, "SELECT * FROM categories").fetchall()
        conn.close()
        return render_template("main/post_create.html", categories=categories)


@app.route('/post/<int:id>/edit', methods=['POST', 'GET'])
def update_post(id):
    if request.method == "POST":
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
        account_id = session['account'][0]
        post_acccount_id = request.form['post_acccount_id']
        if int(post_acccount_id) != int(account_id):
            print(post_acccount_id, account_id)
            return redirect("/")
        category_id = request.form['category_id']
        title = request.form['title']
        content = request.form['content']
        images_paths = request.form['images_paths'].split()
        conn = get_db()
        with conn:
            post = (category_id, title, content, id)
            execute_commit(conn, post, """
                UPDATE posts 
                SET category_id=?, title=?, content=? 
                WHERE id=?"""
            )
            images = execute_query_param(conn, (id,), """
                SELECT i.path image_path
                FROM postimages pi, images i
                WHERE pi.image_id=i.id
                AND pi.post_id=? """
            ).fetchall()
            flag = False
            print(images_paths, images)
            if len(images_paths) == len(images):
                for i in range(len(images)):
                    if images_paths[i] != images[i]['image_path']:
                        print(images_paths[i], images[i]['image_path'])
                        flag = True
            else: flag = True
            if flag:
                execute_commit(conn, (id,), """
                    DELETE FROM images 
                    WHERE id IN (
                        SELECT pi.image_id
                        FROM postimages pi, images i
                        WHERE pi.image_id=i.id
                        AND pi.post_id=?) """
                )
                execute_commit(conn, (id,), """
                    DELETE FROM postimages 
                    WHERE post_id IN (
                        SELECT pi.post_id
                        FROM postimages pi
                        WHERE pi.post_id=?) """
                )
                for image_path in images_paths:
                    image_id = execute_commit(conn, (image_path,), 
                        "INSERT INTO images(path) VALUES(?)")
                    execute_commit(conn, (id, image_id), 
                        "INSERT INTO postimages(post_id, image_id) VALUES(?,?)")
        return redirect(f"/post/{id}")
    else:
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.full_path))
        conn = get_db()
        post = execute_query_param(conn, (id,), "SELECT * FROM posts WHERE id=?").fetchone()
        if post['account_id'] != session['account'][0]:
            return redirect(f"/post/{id}")
        categories = execute_query(conn, "SELECT * FROM categories").fetchall()
        images = execute_query_param(conn, (id,), """
            SELECT pi.post_id, pi.image_id, i.path image_path
            FROM postimages pi, images i
            WHERE pi.image_id=i.id
            AND pi.post_id=? """
        ).fetchall()
        conn.close()
        return render_template("main/post_edit.html", categories=categories, post=post, images=images)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        account = (email, hashlib.sha1(password.encode()).hexdigest())
        account = execute_query_param_tuple(conn, account, "SELECT * FROM accounts WHERE email=? AND password=?").fetchone()
        conn.close()

        err_msg = []
        if account:
            session['account'] = account
            session['logged_in'] = True
            next_url = request.args.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("/")
        else:
            err_msg.append("Email or password is incorrect.")
            return render_template("auth/login.html", err_msg=err_msg)
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
            err_msg.append("Confirm password is incorrect.")

        if not err_msg:
            conn = get_db()
            with conn:
                account = (username, email, hashlib.sha1(password.encode()).hexdigest())
                try:
                    account_id = execute_commit(conn, account, "INSERT INTO accounts(name, email, password) VALUES(?,?,?)")
                except sqlite3.IntegrityError as err:
                    err_msg.append("Email already exists.")

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
    conn = get_db()
    accounts = execute_query(conn, "SELECT count(*) number FROM accounts ").fetchone()
    comments = execute_query(conn, "SELECT count(*) number FROM comments ").fetchone()
    posts = execute_query(conn, "SELECT count(*) number FROM posts ").fetchone()
    
    popular_accounts = execute_query_param(conn, (post_num,), """
        SELECT a.name account_name, count(s.follower_id) followers_number
        FROM subscriptions s, accounts a
        WHERE  s.author_id=a.id
        GROUP BY s.author_id
        ORDER BY followers_number DESC, account_name
        LIMIT ? """
    ).fetchall()

    categories_pie_chart = execute_query_tuple(conn, """
        SELECT c.name name, count(p.id) posts_number
        FROM posts p, categories c
        WHERE p.category_id=c.id
        GROUP BY category_id """
    ).fetchall()
    labels = []
    values = []
    for category in categories_pie_chart:
        labels.append(category['name'])
        values.append(category['posts_number'])
    pie_data = {'labels': labels, 'values': values}

    year_month__join_count = execute_query_tuple(conn, """
        SELECT strftime('%Y-%m', created_date) Ym, count(id) join_count
        FROM posts 
        GROUP BY Ym
        ORDER BY Ym DESC """
    ).fetchall()
    year_month = []
    join_count = []
    for post in year_month__join_count:
        year_month.append(post['Ym'])
        join_count.append(post['join_count'])
    line_trace = {'x': year_month, 'y': join_count}

    categories__like_count = execute_query_tuple(conn, """
        SELECT c.name name, sum(like_count) like_count 
        FROM posts p, categories c
        WHERE p.category_id=c.id
        GROUP BY p.category_id """
    ).fetchall()
    theta = []
    r = []
    for post in categories__like_count:
        theta.append(post['name'])
        r.append(post['like_count'])
    radar_data = {'theta': theta, 'r': r}

    popular_posts = execute_query_param(conn, (post_num,), """
        SELECT p.title title, a.name account_name, strftime('%Y-%m-%d', created_date) created_date
        FROM posts p, accounts a
        WHERE p.account_id=a.id
        ORDER BY p.like_count + p.view_count DESC
        LIMIT ? """
    ).fetchall()

    return render_template("admin/dashboard.html", accounts=accounts, comments=comments, posts=posts, popular_accounts=popular_accounts, pie_data=pie_data, line_trace=line_trace, radar_data=radar_data, popular_posts=popular_posts)


if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
