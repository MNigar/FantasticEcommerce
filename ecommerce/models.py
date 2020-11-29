from ecommerce import db 


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

class Category(db.Model):
    __tablename__='Category'
    Id=db.Column(db.Integer,primary_key=True)
    ParentCategoryId=db.Column(db.Integer,nullable=True)
    Name=db.Column(db.String(50),nullable=False)  
    product= db.relationship("Products", backref="Category",lazy='select',uselist=False)
    def __repr__(self):
        return f"Category('{self.ParentCategoryId}','{self.Name}')"
class UserType(db.Model):
    __tablename__ = 'UserType'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    users=db.relationship('User',backref="UserType",lazy='select')
    def __repr__(self):
        return f"UserType('{self.Name}')"
class User(db.Model):
    __tablename__ = 'User'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    Surname=db.Column(db.String(50),nullable=False)
    Phone=db.Column(db.String(50),nullable=False)
    Email=db.Column(db.String(50),nullable=False)
    Password=db.Column(db.String(50),nullable=False)
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

class Products(db.Model):
    __tablename__='Products'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)    
    Count=db.Column(db.Integer, nullable=False)
    CategoryId=db.Column(db.Integer,db.ForeignKey('Category.Id'),nullable=False)
    Price=db.Column(db.Numeric,nullable=False)   
    ShopId=db.Column(db.Integer,db.ForeignKey('Shop.Id'),nullable=False)
    images=db.relationship("ProductImage", backref="iproduct",lazy='select')
    pcolors=db.relationship("Color",secondary=pcolors, backref="cproduct",lazy='select')
    psizes=db.relationship("Size",secondary=psizes, backref="sproduct",lazy='select')    
    ratings=db.relationship('Rating',backref="Products",lazy='select')
    
    def __repr__(self):
        return f"Products('{self.Name}','{self.Count}','{self.CategoryId}','{self.Price}','{self.ShopId}')"

class ProductImage(db.Model):
    __tablename__='ProductImage'
    Id=db.Column(db.Integer,primary_key=True)
    ProductId=db.Column(db.Integer,db.ForeignKey('Products.Id'),nullable=False)
    Image=db.Column(db.String(500),nullable=False)
    MainImage=db.Column(db.String(500),nullable=False)
    
   
    def __repr__(self):
        return f"ProductImage('{self.ProductId}','{self.Image}','{self.MainImageId}')"
class Rating(db.Model):
    __tablename__='Rating'
    Id=db.Column(db.Integer,primary_key=True)
    ProductId=db.Column(db.Integer,db.ForeignKey('Products.Id'),nullable=False)
    UserId=db.Column(db.Integer,db.ForeignKey('User.Id'),nullable=False)
    Amount=db.Column(db.Integer,nullable=False)
