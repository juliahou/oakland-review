#!flask/bin/python

from flask import Flask, render_template, request, redirect, url_for
import flask_admin as admin
import flask_login as login
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate
import click

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'meow'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)

    def __init__(self, email='', username='', password=''):
        self.username = username
        self.email = email
        self.password = password
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True)
    embed = db.Column(db.String(5000), unique=True)
    
    # def __init__(self, num=0, embed=''):
    #     self.num = num
    #     self.embed = embed
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return '<Issue %d>' % self.num

class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return render_template('login.html')
        return super(MyAdminIndexView, self).index()

admin = Admin(app, name='Admin', index_view=MyAdminIndexView(), base_template="admin/admin.html", template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Issue, db.session))

@app.cli.command()
def init_db():
    db.create_all()

    # Create a test user
    new_user = User('jjhou@andrew.cmu.edu', 'jjhou', 'admin')
    new_user.display_name = 'Julia'
    db.session.add(new_user)
    db.session.commit()

# if __name__ == '__main__':
#     init_db()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/admin')
@login_required
def admin():
    pass

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/read')
def read():
    return render_template('read.html')

@app.route('/issue/<int:issue_id>')
def show_issue(issue_id):
    return render_template('issue.html', issue_id=issue_id)

@app.route('/login',methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        # flash('Username or Password is invalid' , 'error')
        return render_template('login.html')
    login_user(registered_user)
    return redirect(url_for('admin.index'))

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')