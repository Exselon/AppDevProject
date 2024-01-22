from wtforms import Form, StringField, PasswordField,DateField, validators,IntegerField,FloatField,TextAreaField,SelectField,FileField,SelectMultipleField

class userSignup(Form):
    name = StringField('name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8), validators.DataRequired()])
    cfmpassword = PasswordField('cfmPassword', [validators.Length(min=8), validators.DataRequired()])
    number = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    dob = DateField('Date of Birth', [validators.DataRequired()], format='%Y-%m-%d')

class userLogin(Form):                                                                                           message='Enter a valid contact number.')]
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