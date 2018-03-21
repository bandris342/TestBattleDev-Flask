from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Exercices
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	user = User(username=request.form['username'], password=generate_password_hash(request.form['password']))
	if db.session.query(User.id).filter_by(username=user.username).scalar() is not None:
		flash('Username already exists', 'error')
		return redirect(url_for('register'))
	db.session.add(user)
	db.session.commit()
	flash('User successfully registered')
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user =  db.session.query(User).filter_by(username=username).first()
    if registered_user and check_password_hash(registered_user.password, password):
        login_user(registered_user)
        return redirect(request.args.get('next') or url_for('index'))
    flash('Username or Password is invalid' , 'error')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    if current_user.get_level() > 6:
        return redirect(url_for('index'))
    ex = Exercices.query.filter_by(id=current_user.get_level()).first()
    if request.method == 'GET':
        return render_template('exo.html', ex=ex, id=str(ex.id))
    solution = request.form['solution']
    if solution == ex.solution:
        current_user.level+=1
        db.session.commit()
        return redirect(url_for('start'))
    flash('Bad solution, try again!')
    return redirect(url_for('start'))
