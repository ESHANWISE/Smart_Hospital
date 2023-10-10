import json,requests,random,string,os
from functools import wraps
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify
from flask_socketio import SocketIO,emit,join_room
from werkzeug.security import generate_password_hash, check_password_hash

# local imports follows below
from pkg import app,csrf
from pkg.models import *
from pkg.forms import CreateAccount,Pwd,PaymentForm


# Initialize SocketIO
socketio = SocketIO(app)

# creating a decorator to be checking login
def login_required(f):
    @wraps(f) #this ensures that the details(meta data) about the original function f, that is being decorated id still available. for tha reason, we from functools import wraps
    def login_check(*args, **kwargs):
        if session.get("userloggedin") != None:
            return f(*args, **kwargs)
        else:
            flash("Access Denied, Please login",category="error")
            return redirect('/login')
    return login_check
# To use login_required, place it after the route decorator over any route that needs authentication


# profile pix
@app.route("/profile/",methods=["POST","GET"])
@login_required
def changedp():
    id = session.get("userloggedin")
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/profile.html",prof=prof)
    else:#form is being submitted
        pix = request.files.get('dp')
        filename = pix.filename
        pix.save("pkg/static/uploads/" + filename)
        prof.profile_picture = filename
        db.session.commit()
        flash('Profile Picture Updated',category='info')
        return redirect("/profile/")
    


@app.route('/profile/',methods = ["POST","GET"])
@login_required
def edit_password():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/profile.html",prof=prof)
    else:
        oldpwd = request.form.get('oldpwd')
        newpwd = request.form.get('newpwd')
        hashed_pwd = prof.pat_password
        if check_password_hash(hashed_pwd,oldpwd) == True:
            prof.pat_password = newpwd
            flash('Password successfully changed',category="info")
            return redirect("/profile/")
        else:
            flash("Your old password is incorrect")
            return redirect("/profile/")


# Phone number changed
@app.route('/profile/',methods = ["POST","GET"])
@login_required
def edit_number():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/profile.html",prof=prof)
    else:
        oldphn = request.form.get('oldphn')
        newphn = request.form.get('newphn')
        if oldphn == prof.pat_phn:
            prof.pat_phn = newphn
            db.session.commit()
            flash("Phone Number successfully changed",category='success')
            return redirect('/profile/')
        else:
            flash('Old phnone number is incorrect',category='error')
            return redirect('/profile/')
        

# All dashboard routes

# Treatment
@app.route("/treatment/")
@login_required
def treatment():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/treatment.html",prof=prof)

# this route displays all the lab results
@app.route("/labdisplay/")
@login_required
def labdisplay():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    labdisp = db.session.query(Labtest).filter(Labtest.lab_pat_id==id).all()
    return render_template("userdash/labdisplay.html",labdisp=labdisp,prof=prof)



# labform route
@app.route("/lab/",methods=["POST","GET"])
@login_required
def lab():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    lab = db.session.query(Labtest).all()
    applab = db.session.query(Appointment).filter(Appointment.app_id==id)
    if request.method == "GET":
        return render_template("userdash/labform.html",prof=prof,applab=applab)
    else:
        lab = request.form.get("labtest")
        # retrieve files
        allowed = ["jpg","png","jpeg"]
        filesobj = request.files['file']
        filename= filesobj.filename
        newname = "default.png"#this is the default  cover 
        # here we are checking if the user did not upload any image in the fields. the chk is on file name is on filaname because if there is a file there must be a name
        if filename == '':#No file was uploaded
            flash("Profile picture was not uploaded",category="error")
        else:#file was selected
            pieces =filename.split('.')
            exist = pieces[-1].lower()
            if exist in allowed:
                newname = str(int(random.random()*10000000000)) +filename#this is to help us make the image name as unique as possible to avoid clash of names
                filesobj.save("pkg/static/uploads/" + newname)
            else:
                flash("File extention type not allowed, file was not uploaded", category='error')
    l = Labtest(lab_result=newname,lab_test=lab,lab_pat_id=id)
    db.session.add(l)
    db.session.commit()
    flash("Files Uploaded successfully")
    return render_template("userdash/labform.html",prof=prof)



# medicalrecords
@app.route("/medicalrecords/")
@login_required
def medicalrecords():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    health = db.session.query(HealthRecord).filter(HealthRecord.health_pat_id==id).all()
    return render_template("userdash/medicalrecords.html",prof=prof,health=health)
    




# appointment profile viewing
@app.route("/appointment/<int:id>/",methods = ["POST","GET"])
@login_required
def personnel_deets(id):
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    person = db.session.query(Personnel).get(id)
    return render_template("userdash/appointment.html",prof=prof,person=person)


# list of all appointments
@app.route("/all_app/")
@login_required
def all_app():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    all = db.session.query(Appointment).filter(Appointment.app_pat_id==id).all()
    fin = db.session.query(Financial).filter(Financial.fin_pat_id==id).all()
    return render_template("userdash/all_app.html",all=all,prof=prof,fin=fin)


# appointment querying
@app.route("/appointment/",methods = ["POST","GET"])
@login_required
def appointment():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    spec = db.session.query(Specialization).all()
    state = db.session.query(State).all()
    lga = db.session.query(Lga).all()
    per= db.session.query(Personnel).all()
    app = db.session.query(Appointment).filter(Appointment.app_pat_id==id).all()
    rev = db.session.query(Reviews).filter(Reviews.rev_pat_id==id).all()
    if request.method == "GET":
        return render_template("userdash/appointment.html",prof=prof,spec=spec,state=state,app=app,lga=lga,per=per,rev=rev)
    else:
       
        spec1 = request.form.get("spec")
        state1 = request.form.get("state")
        lga1 = request.form.get("lga")
        query = db.session.query(Personnel).filter(Personnel.per_lga==lga1,Personnel.per_spec_id==spec1,Personnel.per_state_id==state1).all()
        if query:
            return render_template("userdash/appointment.html",query=query,prof=prof,app=app,per=per)
        else:
            flash("No result found",category="error")
            return render_template("userdash/appointment.html",prof=prof,app=app,per=per)


# booking id 
@app.route("/personnel/<id>")
def personnel_id(id):
    book = Appointment.query.get_or_404(id)
    return render_template("userdash/appointment.html", book=book)


@app.route("/book_app/",methods=["POST","GET"])
@login_required
def book_app():
    patid = session.get('userloggedin')
    prof = db.session.query(Patient).get(patid)
    # p = db.session.query(Personnel).get(id)
    if request.method == "GET":
        return render_template("userdash/appointment.html",prof=prof)
    else:
        date = request.form.get("date")
        time = request.form.get("time")
        userid = session["userloggedin"]
        per_id = request.form.get("appid")
        app = Appointment(app_date=date,app_time=time,app_pat_id=userid,app_per_id=per_id)
        db.session.add(app)
        db.session.commit()
        flash("Appointment successfully Booked",category="info")
        return redirect('/appointment/')







@app.route('/book_appointment/<int:user_id>/<appointment_id>', methods=['POST'])
def book_appointment(user_id, appointment_id):
    user = Personnel.query.get(user_id)
    appointment = Appointment.query.get(appointment_id)

    if user and appointment:
        appointment.user = user
        db.session.commit()

    return render_template('userdash/appointment.html',user=user,appointment=appointment) 


@app.route("/home_review/")
def home_review():
    revs = db.session.query(Reviews).all()
    return render_template("user/index.html",revs=revs)



# view doctors profils before booking appointments
@app.route("/view_per/<int:id>/")
@login_required
def view_per(id):
    per = db.session.query(Personnel).get(id)
    for b in per.per_kyc:
        b.kyc_status
    a = {"fname":per.per_firstname,"lname": per.per_lastname,"pix":per.per_profile_picture,"state":per.per_state.state_name,"lga":per.per_lga,"var_status":b.kyc_status,"gender":per.per_gender}
    return jsonify(a) if per else jsonify({}), 404


# Delete appointment
@app.route("/delete_app/<int:id>/")
@login_required
def delete_app(id):
    patid = session.get('userloggedin')
    cancel = db.session.query(Appointment).get(id)
    db.session.delete(cancel)
    db.session.commit()
    flash("Appointment Cancelled")
    return redirect("/all_app/")


# Review of previous appointments
@app.route("/review/<int:personnel_id>", methods=["GET", "POST"])
@csrf.exempt
@login_required
def review(personnel_id):
    userid = session["userloggedin"]
    prof = db.session.query(Patient).get(userid)
    if request.method == "GET":
        return render_template("userdash/all_app.html",prof=prof)
    else:
        content = request.form.get("txt")
        userid = session["userloggedin"]
        r = Reviews(rev_pat_id=userid, rev_per_id=personnel_id, message=content)
        db.session.add(r)
        db.session.commit()
        flash("Review submission was successful")
        return redirect("/all_app/")


# @app.route("/review/",methods=["GET","POST"])
# @login_required
# def review():
#     content = request.form.get("content")
#     userid = session["userloggedin"]
#     personnel = request.form.get("personnel")
#     r = Reviews(rev_pat_id=userid,rev_per_id=personnel,message=content)
#     db.session.add(r)
#     db.session.commit()
#     return "Review sumbmission was successful"
        













# vitals
@app.route("/vitals/")
@login_required
def vitals():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/vitals.html",prof=prof)
    return render_template("userdash/vitals.html")


# billings
@app.route("/billing/")
@login_required
def billing():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    fin = db.session.query(Financial).all()
    if request.method == "GET":
        return render_template("userdash/billing.html",prof=prof,fin=fin)
    return render_template("userdash/billing.html")


# billings
@app.route("/medform/",methods=["POST","GET"])
@login_required
def med_form():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("userdash/med_form.html",prof=prof)
    else:
        userid =session.get('userloggedin')
        medications = request.form.get("medications")
        allergies = request.form.get("allergies")
        histories = request.form.get("histories")
        m = HealthRecord(Medications =medications,allergies =allergies,medical_history =histories,health_pat_id=userid)
        db.session.add(m)
        db.session.commit()
        flash("Medical Records successfully Updated")
    return render_template("userdash/med_form.html",prof=prof)

##################################################### message #######################################################################


# message


# Route to send a message
@app.route('/patient_chat', methods=['GET', 'POST'])
def patient_chat():
    # Assuming the user is logged in and is a patient
    user_id = session.get('user_id')
    prof = Patient.query.get(user_id)

    if request.method == 'POST':
        message_content = request.form['message']
        new_message = Message(msg_content=message_content, patient_id=user_id)
        db.session.add(new_message)
        db.session.commit()
        # Emit the message to the relevant room
        socketio.emit('message_received', {'message': message_content}, room=f'patient_{user_id}')

    return render_template('userdash/message.html', prof=prof)

# SocketIO event to join a room for a specific chat
@socketio.on('join_patient_room')
def on_join_patient(data):
    user_id = data['user_id']
    join_room(f'patient_{user_id}')





# @app.route("/message/", methods=["POST","GET"])
# @login_required
# def message():
#     id = session.get('userloggedin')
#     prof = db.session.query(Patient).get(id)
#     if request.method == "GET":
#         return render_template("userdash/message.html",prof=prof)
   
#     return render_template("userdash/message.html")

################################################################################################################################################
  
#  dashboard this route takes of people who wants to revisit the dashboard after they are loged out through the back arrow button in ther
# browser. it will check if there login details is saved in the session if true, it takes them to dashboard if false it redirects them to
# login page with a flashed message
@app.route("/dashboard/")
@login_required
def dashboard():
    id = session.get('userloggedin')
    prof = db.session.query(Patient).get(id)
    return render_template("userdash/dashboard.html",prof=prof)
   

 #Logout route
#  checks if the seesion is empty if True, do nothing else remove the user and redirect them back to home page
@app.route("/logout/")
def logout():
    if session.get("userloggedin") != None:
        session.pop("userloggedin",None)
        return redirect('/pat')
    else:
        return render_template("user/pat.html")
    
    
# login route
@app.route('/login/',methods=["POST","GET"])
def login():
    # patients= db.session.query(Patient).get()
    f = CreateAccount()
    if request.method == "GET":
        return render_template('user/pat.html',f=f)
    else:
        f.validate_on_submit()
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        deets = db.session.query(Patient).filter(Patient.pat_email==email).first()
        if deets != None:
            hashed_pwd = deets.pat_password
            if check_password_hash(hashed_pwd,pwd) ==True:
                session['userloggedin']=deets.pat_id
                return redirect("/dashboard")
            else:
                flash("Invalid credentials, try again",category="error")
                return redirect("/pat")
        else:   
            flash("Invalid credentials, try again",category="error")
            return redirect("/pat")
        

# Create account route
@app.route("/pat/",methods =["POST","GET"])
def pat():
    f = CreateAccount()
    if request.method == "GET":
        return render_template("user/pat.html", f=f)
    else:
        if f.validate_on_submit():

             # retrieve files
            allowed = ["jpg","png","jpeg"]
            filesobj = request.files['photo']
            filename= filesobj.filename
            newname = "default.png"#this is the default  cover 
            # here we are checking if the user did not upload any image in the fields. the chk is on file name is on filaname because if there is a file there must be a name
            if filename == '':#No file was uploaded
                flash("Profile picture was not uploaded",category="error")
            else:#file was selected
                pieces =filename.split('.')
                exist = pieces[-1].lower()
                if exist in allowed:
                    newname = str(int(random.random()*10000000000)) +filename#this is to help us make the image name as unique as possible to avoid clash of names
                    filesobj.save("pkg/static/uploads/" + newname)
                else:
                    flash("File extention type not allowed, file was not uploaded", category='error')


            fname = request.form.get("fname")
            lname = request.form.get("lname")
            email = request.form.get("email")
            dob = request.form.get("Dob")
            pwd = request.form.get("pwd")
            hash_pwd = generate_password_hash(pwd)
            phn = request.form.get("phn")
            gender =  request.form.get("gender")
            mStatus =  request.form.get("mStatus")
            insurance =  request.form.get("insurance")
            address = request.form.get("address")

            em = db.session.query(Patient).filter(Patient.pat_email==email).first()
            if em:
                flash("Email Already taken Please Use Another email Address",category="error")
                return redirect("/pat/")
            else:
                r = Patient(profile_picture=newname,
                            pat_firstname=fname,pat_lastname=lname,pat_password=hash_pwd,
                            pat_phn=phn,pat_address=address,pat_mStatus=mStatus,pat_gender=gender,
                            insurance_number=insurance,pat_email=email,pat_dob=dob)
                db.session.add(r)
                db.session.commit()
                session['userloggedin']=lname
                flash("An account has been created for you. Please login", category="success")
                return redirect("/login")
        else:
            flash("Please kindly go back to recreate your account.",category='error')
            return render_template("user/pat.html",f=f)


# Home Page
@app.route("/")
def homepage():
    revs = Reviews.query.limit(3).all()
    return render_template("user/index.html",revs=revs)


# clearing header cache
# This route helps to clear all cache fr the browsers header so that they cannot use ther arrow btn to renter the dashboard.
@app.after_request
def after_request(response):
    response.headers["cache-control"]="no-cache, no-store, must-validate"
    return response


# Forgot password route
@app.route('/forgot_password/')
def forgot_password():
    return render_template('user/forgot-password.html')

# Password suggestion
@app.route('/suggestpwd/', methods={"POST","GET"})
def suggestpwd():
    sp = Pwd()
    if request.method == "GET":
        return render_template("user/suggestpwd.html", sp=sp)
    else:
        # sp.validate_on_submit()
        aplpha = int(request.form.get("alpha"))
        symbol = int(request.form.get("symbol"))
        numbers = int(request.form.get("numbers"))

        pwd = []
        for i in range(1, aplpha +1):
            pwd.append(random.choice(Pwd.letters))

        for j in range(1, numbers +1): 
            pwd.append(random.choice(Pwd.number))

        for k in range(1, symbol + 1):
            pwd.append(random.choice(Pwd.symbols))

        random.shuffle(pwd)
        New = ""
        for a in pwd:
            New += a
        with open ("suggested password.txxt","a") as p:
            p.write(f"Your Password Suggestion Is {New} \n")
        flash("Password suggested succesfully Check your email.",category="success")
        return render_template("user/suggestpwd.html",sp=sp)


# ################################################### Payment Gateway Route ######################################################################



def generate_string(howmany):#call this function as renerate_string(10)
    x = random.sample(string.digits,howmany)
    return ''.join(x)






@app.route("/payment/",methods=["POST","GET"])
@login_required
def payment():
    # donate = PaymentForm()
    if request.method == "GET":
        prof = db.session.query(Patient).get(session["userloggedin"])
        # pen = db.session.query(Appointment).get(id)
        return render_template("userdash/payment.html",prof=prof)

    else:
    # if donate.validate_on_submit():
        #retrieve formmdata
        #insert into db
        #generate a transaction reference
        #redirect to a confirmation page
        amt = 2000000
        donor = request.form.get("fullname")
        email = request.form.get("email")
        personnel_id = request.form.get('personnel_id')
        ref = "SH" + str(generate_string(8))
        don = Financial(fin_fullname=donor,fin_email=email,fin_amount=amt,fin_pat_id=session["userloggedin"],fin_status="pending",payment_invoice=ref,fin_per_id=personnel_id)
        db.session.add(don)
        db.session.commit()
        #save the reference no in session
        session["trxno"] = ref
        #redirect to a confirmation page
        return redirect("/confirm_donation/")
        # else:
        #     prof = db.session.query(Patient).get(session["userloggedin"])
        #     return render_template("userdash/payment.html",donate=donate,prof=prof)



@app.route("/confirm_donation/")
@login_required
def confirm_donation():
    """We want to display the details of the transaction saved from previous page"""
    prof = db.session.query(Patient).get(session["userloggedin"])
    if session.get("trxno") == None: #means the are visiting here directly
        flash("Please complete this form",category="error")
        return redirect("/payment/")
    else:
        donation_deets = Financial.query.filter(Financial.payment_invoice ==session["trxno"]).first()
        return render_template("userdash/payment_conf.html",donation_deets=donation_deets,prof=prof)



@app.route("/landing")
@login_required
def landing_page():
    refno = session.get("trxno")
    transaction_deets = db.session.query(Financial).filter(Financial.payment_invoice ==refno).first()
    url="https://api.paystack.co/transaction/verify/" +transaction_deets.payment_invoice 
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_7056bf4a73fba68635f48106f022172f378e30af"}
    response = requests.get(url,headers=headers)
    rspjson = json.loads(response.text)
    # return rspjson #retieve the details and update your database
    if rspjson["status"] == True:
        paystatus = rspjson["data"]["gateway_response"]
        transaction_deets.fin_status = "approved"
        db.session.commit()
        flash("Payment was successful")
        return redirect("/all_app/")#paysatck page will load
    else:
        # flash("Please complete the form again")
        flash("Payment failed")
        return redirect("/reports")



@app.route("/initialize/paystack",methods=["POST","GET"])
@login_required
def initialize_paystack():
    userid = session["userloggedin"]
    deets = db.session.query(Patient).get(userid)
    # transaction details
    refno = session.get("trxno")
    transaction_details = db.session.query(Financial).filter(Financial.payment_invoice ==refno).first()
    # make a curl request to the paystack endpoint
    url="https://api.paystack.co/transaction/initialize"
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_7056bf4a73fba68635f48106f022172f378e30af"}
    data={ 
        "email": deets.pat_email, 
        "amount": transaction_details.fin_amount,
        "reference":refno
        }
    response = requests.post(url,headers=headers,data=json.dumps(data))
    # #extract json fro the response coming from paysatck
    rspjson = response.json()
    # return rspjson
    if rspjson["status"] == True:
        redirectURL = rspjson["data"]["authorization_url"]
        return redirect(redirectURL)#paysatck page will load
    else:
        flash("Please complete the form again")
        return redirect("/payment/")



######################################################### subscription ########################################################################


@app.route('/sub/', methods=['GET', 'POST'])
def subscribe():
    if request.method == "GET":
        return render_template('user/index.html')
    else:
        email = request.form.get("email")
        s = Subscription(sub_email=email)  # For demonstration, add to the mock database
        db.session.add(s)
        db.session.commit()
        flash('Email Successfully Added!', category="info")

        return render_template('user/index.html' )
    


@app.route("/per_review/<int:id>")
def per_review(id):
    patid = session.get('userloggedin')
    prof = db.session.query(Patient).get(patid)
    revs = db.session.query(Reviews).filter(Reviews.rev_per_id==id).all()
    return render_template("userdash/appointment.html",prof=prof,revs=revs)

    
        































