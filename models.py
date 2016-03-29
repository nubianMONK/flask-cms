from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Page(db.Model):
	__tablename__ = "pages"
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	content = db.Column(db.Text, nullable=False)
        author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
	author=db.relationship('Author') 
	
	def __init__(self, page_title,page_content):
		self.page_title = page_title
		self.page_content = page_content
		
		
	def __repr__(self):
		return '<page_title {}>'.format(self.page_title)
		
class Author(db.Model):
	__tablename__ = "author"
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	
	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return '<author_name {}>'.format(self.name)
