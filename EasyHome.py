import gc

import MySQLdb
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mysqldb import MySQL
from jinja2 import Environment
from requests import Session
from wtforms import Form, TextField, validators, PasswordField, BooleanField, StringField, form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart, connection
from functools import wraps

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = "Easyhome_db"
mysql = MySQL(app)
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])


@app.route('/',methods=['GET'])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT address,housetype,rentfee,id from post_ad_table")
    data = cursor.fetchall()
    x = len(data)
    print(x)
    if x>5:
        li = range(x-5, x)
        li= [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    return render_template("index.html",data=data,li=li)



g_data=""
id_n=""
@app.route('/data_rcv', methods=['GET'])
def data_rcv():
    homeId = request.args['query']
    id_n = homeId.split()
    print(id_n)
    return redirect('/description/'+str(id_n[2]))

@app.route('/description_main/<string:name>/', methods = ['GET','POST'])
def description_main(name):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT address,housetype,contact from post_ad_table WHERE id=%s", [name])
    g_data = cursor.fetchall()
    print(g_data)
    return render_template("description_main.html",g_data=g_data)
#
# @app.route('/des_test', methods = ['GET'])
# def des_test():
#     return render_template("des_test.html")



@app.route('/profile_main',methods=['GET'])
def profile_main():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT name,username,email,Mobile_no,Address from resistration_db  WHERE username = %s",[session['username']])
    data = cursor.fetchall()
    #profile newsfeed
    cursor.execute(
        "SELECT address,housetype,rentfee,id from post_ad_table WHERE username=%s", [session['username']])
    data_n = cursor.fetchall()
    x = len(data_n)
    print(x)
    if x>5:
        li = range(x-5, x)
        li= [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()
    return render_template("profile_main.html",data=data,data_n=data_n,li=li)




@app.route('/search_dhaka',methods=['GET', 'POST'])
def search_dhaka():
    if request.method == 'POST':
        # Get Form Fields
        area = request.form.get('area')
        housetype = request.form.get('housetype')

        # Create cursor
        cur1 = mysql.connection.cursor()

        # Get user by username
        cur1.execute(
            "SELECT address,housetype,rentfee,id FROM post_ad_table where (housetype, area)=(%s, %s)",
            (housetype, area))
        data=cur1.fetchall()

        x= len(data)
        print(x)
        if x > 5:
            li = range(0, 5)
        else:
            li = range(0, x)
        return render_template("search_dhaka.html",data=data,li=li)
    return render_template("search_dhaka.html")


@app.route('/search_sylhet',methods=['GET', 'POST'])
def search_sylhet():
    if request.method == 'POST':
        # Get Form Fields
        area = request.form.get('area')
        housetype = request.form.get('housetype')

        # Create cursor
        cur1 = mysql.connection.cursor()

        # Get user by username
        cur1.execute(
            "SELECT address,housetype,rentfee,id FROM post_ad_table where (housetype, area)=(%s, %s)",
            (housetype, area))
        data=cur1.fetchall()

        x= len(data)
        print(x)
        if x > 5:
            li = range(0, 5)
        else:
            li = range(0, x)
        return render_template("search_sylhet.html",data=data,li=li)
    return render_template("search_sylhet.html")

@app.route('/search_chittagong',methods=['GET', 'POST'])
def search_chittagong():
    if request.method == 'POST':
        # Get Form Fields
        area = request.form.get('area')
        housetype = request.form.get('housetype')

        # Create cursor
        cur1 = mysql.connection.cursor()

        # Get user by username
        cur1.execute(
            "SELECT address,housetype,rentfee,id FROM post_ad_table where (housetype, area)=(%s, %s)",
            (housetype, area))
        data=cur1.fetchall()

        x= len(data)
        print(x)
        if x > 5:
            li = range(0, 5)
        else:
            li = range(0, x)
        return render_template("search_chittagong.html",data=data,li=li)
    return render_template("search_chittagong.html")

@app.route('/search_barisal',methods=['GET', 'POST'])
def search_barisal():
    if request.method == 'POST':
        # Get Form Fields
        area = request.form.get('area')
        housetype = request.form.get('housetype')

        # Create cursor
        cur1 = mysql.connection.cursor()

        # Get user by username
        cur1.execute(
            "SELECT address,housetype,rentfee,id FROM post_ad_table where (housetype, area)=(%s, %s)",
            (housetype, area))
        data=cur1.fetchall()

        x= len(data)
        print(x)
        if x > 5:
            li = range(0, 5)
        else:
            li = range(0, x)
        return render_template("search_barisal.html",data=data,li=li)
    return render_template("search_barisal.html")





# User Register
# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    mobileno = StringField('Mobile No.', [validators.Length(min=1, max=50)])
    address = StringField('Address', [validators.Length(min=1, max=50)])


@app.route('/post_ad', methods=['GET', 'POST'])
def post_ad():
    if request.method == 'POST':
        # Get Form Fields
        address = request.form['address']
        housetype = request.form.get('housetype')
        description = request.form['description']
        rentfee = request.form['rentfee']
        contactinformation = request.form['contactinformation']
        division = request.form.get('division')
        district = request.form.get('district')
        area = request.form.get('area')
        username = [session['username']]

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute(
            "INSERT INTO post_ad_table( address, housetype, description, rentfee, contact, division, district, area, username) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (address, housetype, description, rentfee, contactinformation, division, district, area, username))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return render_template("index.html")
    return render_template("post_ad.html")


# User loginmain
@app.route('/loginmain', methods=['GET', 'POST'])
def loginmain():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM resistration_db WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[3]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return render_template('index.html')
            else:
                error = 'Invalid login'
                return render_template('loginmain.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('index.html', error=error)

    return render_template('loginmain.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('logintransparent'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return render_template('index.html')

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
   return render_template("dashboard.html")


@app.route('/registertrans', methods=['GET', 'POST'])
def registertrans():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobileno = form.mobileno.data
        address= form.address.data


        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO resistration_db( name, username, email, password, Mobile_no, Address) VALUES(%s, %s, %s, %s, %s, %s)", (name,  username, email, password, mobileno,address))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('logintransparent'))
    return render_template('registertrans.html', form=form)


# User loginmain
@app.route('/logintransparent', methods=['GET', 'POST'])
def logintransparent():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM resistration_db WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[3]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return render_template('index.html')
            else:
                error = 'Invalid login'
                return render_template('logintransparent.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('logintransparent.html', error=error)

    return render_template('logintransparent.html')





if __name__ == '__main__':
    app.secret_key='secret123'
    app.run()
