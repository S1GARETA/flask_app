from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db, User, Question
from forms import LoginForm, RegistrationForm, AddQuestionForm, QuizForm

from weather_api import get_weather_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'js8sn9s4mka72js0m7p2ap9s'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизируйтесь для доступа'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    session.pop('current_score', None)
    city = request.args.get('city', 'Moscow')
    weather_data = get_weather_data(city)
    return render_template("index.html", weather=weather_data)


@app.route('/quiz', methods=['GET'])
@login_required
def quiz():
    question = Question.query.order_by(db.func.random()).first()
    user_score = current_user.score
    current_score = session.get('current_score', 0)
    form = QuizForm()
    return render_template('quiz.html', question=question, user_score=user_score, form=form,
                           current_score=current_score)


@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    form = QuizForm()
    current_score = session.get('current_score', 0)

    if form.validate_on_submit():
        selected_option = form.selected_option.data
        question_id = request.form.get('question_id')
        question = Question.query.get(question_id)
        if question.correct_option == int(selected_option):
            current_score += 1
            flash('Правильно!', 'success')
        else:
            flash('Неправильный ответ!', 'error')

            if current_score > current_user.score:
                current_user.score = current_score
                flash('Ваши очки обновлены!', 'success')

            current_score = 0

        db.session.commit()
        session['current_score'] = current_score

    return redirect(url_for('quiz'))

@app.route("/leaderboard")
def leaderboard():
    session.pop('current_score', None)
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

@app.route("/login", methods=['GET', 'POST'])
def login():
    session.pop('current_score', None)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template("login.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    session.pop('current_score', None)
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        display_name = form.display_name.data
        password = form.password.data

        if User.query.filter_by(username=username).first() or User.query.filter_by(display_name=display_name).first():
            flash('Логин или имя уже заняты. Попробуйте другое.')
            return redirect(url_for('register'))

        new_user = User(username=username, display_name=display_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template("registration.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('login'))

@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    session.pop('current_score', None)
    form = AddQuestionForm()

    if form.validate_on_submit():
        new_question = Question(
            question_text=form.question_text.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )

        db.session.add(new_question)
        db.session.commit()
        flash('Вопрос успешно добавлен!', 'success')
        return redirect(url_for('add_question'))

    return render_template('add_question.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html")

if __name__ == "__main__":
    app.run(debug=True)