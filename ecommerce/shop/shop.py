from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect, Blueprint,flash,request,redirect,session,escape
from datetime import datetime

from werkzeug.utils import secure_filename
import os
import random
import string


shop=Blueprint("shop",__name__,template_folder='templates' ,static_folder='assets')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#ProductAdd
@shop.route('/addpr',methods=['GET','POST'])    
def addpr():
      
    userid=session["userid"]
    shop=Shop.query.filter_by(UserId=userid).first()
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
      shopId=shop.Id
      Status=0
      mainimage=request.files['MainImage']
      description=request.form['Description']
      
         
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


      return redirect(url_for('shop.listp'))
    if request.method=='GET':
      return render_template('shop/addproduct.html',categorylist=catlist,sizelist=sizes,colorlist=colors,shoplist=shops)
#ProductList
@shop.route('/listp')
def listp():
    userid=session["userid"]
    shop=Shop.query.filter_by(UserId=userid).first()
    products = Products.query.filter_by(ShopId=shop.Id,Status=0).all()
    return render_template("shop/productlist.html", allpr = products,shop=shop)
@shop.route('/orderl')
def orderl():
  userid=session["userid"]
  shop=Shop.query.filter_by(UserId=userid).first()
  orderlist=Order.query.filter_by(ShopId=shop.Id).all()
  return render_template('shop/orderlist.html',orderlist=orderlist)
 
# shop mehsulun statusunu aktiv edir
@shop.route('/do/<int:id>')
def do(id):
  order=Order.query.get(id)
  order.Status=1
  db.session.commit()
  return redirect(url_for('shop.orderl'))
#Prod
# uctdelete
@shop.route('/deletep/<int:id>', methods = ['GET'])
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
    
    return redirect(url_for('shop.listp'))

#ProductDetail
@shop.route('/prodetails/<int:id>', methods = ['GET'])
def prodetails(id):
    products=Products.query.filter_by(Id=id).first()
    return render_template('shop/productdetail.html',product=products)
