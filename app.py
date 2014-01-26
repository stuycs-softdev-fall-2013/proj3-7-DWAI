#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
import json
import auth

app = Flask(__name__)
app.secret_key = "my secret key"


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if auth.authenticate(username,password):
            session['username'] = username
            return render_template('index.html', user = username)
        else:
            return render_template('login.html', user = None, message = 'Invalid username and password combination')
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
    if not auth.adduser(request.form['username'],request.form['password']):
	return render_template('register.html', error='Username already exists')
    session['username'] = request.form['username']
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    if not auth.authenticate(request.form['username'],request.form['password']):
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
    usererror = None
    passerror = None
    usersuccess = None
    pwsuccess = None
    if request.form['newuser']:
        if not auth.changeuser(request.form['oldpw'],
		session['username'],
                request.form['newuser']):
            usererror = 'Username change unsuccessful. Check your password.'
        else:
            session['username'] = request.form['newuser']
            usersuccess = 'Username successfully changed to: ' + request.form['newuser']
    if request.form['newpw']:
	if request.form['newpw'] != request.form['confirm']:
	    passerror = 'Passwords do not match.'
        elif not auth.changepass(session['username'],
		request.form['oldpw'],
		request.form['newpw']):
	    passerror = 'Password change unsuccessful. Check your password.'
	else:
            pwsuccess= 'Password successfully changed.'
    return render_template('changeinfo.html', user=session['username'],usererror=usererror, passerror=passerror, usersuccess=usersuccess, pwsuccess=pwsuccess)

@app.route('/user/<username>')
def show_user_profile(usernname):
    #show the user profile for that user
    pass

@app.route('/canvas')
def canvas():
    return render_template('canvaspg.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
