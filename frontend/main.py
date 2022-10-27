from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta, date

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

now = date.today()
now_before_month = now - timedelta(days=31)

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
    expiry = db.Column(db.Date, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    back_img = db.Column(db.String(50), nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)

class Medi_equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)

# <------------Store------------->
@app.route("/medicine", methods=['GET', 'POST'])
def medicine():
    medicine = Medicines.query.filter_by(status="Approved").all()
    return render_template('shop.html', params=params, medicine=medicine)

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    medi_equipment = Medi_equipment.query.filter_by(status="Approved").all()
    return render_template('shop_e.html', params=params, equipment = medi_equipment)

# <------------Login/Register------------->
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
                    return redirect('/admin')
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

# <------------Home Page------------->
@app.route("/", methods=['GET', 'POST'])
def home():
    # med = Medicines.query.filter_by(status="Approved").all()
    # now = date.today()
    # now_before_month = now - timedelta(days=31)
    # for med in med:
    #     expiry = med.expiry
    #     if expiry <= now_before_month:
    #         medicine = Medicines.query.filter_by(status="Approved", expiry=expiry).all()[0:3]
    #         medi_equipment = Medi_equipment.query.filter_by(status="Approved").all()[0:3]
    #     else:
    #         pass
    medicine = Medicines.query.filter_by(status="Approved").all()[0:3]
    medi_equipment = Medi_equipment.query.filter_by(status="Approved").all()[0:3]
    if not session.get("user"):
        user = Users.query.filter_by(user_ID=1).all()
    else:
        user = Users.query.filter_by(user_email=session['user']).all()
    return render_template('index.html', params = params, medicine = medicine, equipment = medi_equipment, user = user)

# <------------Medicine Detials Page------------->
@app.route("/medicine/<int:med_id>", methods=['GET', 'POST'])
def view_med(med_id):
    medicine = Medicines.query.filter_by(med_id=med_id).all()
    med = Medicines.query.filter_by(med_id=med_id).first()
    user_ID = med.user_ID
    users = Users.query.filter_by(user_ID = user_ID).all()
    return render_template('shop_single.html', params = params, medicine=medicine, users = users)

# <------------Equipment Detials Page------------->
@app.route("/equipment/<int:equip_id>", methods=['GET', 'POST'])
def view_e(equip_id):
    medi_equipment = Medi_equipment.query.filter_by(equip_id=equip_id).all()
    equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
    user_ID = equip.user_ID
    users = Users.query.filter_by(user_ID=user_ID).all()
    return render_template('shop_eq.html', params = params, medi_equipment=medi_equipment, users = users)

# <------------Medicine Sell Page------------->
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
            back_img = request.form.get("image1")
            user_ID = Users.query.filter_by(user_email=session['user']).first()
            addit = Medicines(name = name, description = description, expiry = expiry, original_price = original_price, price = price, image = image, back_img = back_img, status = status, user_ID = user_ID.user_ID)
            db.session.add(addit)
            db.session.commit()
            f = request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return redirect("/")

# <------------Equipment Sell Page------------->
@app.route("/sell_equip", methods=['GET', 'POST'])
def sell_equip():
    if not session.get("user"):
        return redirect("/")
    else:
        return render_template("med_equip_upload_seller.html", params=params)

@app.route("/sell_equip/add", methods=['GET', 'POST'])
def sell_equip_add():
    if not session.get("user"):
        return redirect("/")
    else:
        name = request.form.get("name")
        description = request.form.get("description")
        original_price = request.form.get("original_price")
        discounted_price = request.form.get("discounted_price")
        image_name = request.form.get("image_name")
        status = "Pending..."
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        addit = Medi_equipment(name=name, description=description, original_price=original_price, discounted_price=discounted_price,
                          image_name=image_name, status=status, user_ID=user_ID.user_ID)
        db.session.add(addit)
        db.session.commit()
        f = request.files['file_name']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return redirect("/")

# <------------My Products Viewing Page------------->
@app.route("/myproducts/med", methods=['GET', 'POST'])
def myproducts_med():
    if not session.get("user"):
        return redirect("/")
    else:
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        medicine = Medicines.query.filter_by(user_ID=user_ID.user_ID).all()
        return render_template('myproduct_med.html', params=params, medicine=medicine)

@app.route("/myproducts/equip", methods=['GET', 'POST'])
def myproducts_equip():
    if not session.get("user"):
        return redirect("/")
    else:
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        equipments = Medi_equipment.query.filter_by(user_ID=user_ID.user_ID).all()
        return render_template('myproduct_equip.html', params=params, equipments=equipments)

# <------------About us------------->
@app.route("/about", methods = ['GET', 'POST'])
def about():
    return render_template("about.html", params=params)

# <------------Contact Us------------->
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    return render_template("contact.html", params=params)

# <------------Logout Mechanism------------->
@app.route("/logout")
def logout():
    if not session.get("user"):
        return redirect("/")
    else:
        session.pop('user')
        return redirect('/')


# <------------Admin------------->
@app.route("/admin", methods = ['GET', 'POST'])
def admin_home():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        users = Users.query.filter_by(user_email = session['user']).all()
        return render_template("adminhome.html", params=params, users = users)
    else:
        return redirect("/")

# <------------User Details------------->
@app.route("/details/user", methods = ['GET', 'POST'])
def user_details():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        users = Users.query.filter_by(role="user").all()
        return render_template("detailsuser.html", params=params, users = users)
    else:
        return redirect("/")

# <------------Admin Details------------->
@app.route("/details/admin", methods = ['GET', 'POST'])
def admin_details():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        users = Users.query.filter_by(role="admin").all()
        return render_template("detailsadmin.html", params=params, users = users)
    else:
        return redirect("/")

# <------------Med Details------------->
@app.route("/details/med", methods = ['GET', 'POST'])
def med_details():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        med = Medicines.query.filter_by(status="Approved").all()
        return render_template("detailsmed.html", params=params, med = med)
    else:
        return redirect("/")

# <------------Med Delete------------->
@app.route("/medicine/remove/<int:med_id>", methods = ['GET', 'POST'])
def med_remove(med_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        med = Medicines.query.filter_by(med_id = med_id).first()
        med.status = "Removed by Admin"
        db.session.commit()
        return redirect("/details/med")
    else:
        med = Medicines.query.filter_by(med_id=med_id).first()
        med.status = "Removed by You"
        db.session.commit()
        return redirect("/myproducts/med")

# <------------Equip Details------------->
@app.route("/details/equip", methods = ['GET', 'POST'])
def equip_details():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equip = Medi_equipment.query.filter_by(status="Approved").all()
        return render_template("detailsequip.html", params=params, equip=equip)
    else:
        return redirect("/")

# <------------Equip Delete------------->
@app.route("/equipment/remove/<int:equip_id>", methods = ['GET', 'POST'])
def equip_remove(equip_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equip = Medi_equipment.query.filter_by(equip_id = equip_id).first()
        equip.status = "Removed by Admin"
        db.session.commit()
        return redirect("/details/equip")
    else:
        equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
        equip.status = "Removed by You"
        db.session.commit()
        return redirect("/myproducts/equip")

# <------------Approval ------------->
# <--------------Med-------------->
@app.route("/med/approval", methods = ['GET', 'POST'])
def med_approval_list():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        med = Medicines.query.filter_by(status="Pending...").all()
        return render_template("approvalmedlst.html", params=params, med = med)
    else:
        return redirect("/")

# <--------------Equip-------------->
@app.route("/equip/approval", methods = ['GET', 'POST'])
def equip_approval_list():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equip = Medi_equipment.query.filter_by(status="Pending...").all()
        return render_template("approvalequiplst.html", params=params, equip=equip)
    else:
        return redirect("/")

# <--------------Med View-------------->
@app.route("/med/approval/view/<int:med_id>", methods = ['GET', 'POST'])
def med_approval_view(med_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        medicine = Medicines.query.filter_by(med_id = med_id).all()
        med = Medicines.query.filter_by(med_id=med_id).first()
        user_ID = med.user_ID
        users = Users.query.filter_by(user_ID=user_ID).all()
        return render_template("approvalmedview.html", params=params, medicine=medicine, users=users)
    else:
        return redirect("/")

@app.route("/medicine/approve/<int:med_id>", methods = ['GET', 'POST'])
def med_approve_done(med_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        med = Medicines.query.filter_by(med_id = med_id).first()
        med.status = "Approved"
        db.session.commit()
        return redirect("/med/approval")
    else:
        return redirect("/")

@app.route("/medicine/reject/<int:med_id>", methods = ['GET', 'POST'])
def med_approve_reject(med_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        med = Medicines.query.filter_by(med_id = med_id).first()
        med.status = "Rejected"
        db.session.commit()
        return redirect("/med/approval")
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)



# <------------All Pages Details------------->
# index.html -> Home Page

# layout.html -> Nav bar/Header/Footer

# shop.html -> All Medicines View Page
# shop_e.html -> All Equipments View Page

# shop_single.html -> Medicines Details Page
# shop_eq.html -> Equipments Details Page

# med_upload_seller.html -> Medicines Selling Page
# med_equip_upload_seller.html -> Equipments Selling Page