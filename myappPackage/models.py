
from myappPackage import db

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String(100))
    price = db.Column(db.Double)
    count = db.Column(db.Integer)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __init__(self,productName,price,count):
        self.productName=productName
        self.price=price
        self.count=count

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    firstName = db.Column(db.String(100),nullable=False)
    lastName = db.Column(db.String(100),nullable=False)
    profileIMG = db.Column(db.String(20),nullable=False,default="static/images/defaultUserPhoto.png")
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    products = db.relationship('Product',backref='owner',lazy=True) #user have one to many relationship

    def __init__(self,username,firstName,lastName,email,password):
        self.username=username
        self.email=email
        self.firstName=firstName
        self.lastName=lastName
        self.password=password