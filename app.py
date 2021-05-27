from flask import Flask, render_template, request, session, redirect, url_for, g
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_logged_user():
    user_res = None

    if 'user' in session:
        user = session['user']

        db = get_db()
        user_cur = db.execute('select id, name, password, expert, admin from users where name = ?', [user])
        user_res = user_cur.fetchone()

    return user_res

@app.route('/')
def index():
    return render_template('home.html', logged_user=get_logged_user())

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', logged_user=get_logged_user())
    
    if request.method == 'POST':
        values = [
            request.form['name'],
            generate_password_hash(request.form['password'], method='sha256'),
            False,
            False
        ]
        
        db = get_db()
        db.execute(' insert into users (name, password, expert, admin) values (?, ?, ?, ?)', values)
        db.commit()

        session['user'] = request.form['name']

        return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', logged_user=get_logged_user())
    
    if request.method == 'POST':
        db = get_db()
        user_cur = db.execute('select id, name, password from users where name = ?', [request.form['name']])
        user_res = user_cur.fetchone()
        
        if check_password_hash(user_res['password'], request.form['password']):
            session['user'] = user_res['name']

            return redirect(url_for('index'))
        else:
            return '<h1>The password is incorrect!</h1>'

@app.route('/question')
def question():
    return render_template('question.html', logged_user=get_logged_user())

@app.route('/answer')
def answer():
    return render_template('answer.html', logged_user=get_logged_user())

@app.route('/ask', methods=['GET','POST'])
def ask():
    if request.method == 'GET':
        db = get_db()
        experts_cur = db.execute('select id, name from users where expert = 1 order by name')
        experts = experts_cur.fetchall()
        
        return render_template('ask.html', logged_user=get_logged_user(), experts=experts)
    
    if request.method == 'POST':
        logged_user = get_logged_user()

        values = [
            request.form['question'],
            logged_user['id'],
            request.form['expert']
        ]

        db = get_db()
        db.execute('insert into questions ( question_text, questioned_by_id, answered_by_id ) values (?, ?, ?)', values)
        db.commit()

        return redirect(url_for('index'))

@app.route('/unaswered')
def unanswered():
    logged_user = get_logged_user()

    db = get_db()
    questions_cur = db.execute('select q.id, q.question_text, q.questioned_by_id, u.name from questions q join users u on u.id = q.questioned_by_id where q.answered_by_id = ? and q.answer_text is null order by q.id', [logged_user['id']])
    questions = questions_cur.fetchall()
    
    return render_template('unanswered.html', logged_user=logged_user, questions=questions)

@app.route('/users')
def users():
    db = get_db()
    users_cur = db.execute('select id, name, expert, admin from users order by name')
    users = users_cur.fetchall()
    
    return render_template('users.html', logged_user=get_logged_user(), users=users)

@app.route('/promote/<user_id>')
def promote(user_id):
    db = get_db()
    db.execute('update users set expert = 1 where id = ?', [user_id])
    db.commit()
    
    return redirect(url_for('users'))

@app.route('/revoke/<user_id>')
def revoke(user_id):
    db = get_db()
    db.execute('update users set expert = 0 where id = ?', [user_id])
    db.commit()
    
    return redirect(url_for('users'))

@app.route('/logout')
def logout():
    session.pop('user', None)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
