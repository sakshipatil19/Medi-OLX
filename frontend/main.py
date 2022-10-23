from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
db = SQLAlchemy(app)

class Users(db.Model):
    user_ID = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable = False)
    UIDAI = db.Column(db.Integer, nullable=False)
    user_add = db.Column(db.String(250), nullable=False)
    user_pcode = db.Column(db.Integer, nullable=False)
    user_Cno = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(80), nullable=False)
    user_pwd = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

class Medicines(db.Model):
    med_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    original_price = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    expiry = db.Column(db.String(12))
    image = db.Column(db.String(30))
    user_ID = db.Column(db.Integer, nullable=False)

class Medi_equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.String(12))
    image_name = db.Column(db.String(30))

@app.route("/medicine", methods=['GET', 'POST'])
def medicine():
    medicine = Medicines.query.filter_by(status="Approved").all()
    return render_template('shop.html', params=params, medicine=medicine)

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    medi_equipment = Medi_equipment.query.filter_by().all()
    return render_template('shop_e.html', params=params, equipment = medi_equipment)

@app.route("/signin", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        user_pwd = request.form.get('user_pwd')
        memb = Users.query.filter_by(user_email=user_email).first()
        if memb:
            if memb.user_pwd == user_pwd and memb.user_email == user_email:
                session['user'] = memb.user_email
                session['role'] = memb.role
                session['name'] = memb.user_name
                session['user_ID'] = memb.user_ID
                if memb.role == "admin":
                    return redirect('adminhome.html')
                else:
                    return redirect("/")
            else:
                return redirect('/signup')
    return render_template('login.html', params=params)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get("user_name")
        UIDAI = request.form.get("UIDAI")
        user_add = request.form.get("user_add")
        user_Cno = request.form.get("user_Cno")
        user_email = request.form.get("user_email")
        user_pcode = request.form.get("user_pcode")
        user_pwd = request.form.get("user_pwd")
        role = "user"
        newreg = Users(user_name=user_name, UIDAI=UIDAI, user_add=user_add, user_Cno=user_Cno, user_email=user_email, user_pcode=user_pcode, user_pwd=user_pwd, role=role)
        db.session.add(newreg)
        db.session.commit()
        return redirect("/")
    return render_template('signup.html', params=params)


@app.route("/", methods=['GET', 'POST'])
def home():
    medicine = Medicines.query.filter_by(status="Approved").all()[0:3]
    medi_equipment = Medi_equipment.query.filter_by().all()[0:3]
    if not session.get("user"):
        user = Users.query.filter_by(user_ID=1).all()
    else:
        user = Users.query.filter_by(user_email=session['user']).all()
    return render_template('index.html', params = params, medicine = medicine, equipment = medi_equipment, user = user)

@app.route("/medicine/<int:med_id>", methods=['GET', 'POST'])
def view_med(med_id):
    medicine = Medicines.query.filter_by(med_id=med_id).all()
    return render_template('shop_single.html', params = params, medicine=medicine)

# @app.route("/myproducts/<int:med_id>", methods=['GET', 'POST'])
# def view_med(med_id):
#     medicine = Medicines.query.filter_by(med_id=med_id, users_ID = session['user_ID']).all()
#     return render_template('shop_single.html', params = params, medicine=medicine)

@app.route("/equipment/<int:equip_id>", methods=['GET', 'POST'])
def view_e(equip_id):
    medi_equipment = Medi_equipment.query.filter_by(equip_id=equip_id).all()
    return render_template('shop_eq.html', params = params, medi_equipment=medi_equipment)

@app.route("/sell_medi", methods=['GET', 'POST'])
def sell_medi():
    if not session.get("user"):
        return redirect("/")
    else:
        return render_template("med_upload_seller.html", params=params)

@app.route("/sell_medi/add", methods=['GET', 'POST'])
def sell_medi_add():
    if not session.get("user"):
        return redirect("/")
    else:
        if (request.method == 'POST'):
            name = request.form.get("name")
            description = request.form.get("description")
            expiry = request.form.get("expiry")
            original_price = request.form.get("original_price")
            price = request.form.get("price")
            image = request.form.get("image")
            status = "Pending..."
            user_ID = Users.query.filter_by(user_email=session['user']).first()
            addit = Medicines(name = name, description = description, expiry = expiry, original_price = original_price, price = price, image = image, status = status, user_ID = user_ID.user_ID)
            db.session.add(addit)
            db.session.commit()
            f = request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return redirect("/")

@app.route("/myproducts", methods=['GET', 'POST'])
def myproducts():
    if not session.get("user"):
        return redirect("/")
    else:
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        medicine = Medicines.query.filter_by(user_ID=user_ID.user_ID).all()
        return render_template('myproduct.html', params=params, medicine=medicine)

@app.route("/sell_equip", methods=['GET', 'POST'])
def sell_equip():
    if not session.get("user"):
        return redirect("/")
    else:
        return render_template("med_equip_upload_seller.html", params=params)

@app.route("/about", methods = ['GET', 'POST'])
def about():
    return render_template("about.html", params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    return render_template("contact.html", params=params)

@app.route("/logout")
def logout():
    if not session.get("user"):
        return redirect("/")
    else:
        session.pop('user')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)