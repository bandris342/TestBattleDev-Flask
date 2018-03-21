from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user , logout_user , current_user , login_required
from app.models import db, User, Exercices
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	user = User(username=request.form['username'], password=request.form['password'])
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
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))

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
