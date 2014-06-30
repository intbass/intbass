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
    username = TextField('Name:', validators = [Required()])
    password = PasswordField('Password:', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class UserEditForm(Form):
    username = TextField('username ', validators = [Required()])
    email = TextField('emailjapan', validators = [Required()])
    location = TextField('Location', validators = [Required()])
    password = PasswordField('Password')
    role = SelectField('Role', validators = [Required()],
            choices=[('0', 'disabled'),
            ('1', 'user'),
            ('2', 'dj'),
            ('11', 'admin')])

class FileForm(Form):
    title = TextField('title', validators=[Required()])
    artist = TextField('artist', validators=[Required()])
    album = TextField('album', validators=[Required()])
    date_recorded = TextField('date_recorded')


