from wtforms import Form, SubmitField, StringField, PasswordField,DateField, validators,IntegerField,SelectField,FloatField,TextAreaField,FileField,SelectMultipleField,BooleanField,RadioField,EmailField, MonthField
from wtforms.validators import DataRequired, Email, Length, Optional
class userSignup(Form):
    name = StringField('name', [validators.Length(min=1, max=150)])
    password = PasswordField('Password', [validators.Length(min=8)])
    cfmpassword = PasswordField('cfmPassword', [validators.Length(min=8)])
    number = IntegerField('Contact Number', [validators.Length(min=8, max=8)])
    email = EmailField('Email', [validators.Email()])
    dob = DateField('Date of Birth',  format='%Y-%m-%d')

class userLogin(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

class ProductForm(Form):
    image = FileField('ImageURL')
    name = StringField('Name')
    price = FloatField('Price')
    category = SelectMultipleField('Category', choices=[('men', 'Men'), ('woman', 'Women'), ('kids', 'Kids'), ('others', 'Others')])
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    size = SelectMultipleField('Size', choices=[('Freesize', 'Free size'),('XS', 'XS'),('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')])

class PromotionForm(Form):
    ID = StringField("ID")
    name = StringField("Name")
    discount = StringField("Discount")
    description = TextAreaField("Description")

class PasswordChange(Form):
    CurrentPasswordField = PasswordField('CurrentPassword', [validators.DataRequired(), validators.length(min=8)])
    NewPasswordField = PasswordField('NewPassword', [validators.DataRequired(), validators.length(min=8), validators.equal_to('ConfirmPassword', message='Passwords Must Match.')])
    ConfirmPasswordField = PasswordField('ConfirmPassword', [validators.DataRequired(), validators.length(min=8)])

class ForgetPasswordEmail(Form):
    Email = EmailField('Email', [validators.Email()])

class ProductFilter(Form):
    category_men = BooleanField('Men')
    category_woman = BooleanField('Women')
    category_kids = BooleanField('Kids')
    category_others = BooleanField('Others')
    pricerange = RadioField('Price', choices=[
        ('1-10', '$1 ~ $10'),
        ('11-20', '$11 ~ $20'),
        ('21-30', '$21 ~ $30'),
        ('31-40', '$31 ~ $40'),
        ('41-999', '$41++')
    ])

class CheckoutForm(Form):
    fname = StringField('firstname', [validators.DataRequired()])
    lname = StringField('lastname', [validators.DataRequired()])
    address = StringField('address', [validators.DataRequired()])
    email = EmailField(validators.DataRequired("Please enter your email address"), [validators.Email("Please enter your email address")])
    postalcode = IntegerField('postalcode', [validators.DataRequired(), validators.length(min=6, max=6)])
    unitno = StringField('unitno', [validators.Optional(strip_whitespace=True)])
    submit = SubmitField('Pay Now')
    # nameoncard = StringField('nameoncard', [validators.InputRequired(), validators.DataRequired()])
    # cardno = IntegerField('cardno', [validators.InputRequired(), validators.DataRequired(), validators.length(min=16, max=16)])
    # expirydate = MonthField('expirydate', [validators.InputRequired(), validators.DataRequired()], format='%m - %y')
    # cvv = IntegerField('cvv', [validators.InputRequired(), validators.DataRequired, validators.length(min=3, max=4)])



class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150)])
    email = EmailField('Email', [validators.Email()])
    enquiry = TextAreaField('Enquiry ')
    subject_choices = [('general', 'General Inquiry'),
                       ('support', 'Technical Support'),
                       ('sales', 'Sales Inquiry'),
                        ('others', 'Others')]
    subject = SelectField('Subject', choices=subject_choices)




