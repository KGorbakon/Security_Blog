import sqlite3
from flask import Flask, render_template, render_template_string, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_file(f_name):
    with open(f_name) as f:
        return f.readlines()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.jinja_env.globals['get_user_file'] = get_user_file

@app.route('/')
def index():
    conn = get_db_connection()
    conn.close()
    return render_template('index.html')

@app.route('/SQLi', methods=('GET', 'POST'))
def SQLi():

    if request.method == "POST":
        details = request.form
        
        user = details['user'] 
        passw = details['pass']
        
        conn = get_db_connection()
        sql = "SELECT * FROM users WHERE username ='" + user + "' AND password = '" + passw + "'"
        account = conn.execute(sql).fetchone()
        
        if account is not None:
            return 'Logged in successfully'
        else:
            return 'Log in failed, Wrong Credentials'

    return render_template('SQLi.html')

@app.route('/LFI')
def LFI():

    person = {'name':"world"}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h1>LFI</h1>
        <p>Local File Inclusion - это подключение, выполнение или чтение локальных файлов на сервере.</p>
        <p>Пример:</p>
        <p>?name=&#123;&#123; get_user_file("secret.txt")&#125;&#125;</p>
        <h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)

@app.route('/RCE')
def RCE():

    person = {'name':"world", 'secret':"z8ms4qa9v"}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template =  '''<h1>RCE</h1>
        <p>Remote Code Execution - эксплуатация этой уязвимости позволяет дистанционно запустить
         вредоносный код в рамках целевой системы по локальной сети или через интернет. Физического 
         доступа злоумышленника к устройству не требуется. В результате эксплуатации RCE-уязвимости 
         взломщик может перехватить управление системой или ее отдельными компонентами, а также украсть 
         конфиденциальные данные.</p>
        <p>Пример:</p>
        <p>?name=&#123;&#123;person.secret&#125;&#125;</p>
        <h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)

@app.route('/XSS')
def XSS():
    person = {'name':"world"}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template =  '''<h1>XSS</h1>
        <p> XSS — тип атаки на веб-системы, заключающийся во внедрении в выдаваемую веб-системой страницу 
        вредоносного кода и взаимодействии этого кода с веб-сервером злоумышленника.</p>
        <p>Пример:</p>
        <p>?name=XSS&lt;script&gt;alert("Send me 10$ +79772673208")&lt;/script&gt;</p>
        <h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)

   