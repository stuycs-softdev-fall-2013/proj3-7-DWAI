from flask import Flask, session, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        user = session['username']
        return render_template('home.html', user = user)
    else:
        render_template('home.html', use = None)

@app.route('/login')
def login():
    if 'username' in session: 
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['Username']
    password = request.form['Password']
    if auth.auth(username,password):
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html', message = 'Invalid username and password combination')

@app.route('/register')
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['Username']
    password = request.form['Password']
    cpassword = request.form['CPassword']
    if auth.exists(username):
        return render_template('register.html', message = 'Username already exists')
    
    if password != cpassword:
        return render_template('register.html', message = 'Passwords do not match')
    auth.addUser(username, password)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home.html'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
