from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Exercices, Startstop, Codes
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
        if current_user.username == 'admin':
            return redirect(url_for('admin.index'))
        return redirect(request.args.get('next') or url_for('index'))
    flash('Username or Password is invalid' , 'error')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    ex = Exercices.query.filter_by(id=99).first()
    if request.method == 'GET':
        return render_template('exo.html', ex=ex, id=str(ex.id))
    solution = request.form['solution']
    if (solution == ex.solution):
        return render_template('message.html', message='Bravo!')
    flash('Bad solution, try again!')
    return redirect(url_for('test'))


@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    if current_user.level==7:
        return render_template('message.html', message='Félicitations! You are the best :)')
    stst=Startstop.query.all()[0]
    if stst.status==0:
        return render_template('message.html', message='Un peu de patience... On commence tout de suite!')
    if stst.status==2:
        return render_template('message.html', message='Désolé, le concours est terminé ;(')
    if current_user.get_level() > 6:
        return redirect(url_for('index'))
    ex = Exercices.query.filter_by(id=current_user.get_level()).first()
    if request.method == 'GET':
        return render_template('exo.html', ex=ex, id=str(ex.id))
    solution = request.form['solution']
    codetext = request.form['code']
    if (solution == ex.solution) and (stst.status==1):
        code = Codes(code=codetext, user_id=current_user.get_id())
        current_user.level+=1
        db.session.add(code)
        db.session.commit()
        return redirect(url_for('start'))
    flash('Bad solution, try again!')
    return redirect(url_for('start'))

@app.route('/results', methods=['GET'])
def results():
    rank={}
    for u in User.query.all():
        r = u.get_rank()
        if r > 0:
            rank[r]=u

    return render_template('results.html', rank=rank, len=len(rank))
