from flask import Flask, render_template, request, json, jsonify, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

#CLEARDB_DATABASE_URL: mysql://bc318808df5eaf:25b4c773@us-cdbr-iron-east-05.cleardb.net/heroku_f959c05b805d118?reconnect=true
app.config['MYSQL_DATABASE_USER']='bc318808df5eaf'
app.config['MYSQL_DATABASE_PASSWORD']='25b4c773'
app.config['MYSQL_DATABASE_DB']='heroku_f959c05b805d118'
app.config['MYSQL_DATABASE_HOST']='us-cdbr-iron-east-05.cleardb.net'
#app.config['MYSQL_DATABASE_USER']='root'
#app.config['MYSQL_DATABASE_PASSWORD']='Rootpass@123'
#app.config['MYSQL_DATABASE_DB']='Hobbies'
#app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)
app.secret_key="I've got the key, I've got the secret"

@app.route('/')
def home():
    return render_template('index.html')

#@app.route('/<string:page_name>')
#def static_page(page_name):
#    return render_template('%s.html' % page_name)

@app.route('/signup')
def sign():
    return render_template('signup.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _number = request.form['inputNumber']
    _password = request.form['inputPassword']
    if _name and _email and _number and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        #_hashed_password = generate_password_hash(_password)
        cursor.callproc('add_User', (_name, _email, _number, _password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            session['user'] = data[0][0]
            return jsonify(dict(redirect='home'))
        else:
            return jsonify(dict(redirect='error'))

    else:
        return jsonify(dict(redirect='error'))

@app.route('/validateLogin',methods=['GET','POST'])
def validateLogin():
    try:
        _email = request.form['logEmail']
        _password = request.form['logPassword']
        
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login',(_email,_password))
        data = cursor.fetchall()

        if len(data)>0:
            #if check_password_hash(str(data[0][3]),_password):
                #session['user']=data[0][0]
            session['user']=data[0][0]
            return jsonify(dict(redirect='home'))
            #else:
               # return json.dumps({'message': 'Wrong email or password'})
        else:
            status = 'Wrong email or password'
            return jsonify(dict(redirect='error'))

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        con.close()

@app.route('/error')
def error():
    return render_template('error.html',error="Something went wrong, try again")

@app.route('/home')
def user():
    if session.get('user'):
        return render_template('home.html')
    else:
        return render_template('error.html',error="Unauthorized access")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/signup')

@app.route('/addHobby',methods=['GET','POST'])
def addHobby():
    try:
        if session.get('user'):
            _hobby = request.form['hobby']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('addHobby',(_hobby,_user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return jsonify(dict(redirect='/home'))
            else:
                return jsonify(dict(redirect='/home_error'))
        else:
            return jsonify(dict(redirect='/error'))
    except Exception as e:
        return jsonify(dict(redirect='/home_error'))
    #finally:
    #    cursor.close()
     #   conn.close()

@app.route('/showHobby')
def showHobby():
    try:
        if session.get('user'):
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('showHobby',(_user,))
            hobbies = cursor.fetchall()
            
            hobbies_dict = []
            for hobby in hobbies:
                hobby_dict = {
                    'Id':hobby[0],
                    'Hobby':hobby[1]}
                hobbies_dict.append(hobby_dict)
            
            return json.dumps(hobbies_dict)
        else:
            return jsonify(dict(redirect='/error'))
    except Exception as e:
        return jsonify(dict(redirect='/home_error'))

@app.route('/home_error')
def home_error():
    return render_template('home_error.html')

if __name__ == '__main__':
    app.run(debug=True)
