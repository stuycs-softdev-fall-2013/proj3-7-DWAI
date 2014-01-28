#!/usr/local/bin/python
from flask import Flask, render_template, session, redirect, request, url_for
import json
from bson import ObjectId
from models import User, Image, Collection

u = User()
img = Image()
models = Collection()

app = Flask(__name__)
app.secret_key = "my secret key"


@app.route('/', methods = ['GET', 'POST'])
def home():
#    if request.method == 'POST':
#        username = request.form['Username'].encode("utf8")
#        password = request.form['Password'].encode("utf8")
#        if u.authenticate(username=username,password=password):
#            session['username'] = username
#            return render_template('index.html', user = username)
#        else:
#            return redirect(url_for('login.html', e = 'Invalid username and password combination'))
    if request.method == "POST":
        wd = request.form["width"]
        ht = request.form["height"]
        return render_template('canvaspg.html', Width = wd, Height = ht)
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

@app.route('/login/<e>',methods=['GET','POST'])
def login(e):
    if e is not None:
        error = e
    else:
        error = ""
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html', error=error)
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

@app.route('/me')
def me():
    #show the user profile for that user
    if 'username' in session:
        obj = img.find(user=session['username'])
        art = []
        for i in obj:
            try:
                art.append(i.image)
            except:
                pass
        x = u.find_one(username=session['username'])
        propic = x.pic
        return render_template('profile.html', user = session['username'], owner = session['username'],art=art, propic = propic)
    else:
        return redirect(url_for('home'))

@app.route('/profile/<name>')
def profile(name):
    if u.exists(name):
        art = img.find(user=name)
        if 'username' in session:
            return render_template('profile.html', user = session['username'], owner = name,art=art)
        else:
            return render_template('profile.html', user= None, owner = name,art=art)
    else:
        return redirect(url_for('home'))

@app.route('/canvas', methods=['GET','POST'])
def canvas():
    if 'username' in session:
        #Don't know if this works
        if request.method == 'POST':
            requestimg = json.load(sys.stdin)
            i = img.insert(user=session['username'],title=request.form['title'])
            i.change_image(requestimg)
        return render_template('canvaspg.html', user=session['username'])
    else:
        return redirect(url_for('login',e='Please log in to use canvas'))

#sample image code
@app.route('/changepic', methods=['GET','POST'])
def changepic():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('changepic.html', user = session['username'])
    if request.method == 'POST':
        x = u.find_one(username = session['username'])
        f = request.files['file']
        x.change_propic(f)
        return redirect(url_for('me'))
    return render_template('changepic.html', user= session['username'])

@app.route('/_image/<image_id>')
def serve_image(image_id):
    image = models.fs.get(ObjectId(image_id))
    data = image.read()
    image.close()
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
