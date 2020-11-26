import sqlite3
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import backref

from werkzeug.utils import secure_filename
from datetime import datetime
import os
app=Flask(__name__,template_folder='template' ,static_folder='assets')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
class User(db.Model):
    __tablename__ = 'User'
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    Surname=db.Column(db.String(50),nullable=False)
    Phone=db.Column(db.String(50),nullable=False)
    Email=db.Column(db.String(50),nullable=False)
    Password=db.Column(db.String(50),nullable=False)
    UserTypeId=db.Column(db.Integer,ForeignKey('UserType.Id'),nullable=False)
    # shop= db.relationship("Shop", back_populates="User")
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
@app.route('/type',methods=['GET','POST'])
def defineusertype():
    if request.method == 'POST':
    
        if  request.form['utype']== "admin":
            return render_template('general/login.html')
        elif request.form['utype']== "shop":
            return render_template('general/shopregistration.html')
        elif request.form['utype']== "customer":
            return render_template('general/registration.html')
    elif request.method == 'GET':
        quser=UserType.query.all()
        return render_template('general/entrance.html',users=quser)

@app.route('/creg',methods=['GET','POST'])    
def creg():
     if request.method=='POST':
      name=request.form['Name']
      surname=request.form['Surname']
      phone=request.form['phone']
      email=request.form['email']     
      password=request.form['password']
      usertypeid=2
      user=User(Name=name,Surname=surname,Phone=phone,Email=email,Password=password,UserTypeId=usertypeid)
      db.session.add(user)
      db.session.commit()
      return "succes"
     if request.method=='GET':
      return render_template('general/registration.html')



# @event.listens_for(UserType.__table__, 'after_create')
# def create_UserType(*args, **kwargs):
#     db.session.add(UserType(name='admin'))
#     db.session.add(UserType(name='shop'))
#     db.session.add(UserType(name='customer'))
#     db.session.commit()
@app.route('/',methods=['GET','POST'])
def new():
     return render_template('admin/example.html')
@app.route('/register',methods=['GET','POST'])
def register():
     if request.method=='POST':
      Name=request.form['Name']
      Surname=request.form['Surname']
      Image=request.files['Image']
      if Image.filename=='':
          flash("no selected file")
          return redirect(url_for('users'))
      file = request.files['Image']

      if allowed_file(file.filename):

          filename=secure_filename(file.filename)
          file.save(os.path.join('assets',app.config['UPLOAD_FOLDER'],filename))
          Image=os.path.join(app.config['UPLOAD_FOLDER'],filename)
      else:
          flash("NON allowed")
          return redirect(url_for('users'))

      user=Example(Name=Name,Surname=Surname,Image=Image)
      
      db.session.add(user)
      db.session.commit()
      return "succes"
@app.route('/users')
def user():
     quser=Example.query.all()
     return render_template('admin/users.html',users=quser)


# def user():
#      quser=Register.query.all()
#      return render_template('users.html',users=quser)
# @app.route('/delete/<id>')
# def delete(id):
#      user=Register.query.filter_by(id=int(id)).delete()
#      db.session.commit()
#      return redirect(url_for('user'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    
    app.run(debug=True)




















# from app import app

# if __name__ == '__main__':
    
#     app.run(debug=True)
