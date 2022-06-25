from flask import render_template, redirect, request, session
from flask_app.models.painting import painting
from flask_app.models.login_register import user
from flask_app.__init__ import app

@app.route ('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', paintings = painting.get_all_paintings(), user = user.get_by_id(session['user_id']), own_paintings = painting.get_all_paintings_owned(session['user_id']))

@app.route ('/dashboard/new/painting')
def new_painting():
    return render_template('new_painting.html', user = user.get_by_id(session['user_id']))

@app.route ('/dashboard/new/painting/process', methods=["POST"])
def new_painting_prcoess():
    if not painting.check_stats_painting(request.form):
        return redirect('/dashboard/new/painting')
    painting.new_painting(request.form)
    return redirect('/dashboard')

@app.route('/dashboard/edit/painting/<id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('edit_painting.html',painting = painting.get_painting(id), creater = user.get_by_id(session['user_id']))

@app.route ('/dashboard/edit/painting/process/<id>', methods=["POST"])
def edit_painting_prcoess(id):
    if not painting.check_stats_painting(request.form):
        return redirect('/dashboard/edit/painting/'+str(request.form['id']))
    painting.edit_painting(request.form)
    return redirect('/dashboard')

@app.route('/dashboard/painting/<id>')
def painting_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('painting.html',painting = painting.get_painting(id), creater = user.get_by_id(session['user_id']))

@app.route('/buy/<id>')
def buy_painting(id):
    id = id
    data = {
        'user_id': session['user_id'],
        'painting_id': id
    }
    painting.buy_painting(data)
    return redirect('/dashboard/painting/'+str(id))

@app.route('/sell/<id>')
def sell_painting(id):
    id = id
    data = {
        'user_id': session['user_id'],
        'painting_id': id
    }
    painting.sell_painting(data)
    return redirect('/dashboard/painting/'+str(id))

@app.route('/dashboard/delete/<id>/process')
def delete_show_process(id):
    painting.delete_owned_paintings(id)
    painting.delete_painting(id)
    return redirect("/dashboard")