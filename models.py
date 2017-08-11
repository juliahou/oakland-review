from app import app, db

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

def init_db():
    db.create_all()

    # Create a test user
    new_user = User('a@a.com', 'aaaaaaaa')
    new_user.display_name = 'Nathan'
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    init_db()