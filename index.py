import pymysql
from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import backref
from flask_migrate import Migrate
from datetime import datetime
app=Flask(__name__,template_folder='template' ,static_folder='assets')
app.config['SECRET_KEY'] = 'hardsecretkey'
userpass = 'mysql+pymysql://root:Aa555555@@'
basedir  = '127.0.0.1'
dbname   = '/fantasticecommerce'
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

class User(db.Model):
    __tablename__ = 'User'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    Surname=db.Column(db.String(50),nullable=False)
    Phone=db.Column(db.String(50),nullable=False)
    Email=db.Column(db.String(50),nullable=False)
    Password=db.Column(db.String(50),nullable=False)
    UserTypeId=db.Column(db.Integer,ForeignKey('UserType.Id'),nullable=False)
    shop= db.relationship("Shop", backref="User",lazy='select',uselist=False)
  
    # cart=db.relationship("Cart", back_populates="User")
    # ratings=db.relationship("Rating", back_populates="User")
    # order=db.relationship("Order", back_populates="User")
    # notification=db.relationship("Notification", back_populates="User")

    def __repr__(self):
        return f"User('{self.Name}','{self.Surname}','{self.Phone}','{self.Email}','{self.Password}','{self.UserTypeId}')"
class UserType(db.Model):
    __tablename__ = 'UserType'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    users=db.relationship('User',backref="UserType",lazy='select')
    def __repr__(self):
        return f"UserType('{self.Name}')"
class Shop(db.Model):
    __tablename__='Shop'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    Voen=db.Column(db.String(50),nullable=True)
    RegisterDate=db.Column(db.DateTime, nullable=False)
    Adress=db.Column(db.String(50),nullable=True)
    Status=db.Column(db.Integer,nullable=False)
    UserId=db.Column(db.Integer,ForeignKey('User.Id'),nullable=False)
    

@app.route('/')
def defineusertype():
        return render_template('general/entrance.html')
# Customer registration
@app.route('/creg',methods=['GET','POST'])    
def creg():
    
    if request.method=='POST':
     newuser = User.query.filter_by(Email=request.form['Email'] ).first()
     if newuser is None: 
      name=request.form['Name']
      surname=request.form['Surname']
      phone=request.form['Phone']
      email=request.form['Email']     
      password=request.form['Password']
      usertypeid=3
      user=User(Name=name,Surname=surname,Phone=phone,Email=email,Password=password,UserTypeId=usertypeid)
      db.session.add(user)     
      db.session.commit()
      return render_template('general/login.html')
     else:
      flash('İstifadəçi mövcuddur')
      return render_template('general/registration.html')

    if request.method=='GET':
      return render_template('general/registration.html')
    
@app.route('/login',methods=['GET','POST'])    
def login():
    if(request.method=="POST"):
        email=request.form['Email']
        password=request.form['Password']

        suser = User.query.filter_by(Email=email,Password= password).first()
       
       
        if suser is None:
             flash('İstifadəçi tapılmadı')
             return render_template('general/login.html')
        else:
         if(suser.UserTypeId==1):
             return 'admin'
         elif(suser.UserTypeId==2):
             return 'shop'
         else:
             return 'istifadeci'

    if(request.method=="GET"):
        return render_template('general/login.html')

# Shop registration

@app.route('/sreg',methods=['GET','POST'])    
def sreg():
 if request.method=='POST':
     newuser = User.query.filter_by(Email=request.form['Email'] ).first()
     if newuser is None: 
      name=request.form['Name']
      surname=request.form['Surname']
      phone=request.form['Phone']
      email=request.form['Email']     
      password=request.form['Password']  
      usertypeid=2
      user=User(Name=name,Surname=surname,Phone=phone,Email=email,Password=password,UserTypeId=usertypeid)
      db.session.add(user)
      db.session.commit()
      shopname=request.form['shopname']
      voen=request.form['voen']
      address=request.form['address']
      userid=user.Id
      status=0
      date=datetime.now()
      shop=Shop(Name=shopname,Voen=voen,Adress=address,UserId=userid,Status=status,RegisterDate=date)
      db.session.add(shop)
      db.session.commit()
      return render_template('general/login.html')

     else:
        flash('İstifadəçi mövcuddur')
        return render_template('shop/registration.html')

 if request.method=='GET':
      return render_template('shop/registration.html')



if __name__ == '__main__':
    
    app.run(debug=True)