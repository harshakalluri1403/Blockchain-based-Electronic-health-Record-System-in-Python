from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import blockChain

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'EHR'

mysql = MySQL(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/index.html')
def home():
    return render_template("index.html")


@app.route('/doctor.html')
def doctor():
    return render_template('doctor.html')


@app.route('/patients.html')
def patients():
    return render_template('patients.html')


@app.route('/patients_home.html', methods=["post", "get"])
def patients_home():
    return render_template("patients_home.html")


@app.route('/addEHR.html')
def addEHR():
    return render_template('addEHR.html')


@app.route('/book.html')
def book():
    return render_template('book.html')


@app.route('/blockchain.html')
def blockchain():
    return render_template('blockchain.html')


@app.route('/doctorregister.html')
def doctorregiter():
    return render_template("doctorregister.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/patientslogin', methods=["post", "get"])
def patientslogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patientsdata WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('patients_home.html', username=username)
        else:
            msg = 'Incorrect username/password!'
        return render_template('patients.html', msg=msg)


@app.route("/patientsregister", methods=["post", "get"])
def patientsregister():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone_number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patientsdata WHERE username = %s', ([username],))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template('patients.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('patients.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('patients.html', msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template('patients.html', msg=msg)
        else:

            cursor.execute('INSERT INTO patientsdata VALUES (NULL, %s, %s, %s, %s)',
                           (username, password, email, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return redirect(url_for('patients_home', msg=msg, username=username))


@app.route('/adddata', methods=['post', 'get'])
def adddata():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        record_id = request.form['rid']
        patient_name = request.form['name']
        address = request.form['address']
        insurence_id = request.form['iid']
        phone = request.form['phone']
        text = record_id + patient_name + address + insurence_id + phone
        print(type(text))
        print(text)
        if len(text) < 1:
            return redirect(url_for('index'))
        try:
            make_proof = request.form['make_proof']
        except Exception:
            make_proof = False
        blockChain.write_block(text, make_proof)

        if not record_id or not patient_name or not address or not insurence_id or not phone:
            msg = 'Please Fill All the Fields'
            return render_template('addEHR.html', msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO record VALUES (NULL, %s, %s, %s, %s, %s)',
                           (record_id, patient_name, address, insurence_id, phone))
            mysql.connection.commit()
            msg = 'Data Successfully stored into Block chain'
        return render_template('blockchain.html', msg=msg)


@app.route('/check', methods=['POST'])
def integrity():
    results = blockChain.check_blocks_integrity()
    if request.method == 'POST':
        return render_template('blockchain.html', results=results)
    return redirect(url_for('patients_home'))


@app.route('/mining', methods=['POST'])
def mining():
    if request.method == 'POST':
        max_index = int(blockChain.get_next_block())

        for i in range(2, max_index):
            blockChain.get_POW(i)
        return render_template('blockchain.html', querry=max_index)
    return redirect(url_for('patients_home'))


@app.route('/bookdata', methods=['post', 'get'])
def book_data():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['name']
        age = request.form['age']
        temperature = request.form['temp']
        time = request.form['time']
        patient_id = request.form['patid']
        if not username or not age or not temperature or not time or not patient_id:
            msg = 'Please Fill All the Fields'
            return render_template('book.html', msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO bookdata VALUES (NULL, %s, %s, %s, %s, %s)',
                           (username, age, temperature, time, patient_id))
            mysql.connection.commit()
            msg = 'Data Successfully stored into Block chain'
        return render_template('patients_home.html', msg=msg)


@app.route('/doctorlogin', methods=['post', 'get'])
def doctorlogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from bookdata")
            print("INN")
            data = cursor.fetchall()
            print(data)
            # Redirect to home page
            return render_template('doctorhome.html', data=data, username=username)

        else:
            msg = 'Incorrect username/password!'
        return render_template('doctor.html', msg=msg)


@app.route('/dregister', methods=['post', 'get'])
def docregister():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE username = %s', ([username],))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template('doctor.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('doctor.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('doctor.html', msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template('doctor.html', msg=msg)
        else:

            cursor.execute('INSERT INTO doctor VALUES (NULL, %s, %s, %s, %s)',
                           (username, password, email, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return render_template('doctor.html', msg=msg, username=username)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
