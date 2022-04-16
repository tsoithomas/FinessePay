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
        
    cursor.close()
    cnx.close()
        
    return render_template('pay.html', title=' - Send payment', login=github_user['login'], categories=categories)
 

@app.route("/pay_submit", methods=['POST'])
def pay_submit():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()
    
    payer = get_user(github_user['login'])
    print(payer, file=sys.stderr)
    payer_id = payer["user_id"]
    
    payee = get_user(request.form.get('payee'))
    payee_id = payee["user_id"]
    
    amount = request.form.get('amount')
    category_id = request.form.get('category')

    if payee_id is not None:
        cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        cursor = cnx.cursor(buffered=True)
        
        insert_payment = ("INSERT INTO payment (payer_id, payee_id, amount, category_id, payment_time) VALUES(%s, %s, %s, %s, NOW())")
        cursor.execute(insert_payment, (payer_id, payee_id, amount, category_id))
        
        update_payer_balance = ("UPDATE account SET balance = balance - %s WHERE user_id = %s")
        cursor.execute(update_payer_balance, (amount, payer_id))
        
        update_payee_balance = ("UPDATE account SET balance = balance + %s WHERE user_id = %s")
        cursor.execute(update_payee_balance, (amount, payee_id))
        
        cnx.commit()
        

    cursor.close()
    cnx.close()
        
    return payee
 


@app.route("/schedule")
def schedule():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()

    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)
     
    query = ("SELECT user_id, balance FROM account WHERE username = %s")
    results = cursor.execute(query, (github_user["login"], ))
    if cursor.rowcount > 0:
        (user_id, balance) = cursor.fetchone()

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
        
    cursor.close()
    cnx.close()
        
    return render_template('schedule.html', title=' - Schedule payment', login=github_user['login'], categories=categories)
 
 
@app.route("/history")
def history():
    if not github.authorized:
        return redirect('/login')
        
    github_user = github.get("/user").json()

    user = get_user(github_user['login'])
    user_id = user["user_id"]

    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)
     
    records = []
    current_date = ""
    date_records = []
    query = ("""SELECT 
                    payment_id, payer.user_id, payer.username, payer.nickname, 
                    payee.user_id, payee.username, payee.nickname, 
                    amount, category.category_name, DATE_FORMAT(payment_time, "%e %b %Y") 
                FROM payment 
                LEFT JOIN account AS payer ON payment.payer_id = payer.user_id
                LEFT JOIN account AS payee ON payment.payee_id = payee.user_id
                LEFT JOIN category ON payment.category_id = category.category_id
                WHERE payment.payer_id = %s OR payment.payee_id = %s
                ORDER BY payment_time DESC""")
    cursor.execute(query, (user_id, user_id))
    rows = cursor.fetchall()
    i = 0
    rowcount = cursor.rowcount
    
    for (payment_id, payer_id, payer_username, payer_nickname, payee_id, payee_username, payee_nickname, amount, category, date) in rows:
        if i == 0:
            current_date = date

        if date != current_date:
            records.append({"date": current_date, "transactions": date_records})
            current_date = date
            date_records = []

        if payer_nickname == "":
            payer = payer_username
        else:
            payer = payer_nickname
            
        if payee_nickname == "":
            payee = payee_username
        else:
            payee = payee_nickname
    
        if user_id == payer_id:
            party = payee
            amount = -amount
            style = "red"
        elif user_id == payee_id:
            party = payer
            style = "green"
        else:
            party = "Error"
            style = "error"

        date_records.append({"party": party, "amount": amount, "category": category, "style": style})
        
        i += 1
        
        if i == rowcount:
            records.append({"date": current_date, "transactions": date_records})

    
    cursor.close()
    cnx.close()

    #records = [{"date": "2022-05-03", "transactions": [{"party": "Thomas Tsoi", "amount": 234.20}]}]
        
    return render_template('history.html', title=' - Payment history', login=github_user['login'], balance=user["balance"], records=records)
 
 
 
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

def get_user(username: str):
    cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT user_id, nickname, balance, budget FROM account WHERE username = %s")
    results = cursor.execute(query, (username, ))
    if cursor.rowcount > 0:
        (user_id, nickname, balance, budget) = cursor.fetchone()
        user = {"user_id": user_id, "nickname": nickname, "balance": balance, "budget": budget}
    else:
        user = {"user_id": None, "nickname": None, "balance": None, "budget": None}

    cursor.close()
    cnx.close()
    return user

# main driver function
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
