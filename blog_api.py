
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields, marshal, marshal_with
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

#Model
################ 
relationship_table = db.Table('relationship_table',
											db.Column('post_id', db.Integer,db.ForeignKey('posts.post_id'), nullable=False),
											db.Column('author_id', db.Integer,db.ForeignKey('authors.author_id'), nullable=False),
											db.PrimaryKeyConstraint('post_id', 'author_id'))


class Post(db.Model):
	
	__tablename__ = "posts"
	
	post_id = db.Column(db.Integer, primary_key=True)
	post_title = db.Column(db.String, nullable=False)
	post_content = db.Column(db.Text, nullable=False)
	authors=db.relationship('Author', secondary=relationship_table, backref='posts' ) 
	
	def __init__(self, post_title,post_content):
		self.post_title = post_title
		self.post_content = post_content
		
		
	def __repr__(self):
		return '<post_title {}>'.format(self.post_title)
		
		
		

class Author(db.Model):
	
	__tablename__ = "authors"
	
	author_id = db.Column(db.Integer, primary_key=True)
	author_name = db.Column(db.String, nullable=False)
	
	def __init__(self, author_name):
		self.author_name = author_name
		
	def __repr__(self):
		return '<author_name {}>'.format(self.author_name)

################

# Post Fields
post_fields = {
	'post_id' : fields.Integer,
	'post_title' : fields.String,
	'post_content' : fields.String,
	'uri' : fields.Url('post',absolute=True, scheme='http')
	}

	
# Posts Fields
posts_fields = {
	'post_id' : fields.Integer,
	'post_title' : fields.String,
	'post_content' : fields.String,
	'uri' : fields.Url('posts',absolute=True, scheme='http')
	}

# Author Fields
author_fields = {
	'author_id' : fields.Integer,
	'author_name' : fields.String,
	'uri' : fields.Url('author',absolute=True, scheme='http')
	}
	
	
# Authors Fields
authors_fields = {
	'author_id' : fields.Integer,
	'author_name' : fields.String,
	'uri' : fields.Url('authors',absolute=True, scheme='http')
	}

################ post #############
#PostAPI
class PostAPI(Resource):

	

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('post_title', type=str, required=True, help='No post title provided',location='json')
		self.reqparse.add_argument('post_content', type=str, required=True, help='No post content provided',location='json')
		super(PostAPI, self).__init__()
		

	def get(self, post_id):
		p_id = post_id
		post = db.session.query(Post).filter_by(post_id = p_id).one()
		return {'post': marshal(post, post_fields)}
	
	def delete(self, post_id):
		p_id = post_id
		db.session.query(Post).filter_by(post_id=p_id).delete()
		db.session.commit()
	
		return {'result': True}
	
	@marshal_with(posts_fields)
	def put(self, post_id):
		
		args = self.reqparse.parse_args()
		updated_title = str(args['post_title'])
		updated_content = str(args['post_content'])
		p_id = post_id
		
		db.session.query(Post).filter_by(post_id=p_id).update({"post_title": updated_title})
		db.session.query(Post).filter_by(post_id=p_id).update({'post_content': updated_content})
		db.session.commit()
		
		return {'post_title':updated_title , 'post_content':updated_content}
		
	
#PostsAPI	
class PostsAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('post_title', type=str, required=True, help='No post title provided',location='json')
		self.reqparse.add_argument('post_content', type=str, required=True, help='No post content provided',location='json')
		super(PostsAPI, self).__init__()
	
	
	def get(self):
		posts = db.session.query(Post).all()
		return {'posts': [marshal(post, post_fields) for post in posts]}
		
		
	
	def post(self):
		args = self.reqparse.parse_args()
		post_title = Post(args['post_title'],args['post_content'] )
		post_content = Post(args['post_title'],args['post_content'] )
		
		db.session.add(post_title)
		db.session.add(post_content)
		db.session.commit()
		return {'posts': marshal(post_title, posts_fields),'posts': marshal(post_content, posts_fields)}
		
		
################ author #############
		
#AuthorAPI
class AuthorAPI(Resource):

	
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('author_name', type=str, required=True, help='No author name provided',location='json')
		
		super(AuthorAPI, self).__init__()
		

	def get(self, author_name):
		a_name = author_name
		author = db.session.query(Author).filter_by(author_name = a_name ).first()
		return {'author': marshal(author, author_fields)}
	
	def delete(self, author_name):

		a_name = author_name
		db.session.query(Author).filter_by(author_name = a_name).delete()
		db.session.commit()

		return {'result': True}
	
	@marshal_with(authors_fields)
	def put(self, author_name):
				
		author = author_name
		args = self.reqparse.parse_args()
		updated_name = str(args['author_name'])
		db.session.query(Author).filter_by(author_name=author).update({'author_name' : updated_name})
		db.session.commit()
		
		return {'author' : updated_name}
		
	
#AuthorsAPI	
class AuthorsAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('author_name', type=str, required=True, help='No author name  provided',location='json')
		super(AuthorsAPI, self).__init__()
	
	
	def get(self):
		authors = db.session.query(Author).all()
		return {'authors': [marshal(author, author_fields) for author in authors]}
		
		
	
	def post(self):
		args = self.reqparse.parse_args()
		author = Author(args['author_name'])
		db.session.add(author)
		db.session.commit()
		return {'author': marshal(author, author_fields)}


##############End Point Configs#################

#Post APIs
api.add_resource(PostsAPI, '/api/v1/posts', endpoint = 'posts')
api.add_resource(PostAPI, '/api/v1/post/<int:post_id>', endpoint = 'post')

#Author APIs
api.add_resource(AuthorsAPI, '/api/v1/authors', endpoint = 'authors')
api.add_resource(AuthorAPI, '/api/v1/author/<string:author_name>', endpoint = 'author')

if __name__ == '__main__':
    app.run(debug=True)