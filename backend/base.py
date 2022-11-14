from flask import Flask,request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
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
    if result > 0:
        row_headers = [x[0] for x in cur.description]  # this will extract
        # row headers
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

if __name__ == '__main__':
    app.run(debug=True)
