from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=4, max=50)])
    display_name = StringField('Отображаемое имя', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class QuizForm(FlaskForm):
    selected_option = RadioField('Выберите вариант ответа', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], validators=[DataRequired()])
    submit = SubmitField('Ответить')

class AddQuestionForm(FlaskForm):
    question_text = StringField('Текст вопроса', validators=[DataRequired()])
    option1 = StringField('Вариант 1', validators=[DataRequired()])
    option2 = StringField('Вариант 2', validators=[DataRequired()])
    option3 = StringField('Вариант 3', validators=[DataRequired()])
    option4 = StringField('Вариант 4', validators=[DataRequired()])
    correct_option = IntegerField('Номер правильного варианта (1-4)', validators=[DataRequired()])
    submit = SubmitField('Добавить вопрос')