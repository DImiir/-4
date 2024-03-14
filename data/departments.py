import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase, UserMixin):
    __tablename__ = 'department'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

