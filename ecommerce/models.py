
from ecommerce import db,login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

class Size(db.Model):
    __tablename__ = 'Size'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
   

    def __repr__(self):
        return f"Size('{self.Name}')"
class Color(db.Model):
    __tablename__='Color'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    

    def __repr__(self):
        return f"Color('{self.Name}')"


class UserType(db.Model):
    __tablename__ = 'UserType'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    users=db.relationship('User',backref="UserType",lazy='select')
    def __repr__(self):
        return f"UserType('{self.Name}')"
class User(db.Model,UserMixin):
    __tablename__ = 'User'
    Id=db.Column(db.Integer,primary_key=True)
   
    Name=db.Column(db.String(50),nullable=False)
    Surname=db.Column(db.String(50),nullable=False)
    Phone=db.Column(db.String(50),nullable=False)
    Email=db.Column(db.String(50),nullable=False)
    Password=db.Column(db.String(100),nullable=False)
    UserTypeId=db.Column(db.Integer,db.ForeignKey('UserType.Id'),nullable=False)
    shop= db.relationship("Shop", backref="User",lazy='select',uselist=False)
    ratings=db.relationship('Rating',backref="User",lazy='select')
    
    # cart=db.relationship("Cart", back_populates="User")
    # ratings=db.relationship("Rating", back_populates="User")
    # order=db.relationship("Order", back_populates="User")
    # notification=db.relationship("Notification", back_populates="User")

    def __repr__(self):
        return f"User('{self.Name}','{self.Surname}','{self.Phone}','{self.Email}','{self.Password}','{self.UserTypeId}')"

class Shop(db.Model):
    __tablename__='Shop'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    Voen=db.Column(db.String(50),nullable=True)
    RegisterDate=db.Column(db.DateTime, nullable=False)
    Adress=db.Column(db.String(50),nullable=True)
    Status=db.Column(db.Integer,nullable=False)
    UserId=db.Column(db.Integer,db.ForeignKey('User.Id'),nullable=False)
    products=db.relationship('Products',backref="Shop",lazy='select')

    def __repr__(self):
        return f"Shop('{self.Name}','{self.Voen}','{self.RegisterDate}','{self.Adress}','{self.Phone}','{self.Status}','{self.UserId}')"
pcolors=db.Table('color-product',
  db.Column('product_id',db.Integer,db.ForeignKey('Products.Id')),
  db.Column('color_id',db.Integer,db.ForeignKey('Color.Id')))

psizes=db.Table('size-product',
  db.Column('product_id',db.Integer,db.ForeignKey('Products.Id')),
  db.Column('size_id',db.Integer,db.ForeignKey('Size.Id')))

class Category(db.Model):
    __tablename__ = 'Category'
    Id=db.Column(db.Integer,primary_key=True)
    ParentCategoryId = db.Column(db.Integer, nullable=True)
    Name=db.Column(db.String(50), nullable=False)  
    product= db.relationship("Products", backref="Category",lazy='select',uselist=False)
    
    def __repr__(self):
        return f"Category('{self.ParentCategoryId}','{self.Name}')"

class Products(db.Model):
    __tablename__='Products'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)    
    Count=db.Column(db.Integer, nullable=False)
    CategoryId=db.Column(db.Integer,db.ForeignKey('Category.Id'),nullable=False)
    Price=db.Column(db.Numeric,nullable=False)   
    ShopId=db.Column(db.Integer,db.ForeignKey('Shop.Id'),nullable=False)
    Description=db.Column(db.String(600),nullable=False)
    Status=db.Column(db.Integer,nullable=False)
    images=db.relationship("ProductImage", backref="iproduct",lazy='select')
    pcolors=db.relationship("Color",secondary=pcolors, backref="cproduct",lazy='select')
    psizes=db.relationship("Size",secondary=psizes, backref="sproduct",lazy='select')    
    ratings=db.relationship('Rating',backref="Products",lazy='select')
    
    def __repr__(self):
        return f"Products('{self.Name}','{self.Count}','{self.CategoryId}','{self.Price}','{self.ShopId}','{self.Status}','{self.Description}')"

class ProductImage(db.Model):
    __tablename__='ProductImage'
    Id=db.Column(db.Integer,primary_key=True)
    ProductId=db.Column(db.Integer,db.ForeignKey('Products.Id'),nullable=False)
    Image=db.Column(db.String(1000),nullable=False)
    MainImage=db.Column(db.String(1000),nullable=False)
    def __repr__(self):
        return f"ProductImage('{self.ProductId}','{self.Image}','{self.MainImageId}')"
class Rating(db.Model):
    __tablename__='Rating'
    Id=db.Column(db.Integer,primary_key=True)
    ProductId=db.Column(db.Integer,db.ForeignKey('Products.Id'),nullable=False)
    UserId=db.Column(db.Integer,db.ForeignKey('User.Id'),nullable=False)
    Amount=db.Column(db.Integer,nullable=False)

class Order(db.Model):
    
    __tablename__='Order'
    Id=db.Column(db.Integer,primary_key=True)
    UserId=db.Column(db.Integer,db.ForeignKey('User.Id'),nullable=True)
    ProductId=db.Column(db.Integer,db.ForeignKey('Products.Id'),nullable=False)
    Count=db.Column(db.Integer, nullable=False)
    Price=db.Column(db.Numeric, nullable=False)
    Status=db.Column(db.Integer, nullable=False)   
    SizeId=db.Column(db.Integer,db.ForeignKey('Size.Id'),nullable=False)
    ColorId=db.Column(db.Integer,db.ForeignKey('Color.Id'),nullable=False)
    CreateDate=db.Column(db.DateTime,nullable=False)       
    ShopId=db.Column(db.Integer,db.ForeignKey('Shop.Id'),nullable=False)
    Total=db.Column(db.Numeric, nullable=False)
    Name=db.Column(db.String(30), nullable=False)
    Surname=db.Column(db.String(30), nullable=False)
    Address=db.Column(db.String(600), nullable=False)
    Phone=db.Column(db.String(50), nullable=False)
    Email=db.Column(db.String(50), nullable=False)


    users=db.relationship('User',backref="Order",lazy='select')
    product=db.relationship("Products", backref="Order",lazy='select')
    colors=db.relationship("Color", backref="Order",lazy='select')
    sizes=db.relationship("Size",backref="Order",lazy='select')
    shops=db.relationship("Shop", backref="Order",lazy='select')
    
    def __repr__(self):
        return f"Order('{self.UserId}','{self.ProductId}','{self.Count}','{self.Status}','{self.SizeId}','{self.ColorId}','{self.CreateDate}','{self.Amount}','{self.ShopId}','{self.Total}')"

class Slider(db.Model):
    __tablename__='Slider'
    Id=db.Column(db.Integer,primary_key=True)
    Text=db.Column(db.String(100),nullable=True)   
    Image=db.Column(db.String(1000),nullable=False)
    URL=db.Column(db.String(1000),nullable=True)  
    def __repr__(self):
        return f"Slider('{self.Text}','{self.Image}','{self.URL}')"