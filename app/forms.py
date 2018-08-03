from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RomanConsularDating(FlaskForm):
    consulship = StringField('Consulship:', validators=[DataRequired()])
    day_ref = SelectField('Kalends/Nones/Ides:', choices=[('Kalends','Kalends'),('Nones','Nones'),('Ides','Ides')])
    months = SelectField('Month:', choices=[('January','January'),('February','February'),('March','March'),('April','April'),('May','May'),('June','June'),('July','July'),('August','August'),('September','September'),('October','October'),('November','November'),('December','December')])
    day_number = SelectField('Day:', choices=[
        (1,''),
        (2,'a.d. II (pridie)'),
        (3,'a.d. III'),
        (4,'a.d. IV'),
        (5,'a.d. V'),
        (6,'a.d. VI'),
        (7,'a.d. VII'),
        (8,'a.d. VIII'),
        (9,'a.d. IX'),
        (10,'a.d. X'),
        (11,'a.d. XI'),
        (12,'a.d. XII'),
        (13,'a.d. XIII'),
        (14,'a.d. XIV'),
        (15,'a.d. XV'),
        (16,'a.d. XVI'),
        (17,'a.d. XVII'),
        (18,'a.d. XVIII'),
        (19,'a.d. XIX')
    ])
    reset = SubmitField('Reset...')
    submit = SubmitField('Convert...')