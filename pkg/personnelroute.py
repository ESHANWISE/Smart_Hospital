from functools import wraps
import random,os,string
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# local imports follows below
from pkg import app,csrf
from pkg.models import *
from pkg.forms import Pwd,PersonnelAccount


# creating a decorator to be checking login
def login_req(f):
    @wraps(f) #this ensures that the details(meta data) about the original function f, that is being decorated id still available. for tha reason, we from functools import wraps
    def login_check(*args, **kwargs):
        if session.get("pers") != None:
            return f(*args, **kwargs)
        else:
            flash("Access Denied, Please login",category="error")
            return render_template('user/per.html')
    return login_check

def requires_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        perid = session.get('pers')
        personnel = db.session.query(Personnel).get(perid)

        if personnel and personnel.per_kyc:
            # Check if there is a KYC entry and if it's approved
            for a in personnel.per_kyc:
                if a.kyc_status != 'approved':
                    flash('You need to be verified to access that page.', category="error")
                    return redirect(url_for('kyc'))
        else:
            flash('You need to be verified to access that page.', category="error")
            return redirect(url_for('kyc'))

        return f(*args, **kwargs)
    return decorated_function
#################################################################3333333333333333#######################################################



# # change state
# @app.route('/per_profile/',methods=["POST","GET"])
# @login_req
# # @requires_verification
# def state_lga():
#     id = session.get("pers")
#     personnel = db.session.query(Personnel).get(id)




# change state
@app.route('/per_profile/',methods=["POST","GET"])
@login_req
# @requires_verification
def state_lga():
    id = session.get("pers")
    personnel = db.session.query(Personnel).get(id)
    st = db.session.query(State).all()
    lga = db.session.query(Lga).all()
    if request.method == "GET":
        return render_template("perdash/profile.html",personnel=personnel,st=st,lga=lga)
    else:
        state = request.form.get("state")
        lg = request.form.get("lga")
        id = session.get("pers")
        per = db.session.query(Personnel).filter(Personnel.per_id==id).all()
        for a in per:
            a.per_state_id = state
        for b in per:
            b.per_lga = lg
        db.session.commit()
        flash("State successfully changed",category="info")
        return redirect("/per_profile/")

#  change specialzatyion
@app.route('/per_profile/',methods=["POST","GET"])
@login_req
def special():
    id = session.get("pers")
    personnel = db.session.query(Personnel).get(id)
    sp = db.session.query(Specialization).all()
    st = db.session.query(State).all()
    lga = db.session.query(Lga).all()
    if request.method == "GET":
        return render_template("perdash/profile.html",personnel=personnel,sp=sp,st=st,lga=lga)
    else:
        spec = request.form.get("spec")
        id = session.get("pers")
        per = db.session.query(Personnel).filter(Personnel.per_id==id).all()
        for a in per:
            a.per_spec_id = spec
        db.session.commit()
        flash("Specialization successfully changed",category="info")
        return render_template("perdash/profile.html",sp=sp,personnel=personnel,per=per)


    


# Profile pictur changing
@app.route("/per_profile/",methods=["POST","GET"])
@login_req
def changedp1():
    id = session.get("pers")
    personnel = db.session.query(Personnel).get(id)
    if request.method == "GET":
        return render_template("perdash/profile.html",personnel=personnel)
    else:#form is being submitted
        pers = db.session.query(Personnel).filter(Personnel.per_id==id).all(id)
        pix1 = request.files.get('dp')
        filename = pix1.filename
        pix1.save("pkg/static/uploads/" + filename)
        pers.per_profile_picture = filename
        db.session.commit()
        flash('Profile Picture Updated',category='info')
        return redirect("/per_profile/")



# Password change
@app.route('/per_profile/',methods = ["POST","GET"])
@login_req
def edit_password1():
    id = session.get('pers')
    personnel = db.session.query(Patient).get(id)
    if request.method == "GET":
        return render_template("perdash/profile.html",personnel=personnel)
    else:
        oldpwd = request.form.get('oldpwd')
        newpwd = request.form.get('newpwd')
        hashed_pwd = personnel.pat_password
        if check_password_hash(hashed_pwd,oldpwd) == True:
            personnel.pat_password = newpwd
            flash('Password successfully changed',category="info")
            return redirect("/per_profile/")
        else:
            flash("Your old password is incorrect")
            return redirect("/per_profile/")



@app.route('/per_profile/')
@login_req
def edit_number1():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    if request.method == "GET":
        return render_template("perdash/profile.html",personnel=personnel)
    else:
        oldphn = request.form.get('oldphn')
        newphn = request.form.get('newphn')
        if oldphn == personnel.pat_phn:
            personnel.pat_phn = newphn
            db.session.commit()
            flash("Phone Number successfully changed",category='success')
            return redirect('/per_profile/')
        else:
            flash('Old phnone number is incorrect',category='error')
            return redirect('/per_profile/')




# contact or chat
@app.route('/contact/')
@login_req
def contact():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    return render_template("perdash/contact.html",personnel=personnel)


# Give feedback
@app.route('/feedback/')
@login_req
def feedback():
    return "view"


# view all patients medical records
@app.route('/view_pat_med/<int:id>/')
@requires_verification
@login_req
def view_pat_med(id):
    perid = session.get('pers')
    personnel = db.session.query(Personnel).get(perid)
    med = db.session.query(HealthRecord).filter(HealthRecord.health_pat_id==id).all()
    lab = db.session.query(Labtest).filter(Labtest.lab_pat_id==id).all()
    # med = db.session.query(HealthRecord).get(id)
    # a = {"history":med.medical_history,"allergies":med.allergies,"Medications":med.Medications}
    # return jsonify(a) if med else jsonify({}), 404
    return render_template("perdash/med_rec.html",personnel=personnel,med=med,lab=lab)


# view all patients
@app.route('/kyc/', methods=["POST", "GET"])
@login_req
def kyc():
    perid = session.get('pers')
    personnel = db.session.query(Personnel).get(perid)
    kyc = db.session.query(Kyc).filter_by(kyc_per_id=perid).first()  # Check if KYC exists for this user
    if request.method == "GET":
        return render_template("perdash/kyc.html", personnel=personnel, kyc=kyc)
    else:
        if kyc:
            flash("KYC has already been submitted and can't be uploaded again.", category="error")
            return redirect('/kyc/')
        else:
            kyc_file = request.files.get('kyc')
            if kyc_file:
                filename = secure_filename(kyc_file.filename)
                kyc_file.save(os.path.join("pkg/static/kyc/", filename))
                k = Kyc(kyc_pix=filename, kyc_per_id=perid)
                db.session.add(k)
                db.session.commit()
                flash('Certificate successfully uploaded', category='info')
                return redirect("/kyc/")
            else:
                flash('No file selected for upload.', category='error')
                return redirect("/kyc/")


        



# view all patients
@app.route('/view_patients/')
@requires_verification
@login_req
def view_patients():
    return "view"

# view reviews
@app.route('/view_reviews/')
@requires_verification
@login_req
def view_reviews():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    rev = db.session.query(Reviews).filter(Reviews.rev_per_id==id).all()
    return render_template("perdash/reviews.html",personnel=personnel,rev=rev)



# Delete appointment for approved
@app.route("/delete_app/<int:id>/")
@requires_verification
@login_req
def delete_app1(id):
    perid = session.get('pers')
    cancel = db.session.query(Appointment).get(id)
    db.session.delete(cancel)
    db.session.commit()
    flash("Appointment Cancelled")
    return redirect("/approved/")
# Approved appointments
@app.route('/approved/')
@requires_verification
@login_req
def approved():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    app = db.session.query(Appointment).filter(Appointment.app_per_id==id,Appointment.app_status=="approved").all()
    return render_template("perdash/approved_app.html",personnel=personnel,app=app)


# Delete appointment for approved
@app.route("/delete_app/<int:id>/")
@requires_verification
@login_req
def delete_app2(id):
    perid = session.get('pers')
    cancel = db.session.query(Appointment).get(id)
    db.session.delete(cancel)
    db.session.commit()
    flash("Appointment Cancelled")
    return redirect("/declined/")
# Declined appointments
@app.route('/declined/')
@requires_verification
@login_req
def declined():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    app = db.session.query(Appointment).filter(Appointment.app_per_id==id,Appointment.app_status=="declined").all()
    return render_template("perdash/declined_app.html",personnel=personnel,app=app)




# View appointments
@app.route('/view_recent_app/')
@requires_verification
@login_req
def view_recent_app():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    app = db.session.query(Appointment).filter(Appointment.app_per_id==id,Appointment.app_status=="pending").all()
    return render_template("perdash/recent_app.html",personnel=personnel,app=app)

# med history
@app.route('/app_history/')
@requires_verification
@login_req
def app_history():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    app = db.session.query(Appointment).filter(Appointment.app_per_id==id).all()
    return render_template("perdash/app_history.html",personnel=personnel,app=app)





def get_patient_id(appointment_id):
    appointment = Appointment.query.filter_by(app_id=appointment_id).first()
    if appointment:
        return appointment.app_pat_id
    else:
        return None


@app.route('/app_feedback/<int:id>/', methods=['POST', 'GET'])
def app_feedback(id):
    if request.method == "GET":
        # Code to retrieve the appointment and check if it's declined
        appointment = Appointment.query.filter_by(app_id=id).first()
        if appointment and appointment.app_status == 'declined':
            # Retrieve patient and personnel information for display
            perid = session.get('pers')
            personnel = db.session.query(Personnel).get(perid)
            patient = db.session.query(Patient).get(appointment.app_pat_id)
            return render_template("perdash/feedback.html", personnel=personnel, patient=patient, appointment=appointment)
        else:
            flash("Appointment is not declined", category="error")
            return redirect("/app_history/")
    else:
        feed = request.form.get("feed")
        perid = session.get('pers')
        appid = id  # Use the provided appointment ID

        # Retrieve patient ID based on the appointment ID
        patid = get_patient_id(appid)

        if patid is not None:
            feedback = Feedback(feed_message=feed, feed_pat_id=patid, feed_per_id=perid, feed_app_id=appid)
            db.session.add(feedback)
            db.session.commit()
            flash("Message successfully sent", category="info")
        else:
            flash("Invalid appointment ID", category="error")

        return redirect("/app_history/")









# view patients
@app.route('/show_users/')
@requires_verification
@login_req
def show_users():
    perid = session.get('pers')
    personnel = db.session.query(Personnel).get(perid)
    app1 = db.session.query(Appointment).all()
    return render_template("perdash/app_history",personnel=personnel,app1=app1)


@app.route('/approve_appointment/<int:appointment_id>')
@requires_verification
@login_req
def approve_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.app_status = 'approved'
        db.session.commit()
        flash("Appointment has been successfully Approved",category="info")
    return redirect('/app_history')

@app.route('/decline_appointment/<int:appointment_id>')
@requires_verification
@login_req
def decline_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.app_status = 'declined'
        db.session.commit()
        flash("Appointment has been successfully Declined",category="danger")
    return redirect('/app_history/')


# transactions
@app.route('/transaction_history/')
@requires_verification
@login_req
def transactions():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    fin = db.session.query(Financial).filter(Financial.fin_per_id==id).all()
    return render_template("perdash/transaction.html",personnel=personnel,fin=fin)

# verification
# @app.route("/verification",methods=["POST","GET"])
# def verification():
#     id = session.get('pers')
#     user = db.session.query(Personnel).get(id)
#     if request.method == "GET":
#         return render_template('/perdash/verification.html',user=user)
#     else:
#         spec = request.form.get("spec")
#         state = request.form.get("state")
#         lga = request.form.get("lga")
        
#         spec = Personnel()
#         pass




# dashboard
@app.route("/perdash/")
@login_req
def perdash():
    id = session.get('pers')
    personnel = db.session.query(Personnel).get(id)
    app = db.session.query(Appointment).filter(Appointment.app_per_id==id)
    # kyc = db.session.query(Kyc).get(id)
    return render_template("perdash/mydash.html",personnel=personnel,app=app)



 #Logout route
#  checks if the seesion is empty if True, do nothing else remove the user and redirect them back to home page
@app.route("/personnel/logout/")
def personnel_logout():
    if session.get("pers") != None:
        session.pop("pers",None)
        return redirect('/personnellogin/')
    else:
        return render_template("user/per.html")
    

# clearing header cache
# This route helps to clear all cache fr the browsers header so that they cannot use ther arrow btn to renter the dashboard.
@app.after_request
def after_request(response):
    response.headers["cache-control"]="no-cache, no-store, must-validate"
    return response

  # login route
@app.route('/personnellogin/',methods=["POST","GET"])
def personnel_login():
    p = PersonnelAccount()
    spec = db.session.query(Specialization).all()
    state = db.session.query(State).all()
    lga = db.session.query(Lga).all()
    bank = db.session.query(Bank).all()
    if request.method == "GET":
        return render_template('user/per.html',p=p,state=state,lga=lga,spec=spec,bank=bank)
    else:
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        deets = db.session.query(Personnel).filter(Personnel.per_email==email).first()
        if deets.per_email==email and deets.per_restricted==False:
            hashed_pwd = deets.per_password
            if check_password_hash(hashed_pwd,pwd) ==True:
                session['pers']=deets.per_id
                return redirect("/perdash/")
            else:
                flash("Invalid credentials, try again",category="error")
                return redirect("/personnellogin/")
        else:   
            flash("Your Acoount has been restricted",category="error")
            return redirect("/personnellogin/")


# Create account route
@app.route("/personnel/",methods =["POST","GET"])
def personnel():
    p = PersonnelAccount()
    spec1 = db.session.query(Specialization).all()
    state1 = db.session.query(State).all()
    lga1 = db.session.query(Lga).all()
    bank = db.session.query(Bank).all()
    if request.method == "GET":
        return render_template("user/per.html", p=p,spec1=spec1,lga1=lga1,state1=state1,bank=bank)
    else:
        
        # retrieve files
        allowed = ["jpg","png","jpeg"]
        filesobj = request.files['photo']
        filename= filesobj.filename
        newname = "default1.png"#this is the default  cover 
        # here we are checking if the user did not upload any image in the fields. the chk is on file name is on filaname because if there is a file there must be a name
        if filename == '':#No file was uploaded
            flash("Profile picture not uploaded",category="error")
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
        spec = request.form.get("special")
        state = request.form.get("state")
        lga = request.form.get("lga")
        liscense = request.form.get("license")
        address = request.form.get("address")
        bank = request.form.get("bank")
        acc_num =request.form.get("acc_num")
        
        em = db.session.query(Personnel).filter(Personnel.per_email==email).first()
        if em:
            flash("Email Already taken Please Use Another email Address",category="error")
            return redirect("/personnellogin/")
        else:
        # license = request.form.get("licence")
            per = Personnel(per_profile_picture=newname,liscence_number=liscense,per_lga=lga,
                        per_spec_id = spec,per_state_id =state,
                        per_firstname=fname,per_lastname=lname,per_password=hash_pwd,
                        per_phn=phn,per_address=address,per_mStatus=mStatus,per_gender=gender,
                        per_email=email,per_dob=dob,per_bank_id=bank,acc_num=acc_num)
            db.session.add(per)
            db.session.commit()
            flash("An account has been created for you. Please login", category="success")
            return redirect("/personnellogin/")
        # else:
        #     flash('Could not create an account for you',category="error")
        #     return redirect("/personnel/")
    

    # lga route

@app.route("/lga/<stateid>/")
def load_lgas1(stateid):
    records = db.session.query(Lga).filter(Lga.state_id==stateid).all()
    str2return = "<select class='form-control mt-3' name='lga'>"
    optstr = "<option value=''>Please Select</option>"
    for r in records:
        optstr = "<option>" + r.lga_name + "</option>"
        str2return = str2return + optstr
    str2return=str2return + optstr + "</select>"
    return str2return