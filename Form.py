from wtforms import Form, StringField, PasswordField,DateField, validators,IntegerField,FloatField,TextAreaField,SelectField,FileField,SelectMultipleField,EmailField, MonthField

class userSignup(Form):
    name = StringField('name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8), validators.DataRequired()])
    cfmpassword = PasswordField('cfmPassword', [validators.Length(min=8), validators.DataRequired()])
    number = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    dob = DateField('Date of Birth', [validators.DataRequired()], format='%Y-%m-%d')

class userLogin(Form):
    message=[('Enter a valid contact number.')]
    username = StringField('username', [validators.DataRequired()], render_kw={'placeholder': 'Contact No'})
    password = PasswordField('password', [validators.DataRequired()], render_kw={'placeholder': 'Password'})

class ProductForm(Form):
    image = FileField('ImageURL', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    category = SelectMultipleField('Category', choices=[('shoe', 'Shoe'), ('shirt', 'Shirt'), ('pants', 'Pants')])

    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    size = SelectField('Size', choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])

class PromotionForm(Form):
    ID = StringField("ID",[validators.DataRequired()])
    name = StringField("Name", [validators.DataRequired()])
    discount = FloatField("Discount", [validators.DataRequired()])
    description = TextAreaField("Description", [validators.DataRequired()])

class PasswordChange(Form):
    CurrentPassword = PasswordField('CurrentPassword', [validators.DataRequired(), validators.length(min=8)])
    NewPassword = PasswordField('NewPassword', [validators.DataRequired(), validators.length(min=8), validators.equal_to('ConfirmPassword', message='Passwords Must Match.')])
    ConfirmPassword = PasswordField('ConfirmPassword', [validators.DataRequired(), validators.length(min=8)])


class Checkout(Form):
    firstname = StringField('firstname', [validators.InputRequired(), validators.DataRequired()])
    lastname = StringField('lastname', [validators.InputRequired(), validators.DataRequired()])
    address = StringField('address', [validators.InputRequired(), validators.DataRequired()])
    email = EmailField('email', [validators.InputRequired("Please enter your email address"), validators.DataRequired(), validators.Email("Please enter your email address")])
    postalcode = IntegerField('postalcode', [validators.InputRequired(), validators.DataRequired(), validators.length(min=6, max=6)])
    nameoncard = StringField('nameoncard', [validators.InputRequired(), validators.DataRequired()])
    cardno = IntegerField('cardno', [validators.InputRequired(), validators.DataRequired(), validators.length(min=16, max=16)])
    expirydate = MonthField('expirydate', [validators.InputRequired(), validators.DataRequired()], format='%m - %y')
    cvv = IntegerField('cvv', [validators.InputRequired(), validators.DataRequired, validators.length(min=3, max=4)])
    unitno = StringField('unitno', [validators.Optional(strip_whitespace=True)])
