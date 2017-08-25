#!flask/bin/python

from flask import Flask, render_template
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

class MyView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'meow'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # def __init__(self, username='', email=''):
    #     self.username = username
    #     self.email = email
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

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Issue, db.session))

def init_db():
    db.create_all()

    # Create a test user
    new_user = User('a@a.com', 'aaaaaaaa')
    new_user.display_name = 'Nathan'
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    init_db()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

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