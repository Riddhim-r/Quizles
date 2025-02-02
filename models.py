from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable = False)
    passhash = db.Column(db.String(512), nullable= False)
    name = db.Column(db.String(64), nullable = True)

class Product(db.Model):
    __tablename__= 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    man_date = db.Column(db.Date, nullable = False)

class Category (db.Model) :
    __tablename__= 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db. Column (db. String(64), nullable = False)
    ## relationships
    products = db.relationship('Product', backref='category', lazy=True)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db. Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db. Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db. Integer, nullable = False)

class Order (db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db. Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db. Integer, db. ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db. Integer, nullable = False)
    price = db.Column(db. Float, nullable = False)
    datetime = db. Column(db.DateTime, nullable = False)
