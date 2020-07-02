from wtforms import Form, StringField, TextAreaField, PasswordField, validators


# user registration form class
class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('User name', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm password')


# user articles form class
class ArticlesForm(Form):
    title = StringField('Title', [validators.length(min=2, max=200)])
    body = TextAreaField('Body', [validators.length(min=20)])

