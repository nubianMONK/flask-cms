from views import db

content_tags = db.Table('content_tags',
                        db.Column('content_id', db.Integer, db.ForeignKey('contents.content_id')),
db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id')),
db.UniqueConstraint('content_id', 'tag_id', name='uix_1')


)



class Content(db.Model):

    __tablename__ = "contents"

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    payload = db.Column(db.UnicodeText, nullable=False)
    author = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    content_tags = db.relationship('Tag', secondary=content_tags,
                                   backref=db.backref('contents', lazy='dynamic'))

    def __init__(self, title, payload, author):
        self.title = title
        self.payload = payload
        self.author = author

    def __repr__(self):
        return '<Content {}>'.format(self.payload)


class Tag(db.Model):

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __repr__(self):
        return '<Tag {}>'.format(self.tag_name)


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    email_address = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    contents = db.relationship('Content', backref='users', lazy='dynamic')
    tags = db.relationship('Tag', backref='users', lazy='dynamic')


    def __init__(self, user_name, email_address, password):
        self.user_name = user_name
        self.email_address = email_address
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.user_name)
