#!flask/bin/python 

from flask import render_template, request, flash, session, redirect, g, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, IPForm, UserEditForm
from hashlib import sha256
from app import app, db, lm
from models import Users, ROLE_USER, ROLE_ADMIN, File, FileError

import os

#app = Flask(__name__)      

@app.before_request
def before_request():
    g.user = current_user
 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
# an @admin_required construct would seem more useful
def admin():
    users = Users.query.all()
    #users = Users.query.order_by(Users.name).all()

    return render_template('admin.html',
            users = users)

@app.route('/admin/files', methods=['GET'])
@login_required
def admin_files():
    thefiles = []
    path = app.config['FILE_PATH']

    for root, dirs, files in os.walk(path, followlinks=True):
        for f in files:
            thefiles.append(os.path.relpath(os.path.join(root, f), path))

    return render_template('admin/files/index.html',
                           files=thefiles)

@app.route('/admin/files/<path:path>', methods=['GET', 'POST'])
@login_required
def admin_file(path):
    shortname = os.path.join(app.config['FILE_PATH'],path)
    try:
        file = File(shortname)
    except FileError as e:
        #flash('Error opening file %s - %s') % (str(shortname), str(e))
        #flash('Error opening file ' + str(shortname) + ' - ' + str(e.value))
        flash(e.value)
        return redirect(url_for('admin_files'))
    #except:
    #    flash('Error opening file ' + os.path.join(app.config['FILE_PATH'],path) )
    #    return redirect(url_for('admin_files'))

    return render_template('admin/files/file.html', file=file)

@app.route('/admin/users/', methods=['GET', 'POST'])
@login_required
def admin_users():
    users = Users.query.all()
    return render_template('admin/users.html',
            users = users)

@app.route('/admin/users/edit/<id>', methods=['GET', 'POST'])
@login_required
def edituser(id):
    user = load_user(id)
    form = UserEditForm()
    #if form.validate_on_submit():
    if form.is_submitted():
        if form.username.data != user.name:
            try:
                user.name=form.username.data
                db.session.commit()
                flash('Username change from ' + user.name + ' to ' + form.username.data, 'success')
            except:
                flash('Username change error', 'error')
        if form.password.data != '':
            try:
                user.password = sha256(request.form['password']).hexdigest()
                db.session.commit()
                flash('Password changed', 'success')
            except:
                flash('Password change error.', 'error')
        if form.email.data != user.email:
            try:
                user.email = form.email.data
                db.session.commit()
                flash('Email changed to ' + user.email, 'success')
            except:
                flash('Email change error', 'error')
        if form.location.data != user.location:
            try:
                user.location = form.location.data
                db.session.commit()
                flash('Location changed to ' + user.location, 'success')
            except:
                flash('Location change error', 'error')
        if int(form.role.data) != user.role:
            try:
                user.role = int(form.role.data)
                db.session.commit()
                flash('Role changed to ' + str(user.role), 'success')
            except:
                flash('Role change error', 'error')

        return render_template('admin/users/edit.html',
                form = form,
                user = user)
    else: 
        form = UserEditForm(username = user.name,
        role = user.role,
        email = user.email,
        location = user.location)
        return render_template('admin/users/edit.html',
            form = form,
            user = user)

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = sha256(request.form['password']).hexdigest()
        user = Users.query.filter_by(name=username, password=password).first()
        if user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(user)
        session['remember_me'] = form.remember_me.data
        #flash('Login requested for user {}'.format(form.username))
        return redirect('/home')
    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')


 
if __name__ == '__main__':
    app.run(debug=True)
