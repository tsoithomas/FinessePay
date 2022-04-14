from flask import Flask, request, send_from_directory, render_template, redirect, url_for, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
from time import time
import mysql.connector
import config

# app = Flask(__name__)
app = Flask(__name__,
            static_url_path='', 
            static_folder='assets',
            template_folder='views')
CORS(app)
app.secret_key = config.SECRET_KEY
app.config["GITHUB_OAUTH_CLIENT_ID"] = config.GITHUB_CLIENT_ID
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = config.GITHUB_CLIENT_SECRET
blueprint = make_github_blueprint()
app.register_blueprint(make_github_blueprint(), url_prefix="/login")


        
@app.route("/")
def index():
    if github.authorized:
        github_user = github.get("/user").json()
        
        cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        cursor = cnx.cursor(buffered=True)
         
        
        query = ("SELECT user_id, balance FROM account WHERE username = %s")
        results = cursor.execute(query, (github_user["login"], ))
        if cursor.rowcount > 0:
            (user_id, balance) = cursor.fetchone()
        else:
            query = ("INSERT IGNORE INTO account(username, nickname, balance, budget) VALUES (%s, %s, 1000, 0)")
            cursor.execute(query, (github_user["login"], github_user["name"]))
            cnx.commit()   

        
        cursor.close()
        cnx.close()
        
        
        return render_template('index.html', title = ' - Index', login = github_user['login'], balance=balance)
    else:
        return render_template('index.html', title = ' - Index')

@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))

        
    return redirect('/')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route("/pay")
def pay():
    if not github.authorized:
        return redirect('/login')
    github_user = github.get("/user").json()
    return render_template('pay.html', title = ' - Send payment', login = github_user['login'])
 


 
  
# main driver function
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
