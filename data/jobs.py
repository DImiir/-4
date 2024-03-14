import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, UserMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Job> {self.job}'


