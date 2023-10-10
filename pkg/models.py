from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



class State(db.Model):
    state_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name=db.Column(db.String(20),nullable=False)
    
    # set relationship: using backref means that you dont have to to set relationship on second table(lga)
    lgas = db.relationship("Lga",backref='state_deets')
    state = db.relationship("Personnel",back_populates='per_state')
    

class Lga(db.Model):
    lga_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    lga_name=db.Column(db.String(20),nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)
     


# Financial Transactions
class Financial(db.Model):
    __tablename__="Financial"
    fin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    fin_status = db.Column(db.Enum ('pending','approved','declined'),nullable=False, server_default=("pending"))
    app_date_time = db.Column(db.DateTime(), default=datetime.utcnow)
    fin_amount = db.Column(db.Integer(), nullable=False)
    payment_invoice = db.Column(db.String(250), nullable=False)
    paygate_response = db.Column(db.Text())
    fin_fullname=db.Column(db.String(100),nullable=True)
    fin_email=db.Column(db.String(100),nullable=True)
    fin_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False)
    fin_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    
    # Relationship
    fin_deets = db.relationship("Patient",back_populates='pat_fins')
    fins = db.relationship("Personnel",back_populates='per_fins')

# Health records
class HealthRecord(db.Model):
    __tablename__="HealthRecords"
    health_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    medical_history = db.Column(db.Text())
    allergies = db.Column(db.Text())
    Medications = db.Column(db.Text())
    health_date_time = db.Column(db.DateTime(), default=datetime.utcnow)
    health_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False)
    health_lab_id = db.Column(db.Integer, db.ForeignKey('Labtest.lab_id'))
    health_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'))
    # re
    health_deets = db.relationship("Patient",back_populates='pat_health')



# Labtest
class Labtest(db.Model):
    __tablename__="Labtest"
    lab_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    lab_result = db.Column(db.String(250), nullable=False)
    lab_test = db.Column(db.String(250) )
    lab_order = db.Column(db.String(250))
    lab_date_time = db.Column(db.DateTime(), default=datetime.utcnow)
    lab_app_id = db.Column(db.Integer, db.ForeignKey('Appointment.app_id'))
    lab_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False) 

    labtest_deets = db.relationship("Patient",back_populates='pat_lab')


# Appointment
class Appointment(db.Model):
    __tablename__="Appointment"
    app_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    app_status = db.Column(db.Enum ('pending','approved','declined'),nullable=False, server_default=("pending"))
    app_date = db.Column(db.Date(), default=datetime.utcnow)
    app_time = db.Column(db.Time(),default=datetime.utcnow )
    app_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False)
    app_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)

    # RELATIONAHIP
    # app_fins = db.relationship("Financial",back_populates='fin_app')
    app_feed = db.relationship("Feedback",back_populates='feed_apps')
    app_deets = db.relationship("Patient",back_populates='pat_apps')
    app = db.relationship("Personnel",back_populates='per_apps')



# Specialization
class Specialization(db.Model):
    __tablename__="Specialization"
    spec_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    spec_name = db.Column(db.String(200), nullable=False)
    
    # Relationship
    spec = db.relationship("Personnel",back_populates='per_spec')


# KYC
class Kyc(db.Model):
    __tablename__="Kyc"
    kyc_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    kyc_pix = db.Column(db.String(200), nullable=False)
    kyc_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    kyc_reason = db.Column(db.Text() )
    kyc_date =db.Column(db.DateTime(), default=datetime.utcnow)
    kyc_status = db.Column(db.Enum ('pending','approved','declined'),nullable=False, server_default=("pending"))
    # Relationship
    kyc = db.relationship("Personnel",back_populates='per_kyc')

    

# Reviews
class Reviews(db.Model):
    __tablename__="Reviews"
    rev_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    rev_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False)
    message = db.Column(db.Text() )
    rev_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    rev_date =db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    rev_deets = db.relationship("Patient",back_populates='pat_rev')
    rev = db.relationship("Personnel",back_populates='per_rev')

# Notification Table
class Notification(db.Model):
    __tablename__="Notification"
    __table_args__ = {'extend_existing': True}
    not_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    not_messages = db.Column(db.Text() )
    not_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False) 
    not_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    not_date =db.Column(db.DateTime(), default=datetime.utcnow)  

    not_deets = db.relationship("Patient",back_populates='pat_not')
    nots = db.relationship("Personnel",back_populates='per_not')

# Feedback Table
class Feedback(db.Model):
    __tablename__="Feedback"
    feed_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    feed_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False) 
    feed_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    feed_app_id = db.Column(db.Integer, db.ForeignKey('Appointment.app_id'),nullable=False)
    feed_message = db.Column(db.Text() )
    feed_date =db.Column(db.DateTime(), default=datetime.utcnow)

    feed_apps = db.relationship("Appointment",back_populates='app_feed')
    feed_deets = db.relationship("Patient",back_populates='pat_feed') 
    feed = db.relationship("Personnel",back_populates='per_feed')

class Message(db.Model):
    __tablename__="Message"
    msg_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    msg_pat_id = db.Column(db.Integer, db.ForeignKey('Patient.pat_id'),nullable=False) 
    msg_per_id = db.Column(db.Integer, db.ForeignKey('Personnel.per_id'),nullable=False)
    messages = db.Column(db.Text() )
    msg_date =db.Column(db.DateTime(), default=datetime.utcnow)

    msg_deets = db.relationship("Patient",back_populates='pat_msg')
    msg = db.relationship("Personnel",back_populates='per_msg')

# Table for personnel
class Personnel(db.Model):
    __tablename__="Personnel"
    per_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    per_firstname = db.Column(db.String(50), nullable=False)
    per_lastname = db.Column(db.String(45), nullable=False)
    per_password = db.Column(db.String(200), nullable=False)
    per_email = db.Column(db.String(45), nullable=False,unique=True)
    per_phn = db.Column(db.String(45), nullable=False)
    per_dob = db.Column(db.Date(), nullable=False)
    liscence_number = db.Column(db.Integer(), nullable=False)
    acc_num = db.Column(db.Integer(), nullable=False)
    per_address = db.Column(db.String(70), nullable=False)
    per_gender = db.Column(db.String(70), nullable=False)
    per_state = db.Column(db.String(45), nullable=False)
    per_mStatus = db.Column(db.String(45), nullable=False)
    per_lga = db.Column(db.String(45), nullable=False)
    per_status =db.Column(db.Enum('1','0'),nullable=False, server_default=("0"))
    per_profile_picture = db.Column(db.String(100), nullable=False)
    datereg = db.Column(db.DateTime(), default=datetime.utcnow)
    per_restricted = db.Column(db.Boolean, default=False)

    # Foriegn keys
    per_spec_id = db.Column(db.Integer, db.ForeignKey('Specialization.spec_id'),nullable=False)
    per_state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)
    per_bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'),nullable=False)
    
    

    # Relationships
    per_kyc = db.relationship("Kyc",back_populates='kyc', cascade="all, delete-orphan")
    per_apps = db.relationship("Appointment",back_populates='app')
    per_fins = db.relationship("Financial",back_populates='fins')
    per_spec = db.relationship("Specialization",back_populates='spec')
    per_rev = db.relationship("Reviews",back_populates='rev')
    per_not = db.relationship("Notification",back_populates='nots') 
    per_feed = db.relationship("Feedback",back_populates='feed')
    per_msg = db.relationship("Message",back_populates='msg')
    per_state = db.relationship("State",back_populates='state')
    per_bank = db.relationship("Bank",back_populates='bnk')

# Table for patients
class Patient(db.Model):
    __tablename__="Patient"
    pat_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pat_firstname = db.Column(db.String(50), nullable=False)
    pat_lastname = db.Column(db.String(45), nullable=False)
    pat_password = db.Column(db.String(200), nullable=False)
    pat_email = db.Column(db.String(45), nullable=False,unique=True)
    pat_phn = db.Column(db.String(45), nullable=False)
    pat_dob = db.Column(db.Date(), nullable=False)
    pat_gender = db.Column(db.String(45), nullable=False)
    pat_mStatus = db.Column(db.String(45), nullable=False)
    insurance_number = db.Column(db.Integer(), nullable=False)
    profile_picture = db.Column(db.String(100))
    pat_address = db.Column(db.String(70), nullable=False)
    datereg = db.Column(db.DateTime(), default=datetime.utcnow)
    pat_restricted = db.Column(db.Boolean, default=False)

    # relationshipa
    pat_fins = db.relationship("Financial",back_populates='fin_deets', cascade="all, delete-orphan")
    pat_apps = db.relationship("Appointment",back_populates='app_deets', cascade="all, delete-orphan")
    pat_health = db.relationship("HealthRecord",back_populates='health_deets', cascade="all, delete-orphan")
    pat_lab = db.relationship("Labtest",back_populates='labtest_deets', cascade="all, delete-orphan")
    pat_rev = db.relationship("Reviews",back_populates='rev_deets', cascade="all, delete-orphan")
    pat_not = db.relationship("Notification",back_populates='not_deets', cascade="all, delete-orphan")
    pat_feed = db.relationship("Feedback",back_populates='feed_deets', cascade="all, delete-orphan") 
    pat_msg = db.relationship("Message",back_populates='msg_deets', cascade="all, delete-orphan")



class Admin(db.Model):
    __tablename__="admin"
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_firstname = db.Column(db.String(50), nullable=False)
    admin_lastname = db.Column(db.String(45), nullable=False)
    admin_password = db.Column(db.String(200), nullable=False)
    admin_email = db.Column(db.String(45), nullable=False)

    
class Subscription(db.Model):
    __tablename__="Subscription"
    subs_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sub_email = db.Column(db.String(50), nullable=False)

    

class Bank(db.Model):
    __tablename__="banks"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    code = db.Column(db.String(5), nullable=False)

    bnk = db.relationship("Personnel",back_populates='per_bank')