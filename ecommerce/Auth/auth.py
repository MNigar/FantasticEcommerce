from ecommerce import app,db,bcrypt
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect,flash,Blueprint,session,escape
from datetime import datetime
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash
auth=Blueprint("auth",__name__,template_folder='Molla_HTML' ,static_folder='Molla_HTML')


from ecommerce.admin import admin
@auth.route('/logout')    
def logout():
    logout_user()
    return redirect(url_for('admin.plist'))
# @auth.route('/account')    
# def account():


@auth.route('/')
def defineusertype():
    return render_template('general/entrance.html')
@auth.route('/login',methods=['GET','POST'])    
def login():
    if current_user.is_authenticated:
        return redirect(url_for(admin.listp))
    if(request.method=="POST"):
        email=request.form['Email']
        password=request.form['Password']

        suser = User.query.filter_by(Email=email).first()
       
       
        if suser and bcrypt.check_password_hash(suser.Password,password) :
            #  flash('İstifadəçi tapılmadı')
            #  return render_template('general/login.html')
        #  login_user(suser,remember=request.form['exampleCheck1'])
         
         if(suser.UserTypeId==1):
             session.clear()
             session['userid'] = suser.Id
             session['UserTypeId'] = 1
             return redirect(url_for('auth.user'))
         elif(suser.UserTypeId==2):
             session.clear()
             session['userid'] = suser.Id

             session['UserTypeId']=2
             return 'shop'
         else:
             session.clear()
             session['userid'] = suser.Id
             session['UserTypeId']=3
             return redirect(url_for('auth.user'))
        else:
            flash('İstifadəçi tapılmadı')
            return redirect(url_for('auth.login'))
    if(request.method=="GET"):
        return render_template('login.html')
# Customer registration
@auth.route('/creg',methods=['GET','POST'])    
def creg():
    if current_user.is_authenticated:
        return redirect(url_for(admin.listp))
    if request.method=='POST':
     newuser = User.query.filter_by(Email=request.form['Email'] ).first()
     if newuser is None: 
      name=request.form['Name']
      surname=request.form['Surname']
      phone=request.form['Phone']
      email=request.form['Email']     
      password=bcrypt.generate_password_hash(request.form['Password'] ).decode('utf-8')
    
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
    

# Shop registration

@auth.route('/sreg',methods=['GET','POST'])    
def sreg():
 if current_user.is_authenticated:
        return redirect(url_for(admin.listp))
 if request.method=='POST':
     newuser = User.query.filter_by(Email=request.form['Email'] ).first()
     if newuser is None: 
      name=request.form['Name']
      surname=request.form['Surname']
      phone=request.form['Phone']
      email=request.form['Email']     
      password=bcrypt.generate_password_hash(request.form['Password'] ).decode('utf-8')     
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
@auth.route("/user")
def user():
    if "userid" in session:
        user=session["userid"]
        return f"{user}"
    else:
        return "sehv"
