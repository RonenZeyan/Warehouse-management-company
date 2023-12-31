
# from myappPackage import db,login_manger,app
# from flask_login import UserMixin
# from datetime import datetime
# from itsdangerous import URLSafeTimedSerializer as Serializer
# from sqlalchemy import CheckConstraint

# @login_manger.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class Product(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     productName = db.Column(db.String(100))
#     price = db.Column(db.Double)
#     count = db.Column(db.Integer)
#     ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

#     def __init__(self,productName,price,count,ownerID):
#         self.productName=productName
#         self.price=price
#         self.count=count
#         self.ownerID=ownerID

# class User(db.Model,UserMixin):
#     id= db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(100),unique=True,nullable=False)
#     firstName = db.Column(db.String(100),nullable=False)
#     lastName = db.Column(db.String(100),nullable=False)
#     profileIMG = db.Column(db.String(20),nullable=False,default="defaultUserPhoto.png")
#     email = db.Column(db.String(100),unique=True,nullable=False)
#     password = db.Column(db.String(60),nullable=False)
#     products = db.relationship('Product',backref='owner',lazy=True) #user have one to many relationship
#     posts = db.relationship('Post',backref='PostOwner',lazy=True) 
#     comments = db.relationship('Comment',backref='OwnerOFcomment',lazy=True) 
#     rentedWarehoses = db.relationship('WareHouse',backref='WareHouseOwner',lazy=True) 
#     bio = db.Column(db.Text,nullable=True)

#     def __init__(self,username,firstName,lastName,email,password):
#         self.username=username
#         self.email=email
#         self.firstName=firstName
#         self.lastName=lastName
#         self.password=password

#     def get_reset_token(self):
#         s=Serializer(app.config['SECRET_KEY'],salt='pw-reset')
#         return s.dumps({'user_id':self.id})

#     @staticmethod
#     def verify_reset_token(token,age=3600):
#         s = Serializer(app.config['SECRET_KEY'],salt='pw-reset')
#         try:
#             user_id = s.loads(token,max_age=age)['user_id']
#         except:
#             return None
#         return User.query.get(user_id)

# class Post(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
#     comments = db.relationship('Comment',backref='CommentOwner',lazy=True) 


#     def __init__(self,title,content,ownerID):
#         self.title=title
#         self.content=content
#         self.ownerID=ownerID


# class Comment(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
#     postID = db.Column(db.Integer,db.ForeignKey("post.id"),nullable=False)

#     def __init__(self,content,ownerID,postID):
#         self.content=content
#         self.ownerID=ownerID
#         self.postID=postID

# class WareHouses(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     type = db.Column(db.Integer,nullable=False) #type 1 mean small warehouse,2 mean medium warehosue,3 mean large warehouse
#     status = db.Column(db.Boolean,nullable=False) #if rent or not yet 


#     def __init__(self,type,status):
#         self.type=type
#         self.status=status
    

# class WareHouse(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
#     WareHouseID = db.Column(db.Integer,db.ForeignKey("WareHouses.id"),nullable=False)
#     date_rented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
#     def __init__(self,ownerID,WareHouseID):
#         self.ownerID=ownerID
#         self.WareHouseID=WareHouseID



from myappPackage import db,login_manger,app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String(100))
    price = db.Column(db.Double)
    count = db.Column(db.Integer)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __init__(self,productName,price,count,ownerID):
        self.productName=productName
        self.price=price
        self.count=count
        self.ownerID=ownerID

class User(db.Model,UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    firstName = db.Column(db.String(100),nullable=False)
    lastName = db.Column(db.String(100),nullable=False)
    profileIMG = db.Column(db.String(20),nullable=False,default="defaultUserPhoto.png")
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    products = db.relationship('Product',backref='owner',lazy=True) #user have one to many relationship
    posts = db.relationship('Post',backref='PostOwner',lazy=True) 
    comments = db.relationship('Comment',backref='OwnerOFcomment',lazy=True) 
    rentedWarehoses = db.relationship('WareHouse',backref='WareHouseOwner',lazy=True) 
    bio = db.Column(db.Text,nullable=True)

    def __init__(self,username,firstName,lastName,email,password):
        self.username=username
        self.email=email
        self.firstName=firstName
        self.lastName=lastName
        self.password=password

    def get_reset_token(self):
        s=Serializer(app.config['SECRET_KEY'],salt='pw-reset')
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token,age=3600):
        s = Serializer(app.config['SECRET_KEY'],salt='pw-reset')
        try:
            user_id = s.loads(token,max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    comments = db.relationship('Comment',backref='CommentOwner',lazy=True) 


    def __init__(self,title,content,ownerID):
        self.title=title
        self.content=content
        self.ownerID=ownerID

class Comment(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    postID = db.Column(db.Integer,db.ForeignKey("post.id"),nullable=False)

    def __init__(self,content,ownerID,postID):
        self.content=content
        self.ownerID=ownerID
        self.postID=postID

class houseslist(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    type = db.Column(db.Integer,nullable=False) #type 1 mean small warehouse,2 mean medium warehosue,3 mean large warehouse
    status = db.Column(db.Boolean,nullable=False) #if rent or not yet 


    def __init__(self,type,status):
        self.type=type
        self.status=status
    

class WareHouse(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    WareHouseID = db.Column(db.Integer,db.ForeignKey("houseslist.id"),nullable=False)
    date_rented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    def __init__(self,ownerID,WareHouseID):
        self.ownerID=ownerID
        self.WareHouseID=WareHouseID



