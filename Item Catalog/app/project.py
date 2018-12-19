from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')





if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
