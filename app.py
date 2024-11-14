from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(('menu_incial.html'))

if __name__ == '__main__':
    app.run(debug=True, port=1928)