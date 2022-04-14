from flask import Flask, request, send_from_directory, render_template, redirect, url_for, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
from time import time
import mysql.connector, json, sys
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
    

    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)
     
    query = ("SELECT user_id, balance FROM account WHERE username = %s")
    cursor.execute(query, (github_user["login"], ))
    if cursor.rowcount > 0:
        (user_id, balance) = cursor.fetchone()
        
    categories = []
    query = ("SELECT category_id, category_name FROM category ORDER BY category_id")
    cursor.execute(query)
    rows = cursor.fetchall()
    for (category_id, category_name) in rows:
        categories.append({"id": category_id, "name": category_name})
        
    return render_template('pay.html', title=' - Send payment', login=github_user['login'], categories=categories)
 


@app.route("/schedule")
def schedule():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()
    

    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)
     
    query = ("SELECT user_id, balance FROM account WHERE username = %s")
    cursor.execute(query, (github_user["login"], ))
    if cursor.rowcount > 0:
        (user_id, balance) = cursor.fetchone()
        
    categories = []
    query = ("SELECT category_id, category_name FROM category ORDER BY category_id")
    cursor.execute(query)
    rows = cursor.fetchall()
    for (category_id, category_name) in rows:
        categories.append({"id": category_id, "name": category_name})
        
    return render_template('schedule.html', title=' - Schedule payment', login=github_user['login'], categories=categories)
 
 
@app.route("/history")
def history():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()

        
    return render_template('history.html', title=' - Payment history', login=github_user['login'])
 
 
 
@app.route("/budget")
def budget():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()

        
    return render_template('budget.html', title=' - Budget', login=github_user['login'])
 
 
 
@app.route("/search", methods=['GET'])
def search():
    if not github.authorized:
        return redirect('/login')
    
    github_user = github.get("/user").json()

    args = request.args
    term = args["term"]
    
    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)
     
    query = ("SELECT COUNT(*) FROM account WHERE username LIKE %s")
    results = cursor.execute(query, (term+"%", ))
    (count, ) = cursor.fetchone()
    
    if count == 1:
        # print("a"+str(count), file=sys.stderr)
        query = ("SELECT username FROM account WHERE username LIKE %s")
        results = cursor.execute(query, (term+"%", ))
        (username, ) = cursor.fetchone()
        result = [{"label": username, "value": username, "id": username}]
    else:
        # print("b"+str(count), file=sys.stderr)
        result = [] 
    
    cursor.close()
    cnx.close()
    
    return json.dumps(result) 
 
 
  
# main driver function
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
