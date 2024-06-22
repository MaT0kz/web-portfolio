import datetime
import os

import werkzeug.utils
from flask import Flask, redirect, url_for, request, flash
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from data import db_session
from data.db_session import SqlAlchemyBase
from data.users import User
from data.projects import Project
from data.vacancies import Vacancy, Resume
from forms.user import RegisterForm, LoginForm, ProjectAddForm, ProfileForm, ProjectForm, ScrollForm, OrganisationProfileForm, VacancyForm
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session

app = Flask(__name__)
UPLOAD_FOLDER = r"C:/Users/user/Desktop/Второе полугодие/Web portfolio 2 semester/static"
app.config["SECRET_KEY"] = "Secret key 14949821412"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def db_add_item(dbSession: Session, element: SqlAlchemyBase) -> None:
    dbSession.add(element)
    dbSession.commit()


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
Функции для взаимодействия с аккаунтами
'''
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(1)
        session = db_session.create_session()
        if form.password.data != form.password_again.data:
            print(2)
            # Предупреждение о том, что пароли разные
            return render_template("registration.html", form=form)
        if session.query(User).filter(User.email == form.email.data).first():
            print(3)
            return render_template('registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.role.data == 'Разработчик':
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                created_date=datetime.datetime.now(),
                sphere=form.sphere.data,
                role="person",
                nickname=form.nickname.data,
                unique_id=form.email.data
            )
        elif form.role.data == 'Организация':
            user = User(
                name=form.name.data,
                email=form.email.data,
                created_date=datetime.datetime.now(),
                sphere=form.sphere.data,
                role="organisation",
                nickname=form.nickname.data,
                unique_id=form.email.data
            )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        print(4)
        return redirect(url_for("login"))
    print(5)
    return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    sess = db_session.create_session()
    return sess.query(User).get(user_id)


'''
Функции представления страниц 
'''
@app.route('/profile/<string:unique_user_id>', methods=["GET", "POST"])
def profile(unique_user_id: str):
    session = db_session.create_session()
    user = session.query(User).filter(User.unique_id == unique_user_id).first()

    project_list = session.query(Project).filter(Project.user_id == unique_user_id)
    if user.role == "person":
        resum = session.query(Resume).filter(Resume.account_id == user.unique_id).all()
        if current_user.is_authenticated and current_user == user:
            upload_form = ProfileForm()
            return render_template("personprofile.html", project_list=project_list, user=user, form=upload_form, resumies=resum)
        return render_template("personprofile.html", project_list=project_list, user=user, resumies=resum)
    elif user.role == "organisation":
        vacancies = session.query(Vacancy).filter(Vacancy.account_id == user.unique_id).all()
        if current_user.is_authenticated and current_user.unique_id == unique_user_id:
            form = OrganisationProfileForm()
            if form.validate_on_submit():
                return redirect('update_profile')
            return render_template("organisationprofile.html", organisation=user, form=form, vacancies=vacancies)
        return render_template("organisationprofile.html", organisation=user, vacancies=vacancies)


@app.route('/add_vacancy/profile/<string:unique_id>', methods=["GET", "POST"])
@login_required
def add_vacancy_profile(unique_id : str):
    sess = db_session.create_session()
    form = VacancyForm()
    if form.validate_on_submit():
        print(1)
        if current_user.role == "organisation":
            vacance = Vacancy(
                name=form.name.data,
                created_date=datetime.datetime.now(),
                sphere=form.sphere.data,
                experience=form.experience.data,
                about=form.about.data,
                requirements=form.requirements.data,
                account_id=unique_id,
            )
        elif current_user.role == "person":
            vacance = Resume(
                name=form.name.data,
                created_date=datetime.datetime.now(),
                sphere=form.sphere.data,
                experience=form.experience.data,
                about=form.about.data,
                requirements=form.requirements.data,
                account_id=unique_id,
            )
        sess.add(vacance)
        sess.commit()
        print(2)
        return redirect(url_for('profile', unique_user_id=unique_id))
    return render_template("vacancycreating.html", form=form)


@app.route('/vacancy/<string:id>', methods=["GET", "POST"])
def vacancy(id : str):
    sess = db_session.create_session()
    vacance = sess.query(Vacancy).filter(Vacancy.id == id).first()
    user = sess.query(User).filter(User.unique_id == vacance.account_id).first()
    if current_user.is_authenticated and current_user == user:
        form = VacancyForm()
        return render_template("vacancy.html", vacancy=vacance, form=form, user=user)
    return render_template("vacancy.html", vacancy=vacance, user=user)


@app.route('/vacancies/<string:unique_user_id>', methods=["GET", "POST"])
def vacancies(unique_user_id : str):
    sess = db_session.create_session()
    vacan = sess.query(Vacancy).filter(Vacancy.account_id == unique_user_id).all()
    user = sess.query(User).filter(User.unique_id == unique_user_id).first()
    return render_template("vacancies.html", vacancies=vacan, user=user)


@app.route('/resume/<string:id>', methods=["GET", "POST"])
def resume(id : str):
    sess = db_session.create_session()
    vacance = sess.query(Resume).filter(Resume.id == id).first()
    user = sess.query(User).filter(User.unique_id == vacance.account_id).first()
    if current_user.is_authenticated and current_user == user:
        form = VacancyForm()
        return render_template("vacancy.html", vacancy=vacance, form=form, user=user)
    return render_template("vacancy.html", vacancy=vacance, user=user)


@app.route('/resumies/<string:unique_user_id>', methods=["GET", "POST"])
def resumies(unique_user_id : str):
    sess = db_session.create_session()
    vacan = sess.query(Resume).filter(Resume.account_id == unique_user_id).all()
    user = sess.query(User).filter(User.unique_id == unique_user_id).first()
    return render_template("vacancies.html", vacancies=vacan, user=user)


@app.route('/<string:unique_user_id>/<string:project_id>', methods=["GET", "POST"])
def project(unique_user_id: str, project_id: str):
    session = db_session.create_session()
    project = session.query(Project).filter(Project.id == project_id).first()
    user = session.query(User).filter(User.unique_id == unique_user_id).first()
    form = ProjectForm()

    return render_template("project.html", project=project, user=user, form=form)


@app.route('/add_project/<string:unique_user_id>', methods=["GET", "POST"])
@login_required
def profile_add_project(unique_user_id: str):
    project_form = ProjectAddForm()
    if project_form.validate_on_submit():
        if current_user.unique_id == unique_user_id:
            sess = db_session.create_session()
            files = ''
            cover = ''
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    files = ''
                    cover = ''
            project = Project(
                name=project_form.name.data,
                sphere=project_form.sphere.data,
                about=project_form.about.data,
                user_id=unique_user_id,
                files=files,
                cover=cover
            )
            sess.add(project)
            sess.commit()
            return redirect(url_for('profile', unique_user_id=current_user.unique_id))
    return render_template("projectcreating.html", project=project_form, unique_user_id=unique_user_id)


@app.route('/', methods=["GET", "POST"])
def main_page_portfolio():
    '''Отображает главную страницу вне зависимости зарегестрирован пользоватль или нет'''
    sess = db_session.create_session()
    most_visited_profiles = sess.query(User).filter().all()
    return render_template("index.html", profiles=most_visited_profiles)


user_transform = {"person": "organisation", "organisation": "person"}


@app.route('/gallery', methods=["GET", "POST"])
def scroll():
    form = ScrollForm()
    sess = db_session.create_session()
    most_visited_profiles = sess.query(User).filter().all()
    if form.is_submitted() and form.search.data:
        most_visited_profiles = sess.query(User).filter(User.name == form.search.data).all()
    if current_user.is_authenticated:
        if current_user.role == "person":
            most_visited_profiles = sess.query(Vacancy).all()
            if any((form.search.data, form.experience.data, form.sphere.data)):
                most_visited_profiles = sess.query(Vacancy).filter(and_(Vacancy.name.like(f"%{form.search.data}%"), Vacancy.experience.like(f"%{form.experience.data}%"), Vacancy.sphere.like(f"%{form.sphere.data}%"))).all()
                # if any((form.expirience.data, form.sphere.data)):
                #     most_visited_profiles = sess.query(Vacancy).filter(Vacancy.account_type == "organisation")\
                #         .filter(or_(Vacancy.sphere.like(form.sphere.data), Vacancy.about.like(form.expirience.data)))
        elif current_user.role == "organisation":
            most_visited_profiles = sess.query(Resume).all()
            if any((form.search.data, form.experience.data, form.sphere.data)):
                most_visited_profiles = sess.query(Resume).filter(and_(Resume.name.like(f"%{form.search.data}%"), Resume.experience.like(f"%{form.experience.data}%"), Resume.sphere.like(f"%{form.sphere.data}%"))).all()
                # if any((form.expirience.data, form.sphere.data)):
                #     most_visited_profiles = sess.query(Vacancy).filter(and_(Vacancy.account_type == "person", Vacancy.about.ilike(f"%{form.expirience.data}%")))
    print(most_visited_profiles )
    return render_template("scroll.html", form=form, profiles=most_visited_profiles)


@app.route('/<string:unique_user_id>/<string:project_id>/delete_project', methods=["GET", "POST"])
@login_required
def delete_project(unique_user_id: str, project_id: str):
    session = db_session.create_session()
    session.query(Project).filter(Project.user_id == unique_user_id and Project.id == project_id).delete()
    session.commit()
    return redirect(url_for('profile', unique_user_id=unique_user_id))


def save_the_file(filename: str, user: str, repeat: bool = False) -> tuple[str, str]:
    extencion: str = filename.split('.')[-1]
    file_dir: str = '/icons' + f'/{user[0]}' + f'/{user[1]}/'
    if not repeat:
        name: str = f'{user}' + '.' + extencion
    else:
        sign = user.split('.')[0]
        name: str = sign + sign[-1] + '.' + extencion
    return file_dir, name


def create_the_dir(static_folder: str, filedir: str, filename: str) -> None | str:
    if not os.path.isdir(static_folder + filedir):
        os.makedirs(static_folder + filedir)
        return filename
    if os.path.exists(os.path.join(static_folder + filedir, filename)):
        name = filename.split('.')
        return name[0] + name[0][-1] + "." + name[1]
    return filename


def delete_useless_file_and_dirs(path_to_file: str) -> None:
    try:
        os.remove(path_to_file)
    finally:
        return


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        print(1)
        if any(elem[1] for elem in request.form.items() if elem[0] not in ('csrf_token', 'submit')):
            sess = db_session.create_session()
            user = sess.query(User).filter(User.unique_id == current_user.unique_id).first()
            for elem in request.form.items():
                if elem[0] not in ('csrf_token', 'submit') and elem[1]:
                    print(elem)
                    exec(f'user.{elem[0]} = "{elem[1]}"')
            sess.commit()
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('profile', unique_user_id=current_user.unique_id))
        if file and allowed_file(file.filename):
            if not current_user.avatar_path:
                avatar_path = save_the_file(file.filename, current_user.unique_id)
            else:
                delete_useless_file_and_dirs(UPLOAD_FOLDER + current_user.avatar_path)
                avatar_path = save_the_file(file.filename, current_user.avatar_path.split('/')[-1], repeat=True)

            sess = db_session.create_session()
            user = sess.query(User).filter(User.unique_id == current_user.unique_id).first()
            new_filename = create_the_dir(UPLOAD_FOLDER, avatar_path[0], avatar_path[1])

            user.avatar_path = ''.join((avatar_path[0], new_filename))
            sess.commit()

            file.save(os.path.join(UPLOAD_FOLDER + ''.join((avatar_path[0], new_filename))))
    return redirect(url_for('profile', unique_user_id=current_user.unique_id))

# @app.route('/upload_avatar', methods=['GET', 'POST'])
# @login_required
# def upload_avatar():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(current_user.unique_id)
#         if file and allowed_file(file.filename):
#             avatar_path = save_the_file(file.filename, current_user.unique_user_id)
#
#             sess = db_session.create_session()
#             user = sess.query(User).filter(User.unique_id == current_user.unique_id).first()
#             user.avatar_path = avatar_path
#             sess.commit()
#
#             file.save(UPLOAD_FOLDER + avatar_path)
#     return redirect(url_for('profile', unique_user_id=current_user.unique_id))


def main() -> None:
    db_session.global_init("db/users.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
