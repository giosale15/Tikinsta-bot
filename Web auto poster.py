from flask import Flask, request, redirect, render_template_string
import json, os, subprocess

app = Flask(__name__)

LINKS_FILE = "tiktok_links.txt"
ACCOUNTS_FILE = "accounts.json"
SCRIPT_PATH = "auto_poster_instagram_multi_orari.py"

HTML = '''
<!DOCTYPE html>
<html><head><title>Auto Poster Instagram</title>
<style>body{font-family:Arial;margin:20px;}
input,button{width:100%;padding:10px;margin:5px 0;}
.section{margin-bottom:30px;}
</style></head><body>
<h1>Instagram Auto Poster</h1>
<div class="section"><h2>Aggiungi Account</h2>
<form method="POST" action="/add_account">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Salva Account</button>
</form></div>
<div class="section"><h2>Aggiungi Link TikTok</h2>
<form method="POST" action="/add_link">
<input type="text" name="link" placeholder="https://www.tiktok.com/..." required>
<button type="submit">Aggiungi Link</button>
</form></div>
<div class="section"><h2>Avvia Script</h2>
<form method="POST" action="/start_script">
<button type="submit" style="background:green;color:white;">Avvia</button>
</form></div>
</body></html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/add_account", methods=["POST"])
def add_account():
    u, p = request.form["username"], request.form["password"]
    accounts = json.load(open(ACCOUNTS_FILE)) if os.path.exists(ACCOUNTS_FILE) else []
    accounts.append({"username":u,"password":p})
    json.dump(accounts, open(ACCOUNTS_FILE,"w"), indent=4)
    return redirect("/")

@app.route("/add_link", methods=["POST"])
def add_link():
    link = request.form["link"]
    with open(LINKS_FILE,"a") as f: f.write(link+"\\n")
    return redirect("/")

@app.route("/start_script", methods=["POST"])
def start_script():
    subprocess.Popen(["python", SCRIPT_PATH])
    return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
