from functools import wraps
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify

# local imports follows below
from pkg import app
from pkg.models import *


# creating a decorator to be checking login
def login_req_admin(f):
    @wraps(f) #this ensures that the details(meta data) about the original function f, that is being decorated id still available. for tha reason, we from functools import wraps
    def login_check(*args, **kwargs):
        if session.get("Admin") != None:
            return f(*args, **kwargs)
        else:
            flash("Access Denied, Please login",category="error")
            return render_template('admin/login.html')
    return login_check




###################################################### Specialization #########################################################################

@app.route("/pop/",methods=["POST","GET"])
def pop():
    if request.method == "GET":
        return render_template("admin/pop.html")
    else:
        pop = request.form.get("pop")
        s = Specialization(spec_name=pop)
        db.session.add(s)
        db.session.commit()
        flash("Specialization Successfully Added",category="info")
        return redirect("/pop/")


@app.route("/all_payment/")
@login_req_admin
def all_payment():
    personnel = db.session.query(Personnel).all()
    fin = db.session.query(Financial).all()
    return render_template("admin/all_payment.html",personnel=personnel,fin=fin)  




####################################################### ALL ABOUT PERSONNELS STARTED HERE ############################################################################################

@app.route('/approve_kyc/<int:kyc_id>')
@login_req_admin
def approve_kyc(kyc_id):
    kyc = Kyc.query.get(kyc_id)
    if kyc:
        kyc.kyc_status = 'approved'
        db.session.commit()
        flash("Kyc has been successfully Approved",category="info")
    return redirect('/admin/allPersonnels/')

@app.route('/decline_kyc/<int:kyc_id>')
@login_req_admin
def decline_kyc(kyc_id):
    kyc = db.session.query(Kyc).get(kyc_id)
    if kyc:
        kyc.kyc_status = 'declined'
        db.session.commit()
        flash("Kyc Declined",category="danger")
    return redirect('/admin/allPersonnels/')


# @app.route('/reason_decline_kyc/<int:kyc_id>',methods=["POST","GET"])
# # @login_req
# def reason_decline_kyc(kyc_id):
#     kyc = Kyc.query.get(kyc_id)
#     if request.method == "GET":
#         return render_template("admin/decline.html",kyc=kyc)
#     else:
#         reason = request.form.get('reason')
#         ad = session.get("Admin")
#         r = Kyc(kyc_reason=reason,kyc_per_id=ad)
#         db.session.add(r)
#         db.session.commit()
#         flash("reason submitted")
#         return redirect('/admin/allPersonnels/')



@app.route('/admin/toggle_access/<int:user_id>')
def toggle_access(user_id):
    personnel = Personnel.query.get(user_id)
    if personnel:
        personnel.per_restricted = not personnel.per_restricted
        db.session.commit()
        return jsonify({'message': 'Access toggled successfully'})
    return jsonify({'message': 'User not found'}), 404



# Very personnels
@app.route("/admin/verify/<int:id>/")
@login_req_admin
def verify(id):
    personnel = db.session.query(Personnel).get_or_404(id)
    kyc = db.session.query(Kyc).filter(Kyc.kyc_per_id==id).all()
    return render_template("admin/verify.html",personnel=personnel,kyc=kyc)


# allPersonnel route
@app.route("/admin/allPersonnels/")
@login_req_admin
def allPersonnels():
    personnel = db.session.query(Personnel).all()
    f = db.session.query(Kyc).all()
    return render_template("admin/allPersonnels.html",personnel=personnel,f=f)
# personnel ends here


# Delete user route
@app.route("/admin/delete_personnel/<int:id>/")
@login_req_admin
def delete_personnel(id):
    personnel = db.session.query(Personnel).get_or_404(id)
    db.session.delete(personnel)
    db.session.commit()
    flash("Profile deleted",category="info")
    return redirect("/admin/allPersonnels")


# Show personnel details
@app.route("/admin/personnel/<int:id>/")
@login_req_admin
def show_personnel(id):
    personnel = db.session.query(Personnel).get(id)
    apps = db.session.query(Appointment).filter(Appointment.app_per_id==id).all()
    spec = db.session.query(Specialization).filter(Specialization.spec_id==id).all()
    rev = db.session.query(Reviews).filter(Reviews.rev_per_id==id).all()
    # fin = db.session.query(Financial).filter(Financial.fin_id==id).all()
    kyc = db.session.query(Kyc).filter(Kyc.kyc_per_id==id).all()
    # fdbk = db.session.query(Feedback).get_or_404(id)
    return render_template("admin/personnel_details.html",kyc=kyc,rev=rev,apps=apps,spec=spec,personnel=personnel)


################################################################## ALL ABOUT  PERSONNELS ENDS HERE ###################################################################################


@app.route("/admin/show/")
@login_req_admin
def show_reviews():
    revs = db.session.query(Reviews).all()
    return render_template('user/index.html',revs=revs)


################################################################## ALL ABOUT PATIENTS STARTED HERE #################################################################################
# allpatients route
@app.route("/admin/allPatients/")
@login_req_admin
def allPatients():
    patients = db.session.query(Patient).all()
    return render_template("admin/allPatients.html",patients=patients)


# Delete user route
@app.route("/admin/delete/<int:id>/")
@login_req_admin
def delete_user(id):
    patients = db.session.query(Patient).get_or_404(id)
    db.session.delete(patients)
    db.session.commit()
    flash("Profile deleted")
    return redirect("/admin/allPatients")


# Show user details
@app.route("/admin/users/<int:id>/")
@login_req_admin
def show_user(id):
    patients = db.session.query(Patient).get_or_404(id)
    app = db.session.query(Appointment).filter(Appointment.app_pat_id==id).all()
    bill = db.session.query(Financial).filter(Financial.fin_pat_id==id).all()
    lab = db.session.query(Labtest).filter(Labtest.lab_pat_id==id).all()
    rev = db.session.query(Reviews).filter(Reviews.rev_pat_id==id).all()
    msg = db.session.query(Message).filter(Message.msg_pat_id==id).all()
    health = db.session.query(HealthRecord).filter(HealthRecord.health_pat_id==id).all()
    return render_template("/admin/userdeet.html",health=health,rev=rev,msg=msg,patients=patients,app=app,bill=bill,lab=lab)


# edit user /Updating 
@app.route("/admin/edit/<int:id>/", methods=["POST","GET"])
@login_req_admin
def edit_user(id):
    r = Patient()
    prof = db.session.query(Patient).get_or_404(id)
    if request.method == "GET":
        return render_template("userdash/profile.html",r=r,prof=prof)
    else:
        
        prof.patients_firstname = request.form.get('patients_firstname')
        prof.patients_lastname = request.form.get('patients_lastname')
        prof.patients_password = request.form.get('patients_password')
        prof.patients_email = request.form.get('patients_email')
        prof.patients_phn = request.form.get('patients_phn')
        prof.patients_kin = request.form.get('patients_kin')
        prof.patients_kinphn = request.form.get('patients_kinphn')
        db.session.commit()
        flash("Details successfully changed",category="success")
        return redirect("/admin/allPatients")
    
########################################################### ALL ABOUT PATIENTS ENDED HERE ###############################################################################################




# admin logout 
@app.route("/admin/logout/")
def admin_logout():
    if session.get("Admin") != None:
        session.pop("Admin",None)
    return redirect('/admin/login/')


# login validation
@app.route("/admin/")
def admin_home():
    if session.get("Admin") == None : #means he is not logged in
        flash("You must be logged in to view this page",category="error")
        return render_template("admin/login.html")
    else:
        return render_template("/admin/home.html")


# Admin login check
@app.route("/admin/login/",methods=["POST","GET"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/login.html")
    else:
        email= request.form.get("email")
        pwd = request.form.get("pwd")
        check = db.session.query(Admin).filter(Admin.admin_email==email).first()
        if check != None:
            if pwd == check.admin_password:
                session["Admin"]=email
                return redirect('/admin')
            else:
                flash("Invalid Login Details",category="error")
                return redirect('/admin/login')
        else:
            flash("Invalid Login Details",category="error")
            return redirect('/admin/login')



# @app.route("/admin/register/",methods=["POST","GET"])
# def admin_register():
#     if request.method == "GET":
#         return render_template("admin/register.html")
#     else:
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         email = request.form.get("email")
#         pwd = request.form.get("pwd")
#         query = Admin(admin_firstname=fname,admin_lastname=lname,admin_password=pwd,admin_email=email)
#         db.session.add(query)
#         db.session.commit()
#         flash("Account Created successfully. Please sign in",category="success")
#         return redirect(url_for('admin_home'))