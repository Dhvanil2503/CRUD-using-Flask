from flask import Flask,render_template,redirect,url_for,flash,request,Response,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from keys import *
import smtplib, ssl
import hashlib
import requests
import json


app = Flask(__name__)
app.secret_key='flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.sqlite3'
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'  # Replace 'login' with the name of your login route

db=SQLAlchemy(app)
class registration_details(UserMixin,db.Model):
    __tablename__ = 'registration_details'
    id = db.Column('registration_id',db.Integer, primary_key=True)
    Fname= db.Column(db.VARCHAR(30))
    Lname= db.Column(db.VARCHAR(30))
    Gender= db.Column(db.String(10))
    Email= db.Column(db.VARCHAR(30))
    Password= db.Column(db.VARCHAR(256))
    Address= db.Column(db.Text)
    hobbies= db.Column(db.VARCHAR(50))
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self,Fname,Lname,Gender,Email,Password,Address,hobbies):
        self.Fname=Fname
        self.Lname=Lname
        self.Gender=Gender
        self.Email=Email
        self.Password=Password
        self.Address=Address
        self.hobbies=hobbies

    def get_id(self):
        return self.id
    
@login_manager.user_loader
def load_user(registration_id):
    return registration_details.query.get(int(registration_id))

def prevent_login_page_access(f):
    @wraps(f)
    def decorated_function(*args , **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('joke'))
        return f(*args,**kwargs)
    return decorated_function




@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('joke'))  # Redirect to the joke page or any other page
    return render_template('login.html')

@app.route('/login', methods= ['GET','POST'])
@prevent_login_page_access
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('joke'))  # Redirect to the joke page or any other page
    # return render_template('login.html')
        user_email = request.form['eml']
        user_pass = request.form['paswrd']

        hash_pass = hashlib.md5(user_pass.encode()).hexdigest()
        user = registration_details.query.filter_by(Email=user_email, Password=hash_pass).first()
        if not user:
            flash ('Invalid Email or password. Please try again!','danger')
        elif not user.is_active:
            flash('You are not logged in, Please login.','danger')
        else:
            login_user(user)
            session['logged_in'] = True
            flash('login successfully','success')
            return redirect(url_for('joke'))

        # if(user):
        #     flash('login successfully','success')
        #     session['user_id'] = user.id  # Storing user ID in session
        #     return redirect(url_for('joke'))
        #     # return render_template('joke.html')
        # else:
        #     flash('Enter wrong email or password','danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # if 'user_id' in session:
        session.pop('logged_in', None)
        logout_user()
        flash('You have been logged out', 'success')
        return render_template('login.html')    
    # else:
        # flash('You are not currently logged in', 'info')
   

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/joke', methods=['GET', 'POST'])
@login_required
def joke():
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}
    
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                joke_data = response.json()
                joke = joke_data['joke']
                return render_template('Joke.html', joke=joke)
            else:
                flash('You must be logged in to access this page', 'danger')
                # flash("Failed to fetch a joke. Please try again later.", 'danger')
                return redirect('/')
        except requests.exceptions.RequestException as e:
            flash(f"Failed to fetch a joke: {e}", "error")
            return redirect('/')
        

@app.route('/register',methods=['GET','POST'])
@prevent_login_page_access
def register():
    if request.method == 'POST':
        if not request.form['gender'] or not request.form['email'] or not request.form['password'] or not request.form['cnfmpass'] :
            flash('all fields require', 'danger')

        else:
            hobby = request.form.getlist('hobbies')
            hobby_csv = ','.join(hobby)

            password= request.form['password']
            h= hashlib.md5()
            h.update(password.encode())
            encod_pass=h.hexdigest()


            user=registration_details(request.form['fname'],request.form['lname'],request.form['gender'],request.form['email'],encod_pass,request.form['address'],hobby_csv)
          
        
            db.session.add(user)

            db.session.commit()
            send_mail()

            flash('Register successfully','success')
            return render_template('login.html')
    return render_template('registration.html')
    
def send_mail():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = send_email # Enter your address
    receiver_email = request.form['email']  # Enter receiver address
    password = gmail_pass
    message = """Subject: Registration Confirmation

        This email is sent by Dhvanil.
        You have been successfully registered with my internship project
        Thank you for Registration.
    ."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
    with app.app_context():
     db.create_all()
     app.run(debug=True)
    #  app.run(port=5000)