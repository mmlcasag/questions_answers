from flask import Flask, render_template, request
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
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
        close_db()

        return '<h1>User created!</h1>'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/answer')
def answer():
    return render_template('answer.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')

@app.route('/unaswered')
def unanswered():
    return render_template('unaswered.html')

@app.route('/users')
def users():
    return render_template('users.html')

if __name__ == '__main__':
    app.run(debug=True)
