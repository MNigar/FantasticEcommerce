from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect, Blueprint,session
from datetime import datetime

from werkzeug.utils import secure_filename
import os
import random
import string


admin=Blueprint("admin",__name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','JPEG', 'gif','webp'}

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@admin.route('/orderl/<int:id>')
def orderl(id):
    userId=session["userid"]
    order=Order.query.filter_by(UserId=id).all()
    
    return render_template('admin/orderl.html',order=order)
#orderdelete
@admin.route('/delorder/<int:id>')    
def delorder(id):
    order=Order.query.filter_by(Id=id).delete()
    db.session.commit()
    if session['UserTypeId']==2:
     return redirect(url_for('shop.orderl'))
    if session['UserTypeId']==1:
     return redirect(url_for('admin.userlist'))


@admin.route('/admin')
def adminindex():
     return render_template('admin/index.html')


#ShopList
@admin.route('/shoplist')
def shoplist():
    shoplist=Shop.query.all()
    return render_template('admin/shoplist.html',shoplist=shoplist)
#ShopDelete
@admin.route('/shopdelete/<int:id>')
def shopdelete(id):
    shopDelete=Shop.query.filter_by(Id=id).delete()
    db.session.commit()    
    return redirect(url_for('admin.shoplist'))
  
    


#Categorylist
@admin.route('/catlist')
def categorylist():
    
    cat=Category.query.all()

    return render_template('admin/categorylist.html',category=cat)
#CategoryAdd
@admin.route('/addcat',methods=['GET','POST'])    
def addcat():
    catList = Category.query.filter_by(ParentCategoryId=0).all()
    
    if request.method=='POST':
     newcat = Category.query.filter_by(Name=request.form['Name'] ).first()
     if newcat is None: 
      parentCategoryId=request.form['ParentCategoryId']
      name=request.form['Name']
      cat=Category(ParentCategoryId=parentCategoryId,Name=name)
      db.session.add(cat)     
      db.session.commit()
      return redirect(url_for('admin.categorylist'))
     else:
      flash('Kateqoriya movcuddur')
      return render_template('admin/addcategory.html',categoryList=catList)
    if request.method=='GET':
      return render_template('admin/addcategory.html',categoryList=catList)
#CategoryDelete
@admin.route('/delcat/<id>')    
def delcat(id):
    cat=Category.query.filter_by(Id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('admin.categorylist'))
#CategoryEdit
@admin.route('/editcat/<id>',methods=['GET','POST'])  
def editcat(id):
 cat=Category.query.get(id)
 catlist = Category.query.filter_by(ParentCategoryId=0).all()
 if request.form:
    newparentid=request.form['ParentCategoryId'] 
    newname=request.form['Name']
    cat.ParentCategoryId=newparentid
    cat.Name=newname
    db.session.commit()
    return redirect (url_for('admin.categorylist'))
 return render_template('admin/editcategory.html',currentcat=cat,catl=catlist)


#ProductAdd
@admin.route('/addpr',methods=['GET','POST'])    
def addpr():
    products = Products.query.all()
    sizes=Size.query.all()
    colors=Color.query.all()
    shops=Shop.query.all()
    catlist=Category.query.all()
    if request.method=='POST':   
      categoryId=int(request.form['CategoryId'])
      
      
      name=request.form['Name']
      count=request.form['Count']
      price=float(request.form['Price'])
      shopId=int(request.form['ShopId'])
      description=request.form['Description']
      mainimage=request.files['MainImage']
      Status=0
      
         
      if mainimage.filename=='':
          flash("no selected file")
          return redirect(url_for('admin.addpr'))
      
      if allowed_file(mainimage.filename):
    
        mainfilename=get_random_string(8)+secure_filename(mainimage.filename)
        mainimage.save(os.path.join('ecommerce\\assets',app.config['UPLOAD_FOLDER'],mainfilename))
      else:
            return "oneerror" 
      product=Products(Name=name,Count=count,CategoryId=categoryId,MainImage=mainfilename,Price=price,ShopId=shopId,Description=description,Status=Status)
      selectedproductobj=product
      selectedcolor = request.form.getlist('color[]')
      selectedsize= request.form.getlist('size[]')
      files = request.files.getlist('photo[]')
      if len(files) == 0:
        flash("No selected file !")
        return redirect(url_for('admin.addpr'))
      db.session.add(product)   
      for color in selectedcolor:
        selectedcolor1=Color.query.filter_by(Id=color).first()
        selectedcolor1.cproduct.append(selectedproductobj)
      for size in selectedsize:
         selectedsize1=Size.query.filter_by(Id=size).first()
         selectedsize1.sproduct.append(selectedproductobj)
      # mainimage=request.files['MainImage']
      # if mainimage.filename=='':
      #     flash("no selected file")
      #     return redirect(url_for('admin.addpr'))
      
      # if allowed_file(mainimage.filename):
    
      #   mainfilename=get_random_string(8)+secure_filename(mainimage.filename)
      #   mainimage.save(os.path.join('ecommerce\\assets',app.config['UPLOAD_FOLDER'],mainfilename))
      #   newMainImage = ProductMainImage(MainImage = mainfilename,mainimages = product)
      #   db.session.add(newMainImage)
      # else:
      #       return "oneerror" 
      for image in files:
       if allowed_file(image.filename):
        filename = get_random_string(8) + secure_filename(image.filename)

        image.save(os.path.join('ecommerce\\assets', app.config['UPLOAD_FOLDER'], filename))

        newPhoto = ProductImage(Image = filename,iproduct = product)
        db.session.add(newPhoto) 
       else:
        flash("Non allowed file format")
        return "multipleerror"
      

      db.session.commit()

      return redirect(url_for('admin.listp'))
    if request.method=='GET':
      return render_template('admin/addproduct.html',categorylist=catlist,sizelist=sizes,colorlist=colors,shoplist=shops)


#ProductList
@admin.route('/listp')
def listp():
    products = Products.query.filter_by(Status=0).all()
    return render_template("admin/productlist.html", allpr = products)
#Productdelete
@admin.route('/deletep/<int:id>', methods = ['GET'])
def deletep(id):
    selectedpr = Products.query.get(id)
    selectedpr.cproduct = [1]
    selectedpr.sproduct = [1]
    for image in selectedpr.images:
        image.Image=[]
        image.MainImage=[]
        db.session.delete(image)
        # os.remove(os.path.join('static', image.Image))
        # os.remove(os.path.join('static', image.MainImage))
    selectedpr.Status=1
    selectedpr.iproduct = []
    db.session.commit()
    
    
    return redirect(url_for('admin.listp'))
    #Productdelete

#Productedit
@admin.route('/editp/<int:id>', methods = ['GET','POST'])
def editp(id):
  sizes=Size.query.all()
  colors=Color.query.all()
  shops=Shop.query.all()
  catlist=Category.query.all()
  selectpr = Products.query.get(id)
  if request.method == 'POST':
        
     
      selectedpr = Products.query.get(id)
      product=selectedpr
      # selectedpr.cproduct = []
      # selectedpr.sproduct = []
      # for image in selectedpr.images:
      #   image.Image=[]
      #   image.MainImage=[]
      categoryId=int(request.form['CategoryId'])
      selectedpr.CategoryId=categoryId
      name=request.form['Name']
      selectedpr.Name=name

      count=request.form['Count']
      selectedpr.Count=count
      shopId=int(request.form['ShopId'])
      selectedpr.ShopId=shopId
      price=int(request.form['Price'])
      selectedpr.Price=price

    
      
      selectedproductobj=selectedpr
      selectedcolor = request.form.getlist('color[]')
      selectedsize= request.form.getlist('size[]')
      files = request.files.getlist('photo[]')
      if len(files) == 0:
        flash("No selected file !")
        return redirect(url_for('admin.addpr'))
      for color in selectedcolor:
        selectedcolor1=Color.query.filter_by(Id=color).first()
        selectedcolor1.cproduct.append(selectedproductobj)
      for size in selectedsize:
         selectedsize1=Size.query.filter_by(Id=size).first()
         selectedsize1.sproduct.append(selectedproductobj)
      mainimage=request.files['MainImage']
      if mainimage.filename=='':
          flash("no selected file")
          return redirect(url_for('admin.addpr'))
      if allowed_file(mainimage.filename):
    
        mainfilename=secure_filename(mainimage.filename)
        if len(files) != 0:
          for image in selectedproductobj.images:
             db.session.delete(image)
          for image in files:
           if allowed_file(image.filename):
            filename = get_random_string(8) + secure_filename(image.filename)
            mainimage.save(os.path.join('ecommerce\\assets',app.config['UPLOAD_FOLDER'],mainfilename))

            image.save(os.path.join('ecommerce\\assets', app.config['UPLOAD_FOLDER'], filename))

            newPhoto = ProductImage(Image = os.path.join(app.config['UPLOAD_FOLDER'], filename), MainImage=os.path.join(app.config['UPLOAD_FOLDER'],mainfilename),iproduct = product)
            db.session.add(newPhoto) 
           else:
            flash("Non allowed file format")
            return "multipleerror"
      else:
        return "oneerror"

      db.session.commit()
      return "nese"
  if request.method=='GET':
      return render_template('admin/editproduct.html',product=selectpr,categorylist=catlist,sizelist=sizes,colorlist=colors,shoplist=shops)
  
#ProductCatlist
@admin.route('/catproduct/<int:id>', methods = ['GET'])
def catproduct(id):
  dbproductlist=Products.query.filter_by(CategoryId=id).all()
  return render_template('admin/catproduct.html',productlist=dbproductlist)

#USerlist
@admin.route('/userlist')
def userlist():
  userlist=User.query.filter(User.UserTypeId==3, User.Id!=3).all()
  return render_template('admin/userlist.html',userlist=userlist)

#general orderlist for admin
@admin.route('/orderlist')
def orderlist():

  orderlist=Order.query.all()
  return render_template('general/orderlist.html',orderlist=orderlist)
#admin shopun statusunu aktiv edir
@admin.route('/activateshopstatus/<int:id>')
def activateshopstatus(id):
  shop=Shop.query.get(id)
  shop.Status=1
  db.session.commit()
  return redirect(url_for('admin.shoplist'))
#admin shopun statusunu deaktive edir
@admin.route('/deactivateshopstatus/<int:id>')
def deactivateshopstatus(id):
  shop=Shop.query.get(id)
  shop.Status=2
  db.session.commit()
  return redirect(url_for('admin.shoplist'))
#AddBanner
@admin.route('/addbanner',methods=['POST','GET'])    
def addbanner():
    
    
    if request.method=='POST':
      sliders=Slider.query.all()
      if sliders.count==2:
             Slider.query.delete()
     
      Text=request.form['Text']
      url=request.form['URL']
      slider1=Slider(Text=Text,URL=url)

      file = request.files['photo']
      if file.filename == '':
        flash("No selected file !")
        return redirect(url_for('index'))

      if allowed_file(file.filename):


        # sekilin adinin secure olub olmamasina baxib duzelis edir adi
        filename =get_random_string(8)+ secure_filename(file.filename)

        file.save(os.path.join('ecommerce\\assets', app.config['UPLOAD_FOLDER'], filename))
        slider1=Slider(Text=Text,URL=url,Image=filename)

        db.session.add(slider1)     
        db.session.commit()
      else:
        flash("Non allowed file format")
        return redirect(url_for('index'))
    


      
      return render_template('client/index.html')

    if request.method=='GET':
      return render_template('admin/addbanner.html')
  # "http://127.0.0.1:5000/admin/catproduct/1"

#BannerList
# @admin.route('/bannerlist')
# def bannerlist():
#     banner = Slider.query.filter_by().all()
#     return render_template("client/layout.html", allpr = banner)
#ProductDetail
@admin.route('/prodetails/<int:id>', methods = ['GET'])
def prodetails(id):
    products=Products.query.filter_by(Id=id).first()
   
    return render_template('admin/productdetail.html',product=products)
@admin.route('/generalorder')
def generalorder():
    
    order=Order.query.filter_by().all()
    
    return render_template('admin/generalorderlist.html',order=order)
#generalorderdelete
@admin.route('/generalorderdelete/<int:id>')    
def generalorderdelete(id):
    order=Order.query.filter_by(Id=id).delete()
    db.session.commit()
    return redirect(url_for('admin.generalorder'))