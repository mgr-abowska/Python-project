from flask import Flask,request,render_template

from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app = config['MYSQL_DATABASE_USER'] = 'root'
app = config['MYSQL_DATABASE_PASSWORD'] = 'root'
app = config['MYSQL_DATABASE_DB'] = 'login_data'
app = config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def login_form():
    return render_template('login.html')

@app.route('/',methods=['POST'])
def authorisation():
    username = request.form['user']
    password = request.form['password']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where username='" + username + "'and password='"+ password +"'")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"


if __name__ == "__main__":
    app.run()