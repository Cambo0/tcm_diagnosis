from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('请使用不同的用户名。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('请使用不同的邮箱地址。')

class AddHerbForm(FlaskForm):
    name = StringField('中药名称', validators=[DataRequired()])
    submit = SubmitField('添加')

class AddDiseaseForm(FlaskForm):
    name = StringField('疾病名称', validators=[DataRequired()])
    submit = SubmitField('添加')

class AddAssociationForm(FlaskForm):
    herb = StringField('中药名称', validators=[DataRequired()])
    disease = StringField('疾病名称', validators=[DataRequired()])
    submit = SubmitField('添加关联')

class BulkAddHerbForm(FlaskForm):
    herbs = TextAreaField('中药名称（每行一个）', validators=[DataRequired()])
    submit = SubmitField('批量添加')

class BulkAddDiseaseForm(FlaskForm):
    diseases = TextAreaField('疾病名称（每行一个）', validators=[DataRequired()])
    submit = SubmitField('批量添加')

class BulkAddAssociationForm(FlaskForm):
    herb = StringField('中药名称', validators=[DataRequired()])
    diseases = TextAreaField('疾病列表（每行一个）', validators=[DataRequired()])
    submit = SubmitField('批量添加关联')