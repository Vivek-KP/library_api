from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db' 

    from library.models.booksModel import Book 
    from library.models.memberModel import Member
    from library.models.issuedBooks import IssuedBooks

    db.init_app(app)
    migrate.init_app(app,db)

    from library.controller.memberController.membersController import members_bp
    from library.controller.bookController.booksController import books_bp

    app.register_blueprint(members_bp)
    app.register_blueprint(books_bp)
    
    with app.app_context():
        db.create_all()

    return app