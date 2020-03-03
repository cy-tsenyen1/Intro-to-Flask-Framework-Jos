from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from data import newsArticles
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

app = Flask(__name__)
#configuring MySQL logic
app.config['SECRET_KEY'] = 'Your_secret_string'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Cyril'
app.config['MYSQL_PASSWORD'] = 'Cyril@2580#'
app.config['MYSQL_DB'] = 'FlaskDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initializing mysql
mysql = MySQL(app)

# newsArticles=newsArticles()

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/articles")
def articles():
# newsArticles=newsArticles()
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute ("SELECT * FROM articles")
    views = cur.fetchall()
    if result:
        return render_template("newsfeed.html", articles= views)
    else:
        msg = "No article found"
        return render_template("newsfeed.html", msg=msg)
    #close connection
    cur.close()


@app.route("/article/<string:id>/")
def article(id):
    return render_template("article.html", article=article, id=id)

class MyForm(Form):
    name = StringField(u"Name", validators=[validators.input_required(), validators.Length(min=3, max=50)])
    email = StringField(u"Email", validators=[validators.input_required(), validators.Length(min=3, max=50)])
    username = StringField(u"Username", validators=[validators.input_required(), validators.Length(min=3, max=50)])
    password = PasswordField("Password", [validators.DataRequired(), validators.EqualTo("confirm", message="Passwords do not match")
    ])
    confirm = PasswordField("Confirm Password")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = MyForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt (str(form.password.data))

        cur = mysql.connection.cursor()
        verify = cur.execute("SELECT * FROM users WHERE username =%s or email =%s", (username, email))
        if verify:
            flash('User already registered', 'danger')
            return redirect(url_for("login"))
        else:    
            # execute query
            
            cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
            #commit to db
            mysql.connection.commit()
            #close connection
            cur.close()
            
            #flash message
            flash("You are Successfully Registered", "success")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)
    
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", "danger")
        return redirect(url_for('login'))
    return wrap    


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #get the form field
        username = request.form["username"]
        password_candidate = request.form["password"]

        #create cursor
        cur = mysql.connection.cursor()

        #Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            #Get the hash
            data =cur.fetchone()
            password = data['password']
            #comparing password
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info("password matched")
                session['logged_in'] = True
                session['username'] = username
                flash ('Your are Successfully Logged in', 'success')
                return redirect(url_for("dashboard"))
                
            else:
                error = "invalid login credential"
                return render_template("login.html", error=error)
                # app.logger.info("password mismatched")  logger is a development tool to check pw

        else:
            error = "user not found"
            return render_template("login.html", error=error)
            # app.logger.info("user not found")
            # flash("Username Not Found", 'danger')
    return render_template("login.html")
    



    #logged 0ut
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template("dashboard.html")




class ArticleForm(Form):
    title = StringField(u"Title", validators=[validators.input_required(), validators.Length(min=3, max=200)])
    body = TextAreaField(u"Body", validators=[validators.input_required(), validators.Length(min=30)])


@app.route('/add_article', methods=["GET", "POST"])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        #create cursor
        cur = mysql.connection.cursor()
        #execute
        cur.execute ("INSERT INTO articles(title,body,author)VALUES(%s, %s, %s)", (title, body, session['username']))
        #commit to db
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("Article Created", 'success')
        return redirect(url_for("dashboard"))
    return render_template('add_article.html', form=form)

    
if __name__ == "__main__":
    app.secret_key = 'secret12345'
    app.run(debug=True)

