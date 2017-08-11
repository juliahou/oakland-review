#!flask/bin/python

from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

from models import User, Issue
admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Issue, db.session))

@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/issue/<int:issue_id>')
def show_issue(issue_id):
    return render_template('issue.html', issue_id=issue_id)