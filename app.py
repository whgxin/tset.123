from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql

from flask import g
import os
import uuid

import hashlib
DATABASE = 'database.db'

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




app.secret_key = "Your Key"
app.config['SESSION_TYPE'] = "test session"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()










DATABASE2 = 'database2.db'

def get_db2():
    db2 = getattr(g, '_database2', None)
    if db2 is None:
        db2 = g._database2 = sql.connect(DATABASE2)
    return db2

@app.teardown_appcontext
def close_connection(exception):
    db2 = getattr(g, '_database2', None)
    if db2 is not None:
        db2.close()




def allowed_file(filename):
    x=''
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        x= filename.rsplit('.', 1)[1].lower()
    return x


def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


@app.route("/")
def hello_python():
    return "<p>Hello, python!</p>"

@app.route("/name/<name>")
def name(name):
    print('Type:',type(name))
    return name

@app.route("/number/<int:number>")
def number(number):
    x = [i for i in range(number)]
    print('Type:',type(number))
    return f"{x}"

@app.route("/page")
def page():
    x = '1234'
    dict1 = {'abc':1324,'name':'tom'}
    return render_template("page.html",testx=x,dict1=dict1)

account = ""
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        type = '登入失敗'
        name = request.form.get('account')
        global account
        account = name
        password = request.form.get('password')
        password = sha256(password)
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute("select * from Users")
            data = cur.fetchall()
            cur.close()
        for i in data:
            if name == i['account'] and password == i['password']:
                type = '成功'
                break
        if type == '成功':
            with get_db() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor()
                cur.execute("select * from Pictures order by p_order")
                data = cur.fetchall()
                cur.close
            return render_template("u_show.html",type=type,data=data)
        else:
            return render_template("login.html",type=type)
    else:
        return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/users")
def users():
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute("select * from Users")
        data = cur.fetchall()
        cur.close
    return render_template("users.html",data = data)



@app.route("/createuser",methods=['POST'])
def createuser():
    name = request.form.get('username')
    if name == '':name = 'User'
    account = request.form.get('account')
    password = request.form.get('password')
    password = sha256(password)
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f"INSERT INTO Users (name, account, password) VALUES ('{name}','{account}','{password}');")
        cur.close()
    flash('新增成功')
    return redirect(url_for('users'))



@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form.get('username')
        account = request.form.get('account')
        password = request.form.get('password')
        password = sha256(password)
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"UPDATE Users SET name='{ name }', account='{ account }', password='{ password }' WHERE id = '{id}';")
            data = cur.fetchone()
            cur.close()
        flash('修改成功')
        return redirect(url_for('users'))
    else:
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"select * from Users where id = '{id}'")
            data = cur.fetchone()
            cur.close()
            return render_template("edit.html",data = data)
    
    #return render_template("users.html",data=data)

@app.route("/deleteuser/<int:id>",methods=['POST'])
def deleteuser(id):
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f"DELETE FROM Users where id={id}")
        #cur.execute("select * from Users")
        #data = cur.fetchall()
        cur.close()
    flash('刪除成功')
    return redirect(url_for('users'))
    #return render_template("users.html",data=data)



@app.route("/upload",methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.filename = allowed_file(f.filename)
        fsize = os.path.getsize(UPLOAD_FOLDER)
        name = str(uuid.uuid4())+"."+f.filename
        if f.filename == '':
            type = '附檔名不符'
        elif fsize >= 1*1024*1024:
            type = "檔案大小不符"
        else:
            type="新增成功"
            with get_db() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor()
                data = cur.execute(f"select * from  Pictures")
                order = 0
                for i in data:
                        if i['p_order'] > order:
                            order = i['p_order']
                cur.execute(f"INSERT INTO Pictures (p_name,p_order) VALUES ('{name}','{order+1}');")
                cur.close()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        return render_template("upload.html",type=type)
    return render_template("upload.html")


@app.route("/show")
def show():
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute("select * from Pictures order by p_order")
        data = cur.fetchall()
        cur.close
    return render_template("show.html",data=data)

@app.route("/u_show")
def u_show():
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute("select * from Pictures order by p_order")
        data = cur.fetchall()
        cur.close
    return render_template("u_show.html",data=data)



@app.route("/pictures")
def pictures():
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute("select * from Pictures order by p_order")
        data = cur.fetchall()
        length = len(data)
        for i in data:
            if i['p_order'] > length:
                length = i['p_order']
        cur.close
    return render_template("pictures.html",data=data,len = length)


@app.route("/manager_pictures",methods=['POST'])
def manager_pictures():
    id = request.form.get('id')
    fun = request.form.get('fun')
    if fun == '修改':
        p_order = request.form.get('p_order')
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"UPDATE Pictures SET p_order='{ p_order }' WHERE id = '{id}';")
            cur.close
        flash('修改成功')
    else:
        p_name = request.form.get('p_name')
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], p_name))
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"DELETE FROM Pictures WHERE id = '{id}';")
            cur.close
        flash('刪除成功')
    return redirect(url_for('pictures'))












@app.route("/home")
def home():
    return render_template("home.html")




@app.route("/ch_acc")
def ch_acc():
    with get_db2() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            #cur.execute(f"SELECT number FROM Users2 where number = '{number}'")
            cur.execute(f"select * from Users2 where number = '{account}'")
            data2 = cur.fetchall()
            cur.close()
    return render_template("ch_acc.html",data2 = data2)


@app.route("/m_login",methods=['GET','POST'])
def m_login():
    if request.method == 'POST':
        type = '登入失敗'
        name = request.form.get('account')
        password = request.form.get('password')
        if name == 'admin' and password == '1234':
            type = '登入成功'

        else:
            return render_template("m_login.html",type=type)
        
        if type == '登入成功':
            with get_db() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor()
                cur.execute("select * from Pictures order by p_order")
                data = cur.fetchall()
                cur.close()
                return render_template("show.html",type=type,data=data)
        else:
            return render_template("m_login.html",type=type)
    else:
        return render_template("m_login.html")




@app.route("/users2")
def users2():
    with get_db2() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute("select * from Users2")
        data2 = cur.fetchall()
        cur.close
    return render_template("users2.html",data2 = data2)

@app.route("/createuser2",methods=['POST'])
def createuser2():
    number = request.form.get('number')
    date = request.form.get('date')
    #if date == '':date = 'date'
    hours = request.form.get('hours')
    money = float(request.form.get('money'))
    note = "及格"
    if money < 60 and money >= 40:
        note = "補考"
    elif money < 40:
        note = "死當"
    with get_db2() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f"INSERT INTO Users2 (number, date, hours, money, note) VALUES ('{number}','{date}','{hours}','{money}','{note}');")
        cur.close()
    flash('新增成功')
    return redirect(url_for('users2'))



@app.route("/edit2/<int:id>",methods=['GET','POST'])
def edit2(id):
    if request.method == 'POST':
        number = request.form.get('number')
        date = request.form.get('date')
        hours = request.form.get('hours')
        money = float(request.form.get('money'))
        note = "及格"
        if money < 60 and money >= 40:
            note = "補考"
        elif money < 40:
            note = "死當"
        #note = request.form.get('note')
        with get_db2() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"UPDATE Users2 SET number='{ number }', date='{ date }', hours='{ hours }', money='{ money }', note='{ note }' WHERE id = '{id}';")
            data2 = cur.fetchone()
            cur.close()
        flash('修改成功')
        return redirect(url_for('users2'))
    else:
        with get_db2() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f"select * from Users2 where id = '{id}'")
            data2 = cur.fetchone()
            cur.close()
            return render_template("edit2.html",data2 = data2)
    
    #return render_template("users.html",data=data)


@app.route("/deleteuser2/<int:id>",methods=['POST'])
def deleteuser2(id):
    with get_db2() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f"DELETE FROM Users2 where id={id}")
        #cur.execute("select * from Users")
        #data = cur.fetchall()
        cur.close()
    flash('刪除成功')
    return redirect(url_for('users2'))
    #return render_template("users.html",data=data)



@app.route("/page2")
def page2():
    return render_template("page2.html")



@app.route("/register")
def register():
    return render_template("register.html")



@app.route("/ap",methods=['GET','POST'])
def ap():
    if request.method == 'POST':
        type = '註冊成功'
        account = request.form.get('account')
        password = request.form.get('password')
        password = sha256(password)
        if account == 'admin' and password == sha256('1234'):
            return render_template("register.html",type='此帳號已存在')
        else:
            with get_db() as cur:
                cur = cur.cursor()
                cur.execute(f"select * from Users where account = '{account}'")
                da_account = cur.fetchone()

                if da_account:
                    return render_template("register.html",type='此帳號已存在')
                else:  
                    with get_db() as cur:
                        cur.row_factory = sql.Row
                        cur = cur.cursor()
                        cur.execute(f"INSERT INTO Users (name, account, password) VALUES ('users','{account}','{password}');")
                        cur.close()
                    type="註冊成功"
                return render_template("login.html",type=type)
    else:
        return render_template("register.html")








if __name__ =="__main__":
    app.run(debug=True)