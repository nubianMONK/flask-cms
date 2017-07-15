

#from views import db
from blog_api import db, Post, Author

db.create_all()

db.session.commit()
