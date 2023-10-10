
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,SelectField,RadioField,BooleanField,SelectFieldBase,DateField,IntegerField,FileField
from wtforms.validators import Email,DataRequired,EqualTo,Length


class CreateAccount(FlaskForm):
    fname = StringField('First name',validators=[DataRequired(message="First name must not be empty")])
    lname = StringField('Last name',validators=[DataRequired(message="Last Name Cannot Be Empty")])
    phn = StringField('Phone Number',validators=[DataRequired(message="Phone Number Cannot Be Empty")])
    Dob = DateField("Date of birth")
    pwd = PasswordField("Password",validators=[DataRequired(message="Password Field Cannot be empty"),Length(min=8,message="Password muct be atleast 8 character long")])
    cpwd = PasswordField("Confirm Password",validators=[EqualTo("pwd",message="Confirm Password Does Not Match"),DataRequired(message="Cannot be empty")])
    email = StringField("Email",validators=[Email(message="invalid email"),DataRequired(message="Email Cannot be empty")])
    subbtn = SubmitField("Submit")
    insurance = IntegerField("Insurance Number",validators=[DataRequired(message="Insurance Number must be supplied")])
    photo = FileField("Profile Picture")
    gender = RadioField("Gender",choices=[("Male","Male"),("Female","Female")])
    address = StringField('Home Address',validators=[DataRequired(message="Home address must be inputed")])
    mStatus = RadioField("Marital Status",choices=[("Single","Single"),("Married","Married"),("Divorced","Divorced")])


# Personnel form
class PersonnelAccount(FlaskForm):
    fname = StringField('First name',validators=[DataRequired(message="First name must not be empty")])
    lname = StringField('Last name',validators=[DataRequired(message="Last Name Cannot Be Empty")])
    phn = StringField('Phone Number',validators=[DataRequired(message="Phone Number Cannot Be Empty")])
    Dob = DateField("Date of birth")
    pwd = PasswordField("Password",validators=[DataRequired(message="Password Field Cannot be empty")])
    cpwd = PasswordField("Confirm Password",validators=[EqualTo("pwd",message="Confirm Password Does Not Match"),DataRequired(message="Cannot be empty")])
    email = StringField("Email",validators=[Email(message="invalid email"),DataRequired(message="Email Cannot be empty")])
    subbtn = SubmitField("Submit")
    license = IntegerField("Medical license Number",validators=[DataRequired(message="Liscenced number must be supplied")])
    acc_num = IntegerField("Demo Account Number ** (for demo purpose)",validators=[DataRequired(message="Account number must be supplied")])
    photo = FileField("Profile Picture")
    gender = RadioField("Gender",choices=[("Male","Male"),("Female","Female")])
    address = StringField('Home Address',validators=[DataRequired(message="Home address must be inputed")])
    mStatus = RadioField("Marital status",choices=[("Single","Single"),("Married","Married"),("Divorced","Divorced")])



class PaymentForm(FlaskForm):
    fullname = StringField("Fullname",validators=[DataRequired(message="FirstName is too short")])
    email = StringField("Email",validators=[Email(message="Invalid Email"), DataRequired(message="Email must be supplied")])
    amount = StringField("Amount",validators=[ DataRequired(message="amount must be supplied")])
    btnsubmit = SubmitField("Continue!")



# class SubscribeForm(FlaskForm):
#     email = StringField('Email', validators=[Email(message='Enter a valid email address.'),DataRequired()])



class Pwd(FlaskForm):

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    alpha = StringField("How many letters would you like in your password?",validators=[Email(message="invalid email"),DataRequired(message="Emmail Cannot be empty")])
    symbol = StringField("How many symbols would you like?",validators=[DataRequired(message="Password Field Cannot be empty")])
    numbers = StringField("How many numbers would you like?",validators=[DataRequired(message="Password Field Cannot be empty")])
