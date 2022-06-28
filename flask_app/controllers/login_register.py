from flask import render_template, redirect, request, session
from flask_app.__init__ import app
from flask_app.models.login_register import user
from flask_bcrypt import Bcrypt
from flask import flash 
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process/new_register', methods=['POST'])
def process_register():
    print(request.form)
    if not user.check_stats(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "confirm_password": request.form['confirm_password']
    }
    id = user.new_user(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/process/login', methods=['POST'])
def process_login():
    user_in_db = user.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

