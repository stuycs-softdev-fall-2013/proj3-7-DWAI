#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
import json


app = Flask(__name__)
app.secret_key = "SECRET_KEY"


@app.route('/')
def home():
    if not 'username' in session:
        return render_template('index.html', user=None)
    else:
        user = users.find_one(username=session['username'])
        return render_template('index.html', user=user)


@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('register.html')
    if users.exists(request.form['username']):
        return render_template('register.html', error='Username already exists')
    if request.form['password'] != request.form['confirm']:
        return render_template('register.html', error='Passwords do not match')
    session['username'] = request.form['username']
    users.insert(username=request.form['username'],
            password=request.form['password'])
    return redirect(url_for('home'))


@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    u = users.find_one(username=request.form['username'],
            password=request.form['password'])
    if not u:
        return render_template('login.html',
                error='Incorrect username or password')
    session['username'] = request.form['username']
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))


# For the user to change personal information
@app.route('/changeinfo', methods=['GET', 'POST'])
def changeinfo():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('changeinfo.html',user=session['username'])
    u = users.find_one(username=session['username'])
    error = None
    usererror = None
    passerror = None
    usersuccess = None
    pwsuccess = None
    if u.password == request.form['oldpw']:
        if request.form['newuser']:
            if not u.change_username(request.form['oldpw'],
                    request.form['newuser']):
                usererror = 'Username change unsuccessful.'
            else:
                session['username'] = request.form['newuser']
                usersuccess = 'Username successfully changed to: ' + request.form['newuser']
        if request.form['newpw']:
            if not u.change_password(request.form['oldpw'], request.form['newpw'],
                    request.form['confirm']):
                passerror= 'Passwords do not match.'
            else:
                pwsuccess= 'Password successfully changed.'
    else:
        error = 'Incorrect password'
    return render_template('changeinfo.html', user=session['username'],error=error, usererror=usererror, passerror=passerror, usersuccess=usersuccess, pwsuccess=pwsuccess)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
