from models import app, db
import views

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print app.url_map
    app.run(debug=True)
