from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta, date
import razorpay
import re
from email.message import EmailMessage
import ssl
import smtplib


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




# @app.route("/result", methods=['POST', 'GET'])
# def res():
#     if request.method == 'POST':
#         receiver = request.form.get("email")
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(sender, password)
#             smtp.sendmail(sender, receiver, em.as_string())
#         return render_template("result.html", res="Success")
#     else:
#         return render_template("result.html", res="Failure!!")
# Email Automation

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
    image = db.Column(db.String(150), nullable=False)
    back_img = db.Column(db.String(150), nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    pills = db.Column(db.Integer, nullable=False)

class Medi_equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)

class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    type_of = db.Column(db.String(80), nullable = False)
    user_ID = db.Column(db.Integer, nullable=False)
    med_id = db.Column(db.Integer, nullable=True)
    equip_id = db.Column(db.Integer, nullable=True)
    wish_stats = db.Column(db.Integer, nullable=False)

class Order_med(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_add = db.Column(db.String(250), nullable=False)
    user_Cno = db.Column(db.Integer, nullable=False)
    med_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    med_id = db.Column(db.Integer, nullable=False)
    pres_img = db.Column(db.String(150), nullable=False)
    order_status = db.Column(db.String(80), nullable=False)
    dis_status = db.Column(db.Integer, nullable=False)

class Payment(db.Model):
    pay_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(80), nullable=False)
    user_Cno = db.Column(db.Integer, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    med_id = db.Column(db.Integer, nullable=True)
    equip_id = db.Column(db.Integer, nullable=True)
    user_add = db.Column(db.String(250), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    cancel_stats = db.Column(db.Integer, nullable=False)

class Delivery(db.Model):
    delivery_id = db.Column(db.Integer, primary_key=True)
    delivery_status = db.Column(db.String(80), nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    med_id = db.Column(db.Integer, nullable=True)
    equip_id = db.Column(db.Integer, nullable=True)
    seller_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
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
    if not session.get("user"):
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
                    elif memb.role == "delivery":
                        return redirect('/delivery')
                    else:
                        flash("You have logged in ", "info")
                        return redirect("/")
                else:
                    flash("Email & Password Did not matched", "error")
                    return redirect('/signin')
            else:
                flash("Your Email is not Registered. Please Register", "error")
                return redirect('/signin')
    else:
        flash("You are already Logged In, Logout first.", "error")
        return redirect("/")
    return render_template('login.html', params=params)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if not session.get("user"):
        if request.method == 'POST':
            user_name = request.form.get("user_name")
            UIDAI = request.form.get("UIDAI")
            user_add = request.form.get("user_add")
            user_Cno = request.form.get("user_Cno")
            user_email = request.form.get("user_email")
            receiver = request.form.get("user_email")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em.as_string())
            user_pcode = request.form.get("user_pcode")
            user_pwd = request.form.get("user_pwd")
            p = user_pwd
            role = "user"
            users = Users.query.filter_by().all()
            for user in users:
                if user_email == user.user_email:
                    flash("Your Email is already Registered", "info")
                    return redirect('/register')
            if (len(p) < 7 or len(p) > 17):
                flash("Password Should be of 8 to 16 Characters", "info")
                return redirect('/register')
            elif not re.search("[a-z]", p):
                flash("Password Should Contain atleast 1 Lowercase Characters", "info")
                return redirect('/register')
            elif not re.search("[0-9]", p):
                flash("Password Should Contain atleast 1 Digit Characters", "info")
                return redirect('/register')
            elif not re.search("[A-Z]", p):
                flash("Password Should Contain atleast 1 Uppercase Characters", "info")
                return redirect('/register')
            elif not re.search("[!$#@*&()]", p):
                flash("Password Should Contain atleast 1 Special Characters", "info")
                return redirect('/register')
            else:
                newreg = Users(user_name=user_name, UIDAI=UIDAI, user_add=user_add, user_Cno=user_Cno,
                               user_email=user_email, user_pcode=user_pcode, user_pwd=user_pwd, role=role)
                db.session.add(newreg)
                db.session.commit()
                flash("Registered Successfully", "info")
                return redirect("/")
    else:
        flash("You are already Logged In, Logout first to Register", "info")
        return redirect("/")

    return render_template('signup.html', params=params)

# Email Automation
sender = 'mediolxcoop@gmail.com'
password = 'ccipobbxfzfbhbrj'

subject = 'Registration Successful!!'
body = """
        Your Account Registration is Successful and you're good to go!!
        Happy Shopping!
        """

em = EmailMessage()
em['From'] = sender

em['Subject'] = subject
em.set_content(body)
context = ssl.create_default_context()


# <------------Home Page------------->
@app.route("/", methods=['GET', 'POST'])
def home():
    medicine = Medicines.query.filter_by(status="Approved").all()[0:3]
    medi_equipment = Medi_equipment.query.filter_by(status="Approved").all()[0:3]
    if not session.get("user"):
        user = Users.query.filter_by(user_ID=1).all()
    else:
        user = Users.query.filter_by(user_email=session['user']).all()
    return render_template('index.html', params = params, medicine = medicine, equipment = medi_equipment, user = user)

# <------------Medicine Details Page------------->
@app.route("/medicine/<int:med_id>", methods=['GET', 'POST'])
def view_med(med_id):
    medicine = Medicines.query.filter_by(med_id=med_id).all()
    med = Medicines.query.filter_by(med_id=med_id).first()
    user_ID = med.user_ID
    users = Users.query.filter_by(user_ID = user_ID).all()
    return render_template('shop_single.html', params = params, medicine=medicine, users = users)

# <------------Equipment Details Page------------->
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
        flash("Login First", "error")
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
            pills = request.form.get("no_tab")
            back_img = request.form.get("image1")
            user_ID = Users.query.filter_by(user_email=session['user']).first()
            addit = Medicines(name = name, description = description, expiry = expiry, original_price = original_price,
                              price = price, image = image, back_img = back_img, status = status, user_ID = user_ID.user_ID, pills=pills)
            db.session.add(addit)
            db.session.commit()
            f = request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            f1 = request.files['file_name1']
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f1.filename)))
            flash("Prescription Uploaded Successfully", "info")
            return redirect("/")

# <------------Equipment Sell Page------------->
@app.route("/sell_equip", methods=['GET', 'POST'])
def sell_equip():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        return render_template("med_equip_upload_seller.html", params=params)

@app.route("/sell_equip/add", methods=['GET', 'POST'])
def sell_equip_add():
    if not session.get("user"):
        return redirect("/")
    else:
        if (request.method == 'POST'):
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
        flash("Login First", "error")
        return redirect("/")
    else:
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        medicine = Medicines.query.filter_by(user_ID=user_ID.user_ID).all()
        return render_template('myproduct_med.html', params=params, medicine=medicine)

@app.route("/myproducts/equip", methods=['GET', 'POST'])
def myproducts_equip():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        user_ID = Users.query.filter_by(user_email=session['user']).first()
        equipments = Medi_equipment.query.filter_by(user_ID=user_ID.user_ID).all()
        return render_template('myproduct_equip.html', params=params, equipments=equipments)

# <------------Wishlist------------->
@app.route("/wishlist", methods = ['GET', 'POST'])
def wishlist():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        wish = Wishlist.query.filter_by(user_ID = session["user_ID"]).all()
        med = []
        equips = []
        for wishs in wish:
            if wishs.wish_stats == 0:
                if wishs.med_id is not None:
                    med_id = wishs.med_id
                    medicine = Medicines.query.filter_by(med_id=med_id, status = "Approved").first()
                    med += [medicine]
        for wishs in wish:
            if wishs.wish_stats == 0:
                if wishs.equip_id is not None:
                    equip_id = wishs.equip_id
                    equipment = Medi_equipment.query.filter_by(equip_id=equip_id, status = "Approved").first()
                    equips += [equipment]
        return render_template("wishlist.html", params=params, med=med, equips=equips)

# <------------Wishlist Med Add------------->
@app.route("/wishlist/med/<int:med_id>", methods = ['GET', 'POST'])
def wishlist_med_add(med_id):
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        med_id = med_id
        user_ID = session["user_ID"]
        type_of = "Medicine"
        wish_stats = 0
        add_med_wish = Wishlist(type_of=type_of, user_ID=user_ID, med_id=med_id, wish_stats = wish_stats)
        db.session.add(add_med_wish)
        db.session.commit()
        return redirect("/wishlist")

# <------------Wishlist Med Remove------------->
@app.route("/wishlist/remove/med/<int:med_id>")
def wishlist_med_remove(med_id):
    if not session.get("user"):
        return redirect("/")
    else:
        deletewish = Wishlist.query.filter_by(med_id=med_id, user_ID=session["user_ID"]).first()
        db.session.delete(deletewish)
        db.session.commit()
        return redirect("/wishlist")

# <------------Wishlist Equip Add------------->
@app.route("/wishlist/equip/<int:equip_id>", methods = ['GET', 'POST'])
def wishlist_equip_add(equip_id):
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        equip_id = equip_id
        user_ID = session["user_ID"]
        type_of = "Equipment"
        wish_stats = 0
        add_equip_wish = Wishlist(type_of=type_of, user_ID=user_ID, equip_id=equip_id, wish_stats=wish_stats)
        db.session.add(add_equip_wish)
        db.session.commit()
        return redirect("/wishlist")

# <------------Wishlist Equip Remove------------->
@app.route("/wishlist/remove/equip/<int:equip_id>", methods = ['GET', 'POST'])
def wishlist_equip_remove(equip_id):
    if not session.get("user"):
        return redirect("/")
    else:
        deletewish = Wishlist.query.filter_by(equip_id=equip_id, user_ID=session["user_ID"]).first()
        db.session.delete(deletewish)
        db.session.commit()
        return redirect("/wishlist")

# <------------PRESCRIPTION UPLOAD------------->
@app.route("/confirm/order/med/<int:med_id>", methods = ['GET', 'POST'])
def pres_upload(med_id):
    if not session.get("user"):
        return redirect("/")
    else:
        users = Users.query.filter_by(user_ID=session["user_ID"]).all()
        return render_template("uploadpres.html", params=params, users=users, med_id=med_id)

@app.route("/upload/pres", methods = ['GET', 'POST'])
def uploaded_pres():
    if not session.get("user"):
        return redirect("/")
    else:
        if (request.method == 'POST'):
            user_name = request.form.get("name")
            user_add = request.form.get("address")
            user_Cno = request.form.get("contact")
            user_ID = session["user_ID"]
            med_id = request.form.get("med_id")
            med =  Medicines.query.filter_by(med_id=med_id).first()
            med_name = med.name
            seller_id = med.user_ID
            price = med.price
            order_status = "Prescription Approval Pending..."
            pres_img = request.form.get("image_name")
            dis_status = 0
            addit = Order_med(user_name=user_name, user_add=user_add, user_Cno=user_Cno, user_ID=user_ID, seller_id=seller_id, med_id=med_id, med_name=med_name,
                              price=price, order_status=order_status, pres_img=pres_img, dis_status = dis_status)
            db.session.add(addit)
            med.status = "Prescription Approval Pending..."
            deletewish = Wishlist.query.filter_by(med_id=med_id, user_ID=session["user_ID"]).first()
            wish = Wishlist.query.filter_by(med_id=med_id).all()
            for wishes in wish:
                wishes.wish_stats = 1
                db.session.commit()
            db.session.delete(deletewish)
            db.session.commit()
            f = request.files['file_name']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return redirect("/orders/med/view")

# <------------Med Order User------------->
@app.route("/orders/med/view", methods = ['GET', 'POST'])
def order_med():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        orders = Order_med.query.filter_by(user_ID = session["user_ID"], dis_status = 0).all()
        med = []
        for order_m in orders:
            med_id = order_m.med_id
            medicine = Medicines.query.filter_by(med_id=med_id).first()
            med += [medicine]
        return render_template("ordermed.html", params=params, orders=orders, med=med)

# <------------Payment med complete------------->
@app.route("/pay/order/med/<int:med_id>", methods=['GET', 'POST'])
def pay_med(med_id):
    if not session.get("user"):
        return redirect("/")
    else:
        med = Medicines.query.filter_by(med_id = med_id).first()
        if med.status == "Payment Pending...":
            users = Users.query.filter_by(user_ID=session['user_ID']).first()
            orders = Order_med.query.filter_by(med_id=med_id, user_ID=session['user_ID']).first()
            client = razorpay.Client(auth = ("rzp_test_HJEVdhoCF6dSvY", "xpocHyKYqLG8FJZrNRR6LOPe"))
            payment = client.order.create({'amount': (int(med.price * 100)),
                                           'currency': 'INR', 'payment_capture': '1'})
            return render_template("razorpay.html", payment=payment, users = users, med=med, params=params, orders=orders)
        else:
            flash("Prescription Approval is Pending", "error")
            return redirect("/orders/med/view")


# <------------Payment Equip complete------------->
@app.route("/pay/order/equip/<int:equip_id>", methods=['GET', 'POST'])
def pay_equip(equip_id):
    if not session.get("user"):
        return redirect("/")
    else:
        equip = Medi_equipment.query.filter_by(equip_id = equip_id).first()
        if equip.status == "Approved":
            users = Users.query.filter_by(user_ID=session['user_ID']).first()
            equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
            client = razorpay.Client(auth = ("rzp_test_HJEVdhoCF6dSvY", "xpocHyKYqLG8FJZrNRR6LOPe"))
            payment = client.order.create({'amount': (int(equip.discounted_price * 100)),
                                           'currency': 'INR', 'payment_capture': '1'})
            return render_template("razorpay_equip.html", payment=payment, users = users, equip=equip, params=params)
        else:
            flash("Something went wrong.", "error")
            return redirect("/wishlist")

# <------------Payment Med confirmed------------->
@app.route("/confirmed/med/<int:med_id>", methods=['GET', 'POST'])
def confirmed_med(med_id):
    if not session.get("user"):
        return redirect("/")
    else:
        med = Medicines.query.filter_by(med_id=med_id).first()
        med.status = "Sold"
        orders = Order_med.query.filter_by(med_id=med_id, user_ID=session["user_ID"]).first()
        orders.order_status = "Payment Completed"
        orders.dis_status = 1
        med_id = med_id
        user_ID = session['user_ID']
        price = med.price
        seller_id = orders.seller_id
        user_Cno = orders.user_Cno
        user_name = orders.user_name
        user_add = orders.user_add
        delivery_status = "Not Yet Dispatched"
        now = date.today()
        payment_date = order_date = now
        cancel_stats = 0
        addit1 = Payment(med_id=med_id, user_ID=user_ID, price=price, seller_id=seller_id, user_Cno=user_Cno,
                        user_name=user_name, user_add=user_add, payment_date=payment_date, cancel_stats=cancel_stats)
        addit2 = Delivery(delivery_status=delivery_status, user_ID=user_ID, med_id=med_id, seller_id=seller_id, order_date=order_date)
        db.session.add(addit1)
        db.session.add(addit2)
        db.session.commit()
        return redirect("/myorders")

# <------------Payment Equip confirmed------------->
@app.route("/confirmed/equip/<int:equip_id>", methods=['GET', 'POST'])
def confirmed_equip(equip_id):
    if not session.get("user"):
        return redirect("/")
    else:
        equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
        equip.status = "Sold"
        user_ID = session['user_ID']
        price = equip.discounted_price
        seller_id = equip.user_ID
        user = Users.query.filter_by(user_ID=user_ID).first()
        user_Cno = user.user_Cno
        user_name = user.user_name
        user_add = user.user_add
        delivery_status = "Not Yet Dispatched"
        now = date.today()
        payment_date = order_date = now
        cancel_stats = 0
        addit1 = Payment(equip_id=equip_id, user_ID=user_ID, price=price, seller_id=seller_id, user_Cno=user_Cno,
                        user_name=user_name, user_add=user_add, payment_date=payment_date, cancel_stats=cancel_stats)
        addit2 = Delivery(delivery_status=delivery_status, user_ID=user_ID, equip_id=equip_id, seller_id=seller_id, order_date=order_date)
        delit = Wishlist.query.filter_by(equip_id=equip_id, user_ID=session['user_ID']).first()
        wish = Wishlist.query.filter_by(equip_id=equip_id).all()
        for wishes in wish:
            wishes.wish_stats = 1
            db.session.commit()
        db.session.add(addit1)
        db.session.add(addit2)
        db.session.delete(delit)
        db.session.commit()
        return redirect("/myorders")

# <------------My Orders------------->
@app.route("/myorders", methods=['GET', 'POST'])
def my_orders():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        orders = Order_med.query.filter_by(user_ID=session['user_ID']).all()
        pay = Payment.query.filter_by(user_ID=session['user_ID']).all()
        delivery = Delivery.query.filter_by(user_ID=session['user_ID']).all()
        equip = []
        for dl in delivery:
            equipment = Medi_equipment.query.filter_by(equip_id = dl.equip_id).first()
            equip += [equipment]

        return render_template("allorders.html", params=params, orders=orders, pay=pay, delivery=delivery, equip = equip)

# <------------Order Med Cancel------------->
@app.route("/myorders/med/cancel/<int:med_id>", methods=['GET', 'POST'])
def cancel_med(med_id):
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        delit = Delivery.query.filter_by(med_id=med_id, user_ID=session['user_ID']).first()
        if delit.delivery_status != "Not Yet Dispatched":
            flash("Sorry, you cannot cancel your order now.", "error")
            return redirect("/myorders")
        else:
            pay = Payment.query.filter_by(med_id=med_id, user_ID=session['user_ID']).first()
            pay.cancel_stats = 1
            orders = Order_med.query.filter_by(med_id=med_id, user_ID=session['user_ID']).first()
            orders.order_status = "Order Cancelled"
            med = Medicines.query.filter_by(med_id=med_id).first()
            delivery = Delivery.query.filter_by(med_id=med_id, user_ID=session['user_ID']).first()
            delivery.delivery_status = "Order Cancelled"
            med.status = "Approved"
            db.session.commit()
            flash("You have cancelled your order", "info")
            return redirect('/myorders')

# <------------order med cancel------------->
@app.route("/myorders/equip/cancel/<int:equip_id>", methods=['GET', 'POST'])
def cancel_equip(equip_id):
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        delit = Delivery.query.filter_by(equip_id=equip_id, user_ID=session['user_ID']).first()
        if delit.delivery_status != "Not Yet Dispatched":
            flash("Sorry, you cannot cancel your order now.", "error")
            return redirect("/myorders")
        else:
            pay = Payment.query.filter_by(equip_id=equip_id, user_ID=session['user_ID']).first()
            pay.cancel_stats = 1
            equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
            equip.status = "Approved"
            delivery = Delivery.query.filter_by(equip_id=equip_id, user_ID=session['user_ID']).first()
            delivery.delivery_status = "Order Cancelled"
            db.session.commit()
            flash("You have cancelled your order", "info")
            return redirect('/myorders')

# <------------About us------------->
@app.route("/about", methods = ['GET', 'POST'])
def about():
    return render_template("about.html", params=params)

# <------------Feedback------------->
@app.route("/feedback", methods = ['GET', 'POST'])
def feedback():
    return render_template("feedback.html", params=params)

@app.route("/feedback/submit", methods = ['GET', 'POST'])
def feedback_sub():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        if request.method == "POST":
            message = request.form.get("message")
            user_ID=session['user_ID']
            mesg = Feedback(message=message, user_ID=user_ID)
            db.session.add(mesg)
            db.session.commit()
            flash("Thankyou for your Valuable Feedback", "info")
            return redirect("/feedback")

# <------------Logout Mechanism------------->
@app.route("/logout")
def logout():
    if not session.get("user"):
        flash("Login First", "error")
        return redirect("/")
    else:
        session.pop('user')
        flash("Logged out Successfully", "info")
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

# <--------------Med Approve-------------->
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

# <--------------Med Reject-------------->
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

# <--------------Equip View-------------->
@app.route("/equip/approval/view/<int:equip_id>", methods = ['GET', 'POST'])
def equip_approval_view(equip_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equipment = Medi_equipment.query.filter_by(equip_id = equip_id).all()
        equip = Medi_equipment.query.filter_by(equip_id=equip_id).first()
        user_ID = equip.user_ID
        users = Users.query.filter_by(user_ID=user_ID).all()
        return render_template("approvalequipview.html", params=params, equipment=equipment, users=users)
    else:
        return redirect("/")

# <--------------Equip Approve-------------->
@app.route("/equipment/approve/<int:equip_id>", methods = ['GET', 'POST'])
def equip_approve_done(equip_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equip = Medi_equipment.query.filter_by(equip_id = equip_id).first()
        equip.status = "Approved"
        db.session.commit()
        return redirect("/equip/approval")
    else:
        return redirect("/")

# <--------------Equip Reject-------------->
@app.route("/equipment/reject/<int:equip_id>", methods = ['GET', 'POST'])
def equip_approve_reject(equip_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        equip = Medi_equipment.query.filter_by(equip_id = equip_id).first()
        equip.status = "Rejected"
        db.session.commit()
        return redirect("/equip/approval")
    else:
        return redirect("/")

# <--------------Prescription List-------------->
@app.route("/prescription/view", methods = ['GET', 'POST'])
def prescription_view_lst():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        orders = Order_med.query.filter_by(order_status="Prescription Approval Pending...").all()
        users = []
        for od in orders:
            user_ID = od.seller_id
            user = Users.query.filter_by(user_ID=user_ID).first()
            users += [user]
        return render_template("approvalpreslst.html", params=params, orders=orders, users=users)
    else:
        return redirect("/")

# <--------------Prescription View-------------->
@app.route("/pres/view/<int:order_id>", methods=['GET', 'POST'])
def pres_view(order_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        orders = Order_med.query.filter_by(order_id=order_id).all()
        return render_template("approvalpresview.html", params=params, orders=orders)
    else:
        return redirect("/")

# <--------------Prescription Approve-------------->
@app.route("/pres/approve/<int:order_id>", methods=['GET', 'POST'])
def pres_approve(order_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        orders = Order_med.query.filter_by(order_id=order_id).first()
        orders.order_status = "Prescription Approved"
        med_id = orders.med_id
        med = Medicines.query.filter_by(med_id=med_id).first()
        med.status = "Payment Pending..."
        db.session.commit()
        return redirect("/prescription/view")
    else:
        return redirect("/")

# <--------------Prescription Reject-------------->
@app.route("/pres/reject/<int:order_id>", methods=['GET', 'POST'])
def pres_reject(order_id):
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        orders = Order_med.query.filter_by(order_id=order_id).first()
        orders.order_status = "Prescription Rejected"
        med_id = orders.med_id
        med = Medicines.query.filter_by(med_id=med_id).first()
        med.status = "Approved"
        db.session.commit()
        return redirect("/prescription/view")
    else:
        return redirect("/")

# <--------------Feedback View-------------->
@app.route("/admin/feedback/view", methods=['GET', 'POST'])
def feedback_view():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        fb = Feedback.query.filter_by().all()
        users = []
        for feed in fb:
            user_ID = feed.user_ID
            user = Users.query.filter_by(user_ID=user_ID).first()
            users += [user]
        return render_template("adminfeedback.html", params=params, fb=fb, users=users)
    else:
        return redirect("/")

# <--------------Payment Details-------------->
@app.route("/admin/payment/view", methods=['GET', 'POST'])
def payment_view():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "admin":
        pay = Payment.query.filter_by().all()
        med = []
        equip = []
        for py in pay:
            if py.med_id is not None:
                med_id = py.med_id
                medicine = Medicines.query.filter_by(med_id=med_id).first()
                med += [medicine]
            if py.equip_id is not None:
                equip_id = py.equip_id
                equipment = Medi_equipment.query.filter_by(equip_id=equip_id).first()
                equip += [equipment]
        return render_template("adminpaymentdetails.html", params=params, pay=pay, med=med, equip=equip)
    else:
        return redirect("/")

# <--------------Delivery-------------->

# <--------------Delivery Home-------------->
@app.route("/delivery", methods=['GET', 'POST'])
def delivery_home():
    if not session.get("user"):
        return redirect("/")
    elif session['role'] == "delivery":
        members = Users.query.filter_by(user_email=session['user']).all()
        delivery = Delivery.query.filter_by().all()
        user = []
        med = []
        seller = []
        for deliver in delivery:
            if deliver.med_id is not None:
                user_ID = deliver.user_ID
                memb = Users.query.filter_by(user_ID=user_ID).first()
                user += [memb]
                med_id = deliver.med_id
                medicine = Medicines.query.filter_by(med_id=med_id).first()
                med = [medicine]
                seller_id = deliver.seller_id
                membs = Users.query.filter_by(user_ID=seller_id).first()
                seller += [membs]
        user1 = []
        seller1 = []
        equip1 = []
        for deliver1 in delivery:
            if deliver1.equip_id is not None:
                user_ID1 = deliver1.user_ID
                memb1 = Users.query.filter_by(user_ID=user_ID1).first()
                user1 += [memb1]
                equip_id1 = deliver1.equip_id
                equipment1 = Medi_equipment.query.filter_by(equip_id=equip_id1).first()
                equip1 = [equipment1]
                seller_id1 = deliver1.seller_id
                membs1 = Users.query.filter_by(user_ID=seller_id1).first()
                seller1 += [membs1]
        return render_template("deliveryhome.html", params=params, members=members, user=user, med=med, seller=seller, delivery=delivery, equip1=equip1, user1=user1, seller1=seller1)
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