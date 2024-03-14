from flask import Flask, redirect, render_template, request, abort
from data.__all_models import *
from data import db_session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index/<title>')
def index(title='main'):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.id == 1:
            jobs = db_sess.query(Jobs).all()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.team_leader.like(current_user.id) |
                                              Jobs.collaborators.contains(current_user.id))
        return render_template('main_jobs.html', title=title, jobs=jobs)
    return render_template('base.html', title=title)


@app.route('/main_dep')
def main_dep(title='main'):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.id == 1:
            deps = db_sess.query(Department).all()
        else:
            deps = db_sess.query(Department).filter(Department.chief.like(current_user.id) | Department.members.contains(current_user.id))
        return render_template('main_dep.html', title=title, departments=deps)
    return render_template('base.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.hashed_password = form.hashed_password.data
        user.modified_date = form.modified_date.data
        user.password(user.hashed_password)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobadd.html', title='Добавление работы', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobadd.html', title='Редактирование новости', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/main_dep')
    return render_template('departmentadd.html', title='Добавление департамента', form=form)


@app.route('/add_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Department).filter(Department.id == id).first()
        else:
            dep = db_sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Department).filter(Department.id == id).first()
        else:
            dep = db_sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/main_dep')
        else:
            abort(404)
    return render_template('departmentadd.html', title='Редактирование департамента', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        dep = db_sess.query(Department).filter(Department.id == id).first()
    else:
        dep = db_sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/main_dep')


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    app.run(port=8080, host='127.0.0.1')
