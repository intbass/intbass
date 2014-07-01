from flask_wtf.form import Form
from wtforms import TextField, RadioField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import Required
 
#class IPForm(Form):
#    subnet = TextField("Subnet", validators = [Required()])
#    action = RadioField("Action", choices=[('bgp', 'BGP'), ('dns', 'DNS Query'), ('blackhole', 'Blackhole IP')])
#    #email = TextField("Email")
#    #subject = TextField("Subject")
#    #message = TextAreaField("Message")
#
#    submit = SubmitField("Send")

class LoginForm(Form):
    username = TextField('Name:', validators=[Required()])
    password = PasswordField('Password:', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class UserEditForm(Form):
    name = TextField('name ', validators=[Required()])
    email = TextField('email', validators=[Required()])
    location = TextField('location', validators=[Required()])
    password = PasswordField('password')

class FileForm(Form):
    title = TextField('title', validators=[Required()])
    artist = TextField('artist', validators=[Required()])
    album = TextField('album', validators=[Required()])
    date_recorded = TextField('date_recorded')


