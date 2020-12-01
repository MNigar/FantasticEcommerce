from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect
from datetime import datetime

from werkzeug.utils import secure_filename
import os
import random
import string

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def adminindex():
     return render_template('admin/index.html')

@app.route('/plist')
def plist():
     return render_template('admin/ecommerce-product-list.html')
#ShopList
@app.route('/shoplist')
def shoplist():
    shoplist=Shop.query.filter_by(Status=0).all()
    return render_template('admin/shoplist.html',shoplist=shoplist)
#ShopDelete
@app.route('/shopdelete/<int:id>')
def shopdelete(id):
    shopdelete=Shop.query.filter_by(Id=id).first()
    shopdelete.Status=1

    db.session.commit()    
    return redirect(url_for('shoplist'))
  
    
#userlist
@app.route('/userlist')
def userlist():
  return render_template('admin/userlist.html')
@app.route('/orderlist')
def orderlist():
     return render_template('admin/orderlist.html')
#Categorylist
@app.route('/catlist')
def categorylist():
    
    cat=Category.query.all()

    return render_template('admin/categorylist.html',category=cat)
#CategoryAdd
@app.route('/addcat',methods=['GET','POST'])    
def addcat():
    catlist = Category.query.filter_by(ParentCategoryId=0).all()
    
    if request.method=='POST':
     newcat = Category.query.filter_by(Name=request.form['Name'] ).first()
     if newcat is None: 
      parentCategoryId=request.form['ParentCategoryId']
      name=request.form['Name']
      cat=Category(ParentCategoryId=parentCategoryId,Name=name)
      db.session.add(cat)     
      db.session.commit()
      return redirect(url_for('categorylist'))
     else:
      flash('Kateqoriya movcuddur')
      return render_template('admin/addcategory.html',categorylist=catlist)
    if request.method=='GET':
      return render_template('admin/addcategory.html',categorylist=catlist)
#CategoryDelete
@app.route('/delcat/<id>')    
def delcat(id):
    cat=Category.query.filter_by(Id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('categorylist'))
#CategoryEdit
@app.route('/editcat/<id>',methods=['GET','POST'])  
def editcat(id):
 cat=Category.query.get(id)
 catlist = Category.query.filter_by(ParentCategoryId=0).all()
 if request.form:
    newparentid=request.form['ParentCategoryId'] 
    newname=request.form['Name']
    cat.ParentCategoryId=newparentid
    cat.Name=newname
    db.session.commit()
    return redirect (url_for('categorylist'))
 return render_template('admin/editcategory.html',currentcat=cat,catl=catlist)



#ProductAdd
@app.route('/addpr',methods=['GET','POST'])    
def addpr():
    products = Products.query.all()
    sizes=Size.query.all()
    colors=Color.query.all()
    shops=Shop.query.all()
    catlist=Category.query.all()
    if request.method=='POST':   
      categoryId=request.form['CategoryId']
      name=request.form['Name']
      count=request.form['Count']
      price=int(request.form['Price'])
      shopId=request.form['ShopId']
      product=Products(Name=name,Count=count,CategoryId=categoryId,Price=price,ShopId=shopId)
      selectedproductobj=product
      selectedcolor = request.form.getlist('color[]')
      selectedsize= request.form.getlist('size[]')
      files = request.files.getlist('photo[]')
      if len(files) == 0:
        flash("No selected file !")
        return redirect(url_for('addpr'))
      db.session.add(product)   
      for color in selectedcolor:
        selectedcolor1=Color.query.filter_by(Id=color).first()
        selectedcolor1.cproduct.append(selectedproductobj)
      for size in selectedsize:
         selectedsize1=Size.query.filter_by(Id=size).first()
         selectedsize1.sproduct.append(selectedproductobj)
      mainimage=request.files['MainImage']
      if mainimage.filename=='':
          flash("no selected file")
          return redirect(url_for('addpr'))
      if allowed_file(mainimage.filename):
    
        mainfilename=secure_filename(mainimage.filename)
     
        for image in files:
          if allowed_file(image.filename):
            filename = get_random_string(8) + secure_filename(image.filename)
            mainimage.save(os.path.join('ecommerce\\assets',app.config['UPLOAD_FOLDER'],mainfilename))

            image.save(os.path.join('ecommerce\\assets', app.config['UPLOAD_FOLDER'], filename))

            newPhoto = ProductImage(Image = filename, MainImage=os.path.join(app.config['UPLOAD_FOLDER'],mainfilename),iproduct = product)
            db.session.add(newPhoto) 
          else:
            flash("Non allowed file format")
            return "multipleerror"
      else:
        return "oneerror"

      db.session.commit()

      return redirect(url_for('listp'))
    if request.method=='GET':
      return render_template('admin/addproduct.html',categorylist=catlist,sizelist=sizes,colorlist=colors,shoplist=shops)


#ProductList
@app.route('/listp')
def listp():
    products = Products.query.all()
    return render_template("admin/productlist.html", allpr = products)
#Productdelete
@app.route('/deletep/<int:id>', methods = ['GET'])
def deletep(id):
    selectedpr = Products.query.get(id)
    selectedpr.cproduct = []
    selectedpr.sproduct = []
    for image in selectedpr.images:
        image.Image=[]
        image.MainImage=[]
        db.session.delete(image)
        # os.remove(os.path.join('static', image.Image))
        # os.remove(os.path.join('static', image.MainImage))

    selectedpr.iproduct = []
    db.session.commit()
    db.session.delete(selectedpr)
    db.session.commit()
    return redirect(url_for('listp'))
    #Productdelete

#Productedit
@app.route('/editp/<int:id>', methods = ['GET','POST'])
def editp(id):
  sizes=Size.query.all()
  colors=Color.query.all()
  shops=Shop.query.all()
  catlist=Category.query.all()
  selectpr = Products.query.get(id)
  if request.method == 'POST':
        
     
      selectedpr = Products.query.get(id)
      selectedpr.cproduct = []
      selectedpr.sproduct = []
      for image in selectedpr.images:
        image.Image=[]
        image.MainImage=[]
      categoryId=request.form['CategoryId']
      selectedpr.CategoryId=categoryId
      name=request.form['Name']
      selectedpr.Name=name

      count=request.form['Count']
      selectedpr.Count=count
      shopId=request.form['ShopId']
      selectedpr.ShopId=shopId
      price=int(request.form['Price'])
      selectedpr.Price=price

    
      
      selectedproductobj=selectedpr
      selectedcolor = request.form.getlist('color[]')
      selectedsize= request.form.getlist('size[]')
      files = request.files.getlist('photo[]')
      if len(files) == 0:
        flash("No selected file !")
        return redirect(url_for('addpr'))
      for color in selectedcolor:
        selectedcolor1=Color.query.filter_by(Id=color).first()
        selectedcolor1.cproduct.append(selectedproductobj)
      for size in selectedsize:
         selectedsize1=Size.query.filter_by(Id=size).first()
         selectedsize1.sproduct.append(selectedproductobj)
      mainimage=request.files['MainImage']
      if mainimage.filename=='':
          flash("no selected file")
          return redirect(url_for('addpr'))
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
  if request.method=='GET':
      return render_template('admin/editproduct.html',product=selectpr,categorylist=catlist,sizelist=sizes,colorlist=colors,shoplist=shops)

#ProductCatlist
@app.route('/catproduct/<int:id>', methods = ['GET'])
def catproduct(id):
  dbproductlist=Products.query.filter_by(CategoryId=id).all()
  return render_template('admin/catproduct.html',productlist=dbproductlist)

#ProductDetail
@app.route('/prodetails/<int:id>', methods = ['GET'])
def prodetails(id):
    products=Products.query.filter_by(Id=id).first()
    if request.method == 'POST':
      categoryId=request.form['CategoryId']
      name=request.form['Name']
      count=request.form['Count']
      price=int(request.form['Price'])
      shopId=request.form['ShopId']
      SizeId=request.form['size[]']
      ColorId=request.form['color[]']
      productorder=Products(Name=name,Count=count,CategoryId=categoryId,Price=price,ShopId=shopId)
      # return render_template('admin/order.html',order=productorder,SizeId=SizeId,ColorId=ColorId,ProductId=products.Id)
      return render_template('admin/order.html',order=productorder,SizeId=SizeId,ColorId=ColorId,ProductId=products.Id)

    else:
     return render_template('admin/productdetail.html',product=products)

#Order
@app.route('/order/<int:productid>', methods = ['GET','POST'])
def order(productid):
    product=Products.query.filter_by(Id=productid).first()

    if request.method == 'POST':
      UserId=1
      ProductId=product.id
      categoryId=request.form['CategoryId']
      count=request.form['Count']
      price=int(request.form['Price'])
      shopId=request.form['ShopId']
      SizeId=request.form['SizeId']
      ColorId=request.form['ColorId']
      Status=0
      CreateDate=datetime.now()
      Total=price
      Address=request.form['Address']
      Phone=request.form['Phone']
      
      order=Order(ProductId=ProductId,UserId=UserId,CategoryId=categoryId,Count=count,Price=price,ShopId=shopId,SizeId=SizeId,ColorId=ColorId,Status=Status,CreateDate=CreateDate,Address=Address,Total=Total,Phone=Phone)
      return "Success"
    if request.method == 'GET':
      return render_template('admin/order.html',product=product)

  

