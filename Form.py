from wtforms import Form, StringField, PasswordField,DateField, validators,IntegerField,FloatField,TextAreaField,FileField,SelectMultipleField,BooleanField,RadioField,EmailField, MonthField

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
    image = FileField('ImageURL', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    category = SelectMultipleField('Category', choices=[('men', 'Men'), ('women', 'Women'), ('kids', 'Kids'), ('shoe', 'Shoe'), ('others', 'Others')])
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    size = SelectMultipleField('Size', choices=[('XS', 'XS'),('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')])

class PromotionForm(Form):
    ID = StringField("ID",[validators.DataRequired()])
    name = StringField("Name")
    discount = FloatField("Discount", [validators.DataRequired()])
    description = TextAreaField("Description")

class PasswordChange(Form):
    CurrentPassword = PasswordField('CurrentPassword', [validators.DataRequired(), validators.length(min=8)])
    NewPassword = PasswordField('NewPassword', [validators.DataRequired(), validators.length(min=8), validators.equal_to('ConfirmPassword', message='Passwords Must Match.')])
    ConfirmPassword = PasswordField('ConfirmPassword', [validators.DataRequired(), validators.length(min=8)])

class ProductFilter(Form):
    category_men = BooleanField('Men')
    category_women = BooleanField('Women')
    category_kids = BooleanField('Kids')
    category_shoes = BooleanField('Shoes')
    category_others = BooleanField('Others')
    price_range = RadioField('Price Range', choices=[
        ('', 'All'),
        ('1-25', '1 - 25'),
        ('26-50', '26 - 50'),
        ('51-75', '51 - 75'),
        ('76-100', '76 - 100')
    ], default='')


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
