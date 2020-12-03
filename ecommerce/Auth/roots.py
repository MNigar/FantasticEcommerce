from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect,flash
from datetime import datetime

@app.route('/')
def defineusertype():
    return render_template('general/entrance.html')
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
      usertypeid=4
      user=User(Name=name,Surname=surname,Phone=phone,Email=email,Password=password,UserTypeId=usertypeid)
      db.session.add(user)     
      db.session.commit()
      return render_template('general/login.html')
     else:
      flash('İstifadəçi mövcuddur')
      return render_template('general/registration.html')

    if request.method=='GET':
      return render_template('general/registration.html')
    

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
      usertypeid=3
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

