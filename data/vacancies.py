import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Vacancy(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'vacancies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="Название вакансии")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    sphere = sqlalchemy.Column(sqlalchemy.String, default="Сфера вакансии")
    experience = sqlalchemy.Column(sqlalchemy.String, default="Стаж вакансии")
    about = sqlalchemy.Column(sqlalchemy.String, default="Описание вакансии")
    requirements = sqlalchemy.Column(sqlalchemy.String, default="Требования к вакансии")
    account_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # account_type = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="organisation")


class Resume(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'resumes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="Название резюме")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    sphere = sqlalchemy.Column(sqlalchemy.String, default="Сфера резюме")
    experience = sqlalchemy.Column(sqlalchemy.String, default="Стаж резюме")
    about = sqlalchemy.Column(sqlalchemy.String, default="Описание резюме")
    requirements = sqlalchemy.Column(sqlalchemy.String, default="Требования к резюме")
    account_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # account_type = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="person")