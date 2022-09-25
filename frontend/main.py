from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
# app.config['UPLOAD_FOLDER'] = params['upload_location']

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
db = SQLAlchemy(app)

class Medicines(db.Model):
    med_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    contents = db.Column(db.String(120), nullable=False)
    expiry = db.Column(db.String(12))
    image = db.Column(db.String(30))
    
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html', params = params)

app.run(debug = True)