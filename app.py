from flask import Flask,render_template,request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from database import Database

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        data1 = Database.find_one("test", {"username": username})
        data2 = Database.find_one("test", {"email": email})

        if (data1 or data2) is None:
            Database.insert("test", {'name': name, 'email': email, 'username': username, 'password': password})
            session['email'] = email

            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))

        flash('Either Username or Email is already registered in the system!')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        data = Database.find_one("test", {"username": username})

        #result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        

        if data is not None:
            # Get stored hash
            #data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                #return redirect(url_for('dashboard'))
                return redirect(url_for('about'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = Null
    session['username'] = Null
    return render_template('home.html')


if __name__ == "__main__":
    
    app.run(debug=True)
