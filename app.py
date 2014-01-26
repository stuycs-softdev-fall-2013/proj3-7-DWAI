#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
import json
from models import User

u = User()

app = Flask(__name__)
app.secret_key = "my secret key"


@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if u.authenticate(username=username,password=password):
            session['username'] = username
            return render_template('index.html', user = username)
        else:
            return render_template('login.html', user = None, error = 'Invalid username and password combination')
    if not 'username' in session:
        return render_template('index.html', user=None)
    else:
        user = session['username']
        return render_template('index.html', user=user)


@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('register.html')
    if request.form['password'] != request.form['confirm']:
        return render_template('register.html', error='Passwords do not match')
    if u.exists(username=request.form['username']):
	return render_template('register.html', error='Username already exists')
    session['username'] = request.form['username']
    u.insert(username=request.form['username'], password=request.form['password'])
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    if not u.authenticate(request.form['username'],request.form['password']):
        return render_template('login.html',
                error='Invalid username and password combination')
    session['username'] = request.form['username']
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))


@app.route('/changeinfo', methods=['GET', 'POST'])
def changeinfo():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('changeinfo.html',user=session['username'])
    x = u.find_one(username=session['username'])
    error = None
    usererror = None
    passerror = None
    usersuccess = None
    pwsuccess = None
    if x.password == request.form['oldpw']:
        if request.form['newuser']:
            if not x.change_username(request.form['oldpw'],
                    request.form['newuser']):
                usererror = 'Username already exists.'
            else:
                session['username'] = request.form['newuser']
                usersuccess = 'Username successfully changed to: ' + request.form['newuser']
        if request.form['newpw']:
            if not x.change_password(request.form['oldpw'], request.form['newpw'],
                    request.form['confirm']):
                passerror= 'Passwords do not match.'
            else:
                pwsuccess= 'Password successfully changed.'
    else:
        error = 'Incorrect password'
    return render_template('changeinfo.html', user=session['username'],error=error, usererror=usererror, passerror=passerror, usersuccess=usersuccess, pwsuccess=pwsuccess)

@app.route('/profile')
def profile():
    #show the user profile for that user
    if 'username' in session:
        return render_template('profile.html', user = session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/canvas')
def canvas():
    return render_template('canvaspg.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
