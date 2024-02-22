from flask import Flask
from data.__all_models import User, Jobs
from data import db_session
import datetime
import time


app = Flask(__name__)


def main():
    db_session.global_init("db/users.sqlite")

    job = Jobs()
    job.team_leader = "1"
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = "15"
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now
    job.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()

    # app.run()


if __name__ == '__main__':
    main()
