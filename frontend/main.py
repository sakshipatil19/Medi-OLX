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

class Users(db.Model):
    user_ID = db.Column(db.Integer, primary_key=True)
    user_Fname = db.Column(db.String(80), nullable = False)
    user_Lname = db.Column(db.String(80), nullable=False)
    UIDAI = db.Column(db.Integer, nullable=False)
    user_add = db.Column(db.String(250), nullable=False)
    user_Cno = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(80), nullable=False)
    user_pwd = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

class Medicines(db.Model):
    med_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    contents = db.Column(db.String(120), nullable=False)
    expiry = db.Column(db.String(12))
    image = db.Column(db.String(30))

class Medi_equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.String(12))
    image_name = db.Column(db.String(30))
    
@app.route("/", methods=['GET', 'POST'])
def home():
    medicine = Medicines.query.filter_by().all()[0:3]
    medi_equipment = Medi_equipment.query.filter_by().all()[0:3]
    return render_template('index.html', params = params, medicine = medicine, equipment = medi_equipment)

@app.route("/medicine", methods=['GET', 'POST'])
def medicine():
    medicine = Medicines.query.filter_by().all()
    return render_template('shop.html', params=params, medicine=medicine)

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    medi_equipment = Medi_equipment.query.filter_by().all()
    return render_template('shop_e.html', params=params, equipment = medi_equipment)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        user_pwd = request.form.get('user_pwd')
        memb = Users.query.filter_by(user_email=user_email).first()
        if memb:
            if memb.user_pwd == user_pwd and memb.user_email == user_email:
                session['user'] = memb.user_email
                session['role'] = memb.role
                if memb.role == "admin":
                    return redirect('adminhome.html')
                else:
                    return redirect("/")
            else:
                return redirect('/signup')
    return render_template('signup.html', params=params)

app.run(debug = True)