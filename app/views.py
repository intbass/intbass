#!venv/bin/python

from functools import wraps
from flask import render_template, request, Response, \
    flash, session, redirect, g, url_for, json
from flask.ext.login import login_user, logout_user, current_user
from forms import LoginForm, FileForm, UserEditForm
from app import app, db, lm
from app.util import admin_required
from models import Users, File, FileError

from sqlalchemy import create_engine, text
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from icealchemy import Base, Station, Listener, Mount

import re
import os
import logging

logger = logging.getLogger()


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       convert_unicode=True)
sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.errorhandler(401)
def forbidden(error='Unauthorized'):
    return Response(error, 401, {'WWW-Authenticate': 'None'})


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/admin/', methods=['GET'])
@admin_required
def admin():
    return render_template('admin.html')


@app.route('/admin/files', methods=['GET'])
@admin_required
def admin_files():
    thefiles = []
    path = app.config['FILE_PATH']

    for root, dirs, files in os.walk(path, followlinks=True):
        for f in files:
            if f.endswith('.mp3'):
                thefiles.append(os.path.relpath(os.path.join(root, f), path))

    return render_template('admin/files/index.html',
                           files=thefiles)


@app.route('/admin/files/<path:path>', methods=['GET', 'POST'])
@admin_required
def admin_file(path):
    shortname = os.path.join(app.config['FILE_PATH'], path)
    try:
        file = File(shortname)
    except FileError as e:
        # flash('Error opening file %s - %s') % (str(shortname), str(e))
        # flash('Error opening file ' + str(shortname) + ' - ' + str(e.value))
        flash(e.value)
        return redirect(url_for('admin_files'))
    # except:
    #    flash('Error opening file ' + shortname)
    #    return redirect(url_for('admin_files'))

    form = FileForm(obj=file)
    return render_template('admin/files/file.html', file=file, form=form)


@app.route('/admin/users/', methods=['GET', 'POST'])
@admin_required
def admin_users():
    users = Users.query.all()
    return render_template('admin/users.html',
                           users=users)


@app.route('/admin/users/edit/<id>', methods=['GET', 'POST'])
@admin_required
def edituser(id):
    user = load_user(id)
    form = UserEditForm()
    # if form.validate_on_submit():
    if form.is_submitted():
        if form.name.data != user.name:
            try:
                user.name = form.name.data
                db.session.commit()
                flash('Username change from ' + user.name + ' to ' +
                      form.name.data, 'success')
            except:
                flash('Username change error', 'error')
        if form.password.data != '':
            try:
                user.password = form.password.data
                db.session.commit()
                flash('Password changed', 'success')
            except:
                flash('Password change error.', 'error')
        if form.email.data != user.email:
            try:
                user.email = form.email.data
                db.session.commit()
                flash('Email changed to ' + user.email, 'success')
            except AssertionError:
                flash('Invalid email address', 'error')
            except:
                flash('Email change error', 'error')
        if form.location.data != user.location:
            try:
                user.location = form.location.data
                db.session.commit()
                flash('Location changed to ' + user.location, 'success')
            except:
                flash('Location change error', 'error')

        return render_template('admin/users/edit.html',
                               form=form,
                               user=user)
    else:
        form = UserEditForm(obj=user)
        return render_template('admin/users/edit.html',
                               form=form,
                               user=user)


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
        password = request.form['password']
        user = Users.query.filter_by(name=username).first()
        if user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        if not user.authenticate(password):
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        login_user(user)
        session['remember_me'] = form.remember_me.data
        return redirect('/home')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect('/home')


def makeresponse(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        data = fn(*args, **kwargs)
        if type(data) == Response:
            return data

        content = request.headers.get('Content-Type')
        accept = request.headers.get('Accept')
        callback = request.args.get('callback', False)
        if callback:
            return Response(str(callback) + '(' + json.dumps(data) + ');',
                            status=200, mimetype='application/json')

        if accept is None or content == 'text/plain':
            resp = Response(json.dumps(data),
                            status=200, mimetype='text/plain')
            resp.headers.set('Content-Disposition',
                             'attachment; filename="api.txt"')
            return resp

        elif 'application/json' in accept:
            return Response(json.dumps(data), status=200,
                            mimetype='application/json')

        elif "text/html" in accept:
            js = json.dumps(data)
            return """<html>
                <body>%s</body>
               </html>""" % js

        else:
            return Response("Unsupported Media Type", status=415)

    return wrapped


def passsession(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        s = session()
        args = [s] + list(args)
        data = fn(*args, **kwargs)
        s.close()
        return data
    return wrapped


@app.route('/stations')
@makeresponse
@passsession
def stations(s):
    return s.query(Station.tag, Station.name).all()


@app.route('/station/<tag>/listeners', methods=['GET'])
@makeresponse
@passsession
def listeners(s, tag):
    if tag == 'all':
        listeners = s.query(Listener.lat, Listener.long, func.count('*')).join(Mount).join(Station)\
                     .filter(text("listeners.last > now() - INTERVAL '30 seconds'"))\
                     .group_by(Listener.lat, Listener.long).all()
    else:
        listeners = s.query(Listener.lat, Listener.long, func.count('*')).join(Mount).join(Station)\
                     .filter(Station.tag == tag)\
                     .filter(text("listeners.last > now() - INTERVAL '30 seconds'"))\
                     .group_by(Listener.lat, Listener.long).all()
    result = []
    count = 0
    for listener in listeners:
        if listener[2] > count:
            count = listener[2]
        result.append({'lat': listener[0], 'lng': listener[1],
                       'count': listener[2]})
    return {'max': count, 'data': result}


@app.route('/station/<tag>')
@makeresponse
@passsession
def station(s, tag):
    station = s.query(Station).filter_by(tag=tag).first()
    if station is None:
        return Response('Not found', 404)
    result = station.dict()
    if station is None:
        return Response('Not found', status=404)
    result['listeners'] = s.query(Listener).join(Mount)\
                           .filter(Mount.stationid == station.id)\
                           .filter(text("listeners.last > now() - INTERVAL '30 seconds'"))\
                           .count()
    return result


@app.route('/pls/<channel>')
@passsession
def pls(s, channel):
    match = re.match(r'([^-]+)-(mp3|ogg)-(hig?h?|low?)', channel)
    if match is not None:
        tag = match.group(1)
        format = match.group(2)
        quality = match.group(3)
        mounts = s.query(Mount).join(Station)\
                  .filter(Mount.stationid == Station.id)\
                  .filter(Station.tag == tag)\
                  .filter(Mount.published is True)\
                  .filter(Mount.url.like('%-'+format+'-%'))\
                  .filter(Mount.url.like('%-'+quality))\
                  .order_by(Mount.preference)
        mount_count = mounts.count()
    pls = "[playlist]\nnumberofentries="+str(mount_count)+"\n"
    idx = 0
    for mount in mounts:
        app.logger.warning('title:%s', mount.title)
        app.logger.warning('URL:%s', mount.url)
        if mount.url is not None and mount.title is not None:
            idx = idx + 1
            i = str(idx)
            pls += 'File'+i+'='+mount.url + \
                   "\nTitle"+i+'='+mount.title + \
                   "\nLength"+i+"=-1\n"
    resp = Response(pls,
                    status=200, mimetype='audio/x-scpls')
    resp.headers.set('Content-Disposition',
                     'inline; filename="intbass.pls"')
    return resp


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    logging.basicConfig(filename='/tmp/poo')
    app.run(debug=True)
