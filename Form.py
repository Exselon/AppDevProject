from wtforms import Form, StringField, PasswordField,DateField, validators,IntegerField,FloatField,TextAreaField,SelectField,FileField

class userSignup(Form):
    name = StringField('name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8), validators.DataRequired()])
    cfmpassword = PasswordField('cfmPassword', [validators.Length(min=8), validators.DataRequired()])
    number = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    dob = DateField('Date of Birth', [validators.DataRequired()], format='%Y-%m-%d')

class userLogin(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

class ProductForm(Form):
    image = FileField('ImageURL', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    category = StringField('Category', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    size = SelectField('Size', choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])

class PromotionForm(Form):
    ID = StringField("ID",[validators.DataRequired()])
    name = StringField("Name", [validators.DataRequired()])
    discount = FloatField("Discount", [validators.DataRequired()])
    description = TextAreaField("Description", [validators.DataRequired()])