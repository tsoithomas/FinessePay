from flask import Flask, request, send_from_directory, render_template, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
from time import time

# app = Flask(__name__)
app = Flask(__name__,
            static_url_path='', 
            static_folder='assets',
            template_folder='views')
CORS(app)
app.secret_key = "please_define_a_secret_key_here"
app.config["GITHUB_OAUTH_CLIENT_ID"] = 'YOUR_GITHUB_CLIENT_ID'
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = 'YOUR_GITHUB_CLIENT_SECRET'
blueprint = make_github_blueprint()
app.register_blueprint(make_github_blueprint(), url_prefix="/login")

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/")
def index():
    if github.authorized:
        github_user = github.get("/user").json()
        return render_template('index.html', title = ' - Index', login = github_user['login'])
    else:
        return render_template('index.html', title = ' - Index')

@app.route("/login")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return redirect('/')

@app.route("/portfolio")
def portfolio():
    if not github.authorized:
        return redirect('/login')
    github_user = github.get("/user").json()
    return render_template('portfolio.html', title = ' - Portfolio')
 
  
# main driver function
if __name__ == '__main__':
    app.run()
