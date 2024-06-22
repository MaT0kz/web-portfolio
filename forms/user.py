from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField, RadioField, FileField
from wtforms.validators import DataRequired

photos = UploadSet('photos', IMAGES)


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия')
    role = SelectField("Выберите роль", choices=["Разработчик", "Организация"])
    sphere = StringField('Моя отрасль', validators=[DataRequired()], id="sphere", name="sphere")
    nickname = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField('Создать пофиль')


class LoginForm(FlaskForm):
    login = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProfileForm(FlaskForm):
    photo = FileField('Аватар', name='file')
    sphere = StringField('Отрасль')
    experience = StringField('Стаж')
    about = StringField('Обо мне')
    submit = SubmitField("Сохранить")


class ProjectAddForm(FlaskForm):
    name = StringField("Имя проекта", validators=[DataRequired()])
    sphere = StringField("Отрасль", validators=[DataRequired()])
    about = TextAreaField("Описание проекта", validators=[DataRequired()])
    photo = FileField("Добавить обложку проекта", name='file')
    submit = SubmitField("Сохранить")


class ProjectForm(FlaskForm):
    name = StringField("Имя проекта", validators=[DataRequired()])
    sphere = StringField("Отрасль", validators=[DataRequired()])
    about = TextAreaField("Описание проекта", validators=[DataRequired()])
    file = FileField("Обложка проекта", name='file')
    submit = SubmitField("Сохранить")


class ScrollForm(FlaskForm):
    search = StringField("Поиск")
    experience = StringField("Стаж")
    sphere = StringField("Сфера")
    submit = SubmitField("Применить")


class OrganisationProfileForm(FlaskForm):
    name = StringField("Название организации")
    sphere = StringField("Сфера Деятельности")
    links = StringField("Ссылки на соглашения")
    about = TextAreaField("Об организации")
    photo = FileField("Аватар организации", name='file')
    submit = SubmitField("Сохранить")


class VacancyForm(FlaskForm):
    name = StringField("Название вакансии", validators=[DataRequired()])
    sphere = StringField("Сфера вакансии", validators=[DataRequired()])
    experience = StringField("Стаж вакансии", validators=[DataRequired()])
    about = StringField("Описание вакансии", validators=[DataRequired()])
    requirements = TextAreaField("Требования к вакансии")
    submit = SubmitField("Создать вакансию")