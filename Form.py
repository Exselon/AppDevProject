from wtforms import Form, StringField, PasswordField,DateField, validators

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

#class test(Form):
