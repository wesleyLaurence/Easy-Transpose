from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import getpass

app = Flask(__name__)

# configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = input('User ID: ')
app.config['MYSQL_PASSWORD'] = getpass.getpass('Password: ')
app.config['MYSQL_DB'] = 'easytranspose'

mysql = MySQL(app)

# Display MySQL table as HTML table
@app.route('/transpose')
def transpose():
	cur = mysql.connection.cursor()
	data = cur.execute("SELECT * FROM transpose;")
	if data > 0:
		all_columns = cur.fetchall()
		return render_template('transpose.html',all_columns=all_columns)


if __name__== '__main__':
	app.run(debug=True)