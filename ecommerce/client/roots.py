from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect,make_response, session,Blueprint
from datetime import datetime

from werkzeug.utils import secure_filename
import os
import random
import string
from flask_mail import Mail, Message
client=Blueprint("roots",__name__,template_folder='templates' ,static_folder='assets')

mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nigarmammadova4t@gmail.com'
app.config['MAIL_PASSWORD'] = 'jracenqhiyxfyryx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
#ProductDetail
@client.route('/prodetails/<int:id>', methods = ['GET','POST'])
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
@client.route('/order/<int:productid>', methods = ['GET','POST'])
def order(productid):
    product=Products.query.filter_by(Id=productid).first()
    
    if request.method == 'POST':
      UserId=3
      ProductId=product.Id
      price=int(request.form['Price'])
      shopId=request.form['ShopId']
      SizeId=request.form['size']
      Name=request.form['Name']
      Surname=request.form['Surname']
      ColorId=request.form['color']
      count=request.form['count']
      Status=0
      CreateDate=datetime.now()
      Total=price
      Address=request.form['Address']
      Phone=request.form['Phone']
      Email=request.form['Email']
      order=Order(ProductId=ProductId,UserId=UserId,Count=count,Price=price,ShopId=shopId,SizeId=SizeId,ColorId=ColorId,Status=Status,CreateDate=CreateDate,Address=Address,Total=Total,Phone=Phone,Email=Email,Name=Name,Surname=Surname)
      ordername=Products.query.filter_by(Id=order.ProductId).first()
      ordersize=Size.query.filter_by(Id=SizeId).first()
      ordercolor=Color.query.filter_by(Id=ColorId).first()

      db.session.add(order)
      db.session.commit()
      msg = Message('Salam', sender = 'nigarmammadova4t@gmail.com', recipients = [order.Email])
      msg.body = f'{order.Id} nömrəli sifarişiniz icra olundu. Sfiraişin detalı: Ad: {ordername.Name} Ölçü :{ordersize.Name} Rəng:{ordercolor.Name}   Qiymət:{order.Price}'   
      mail.send(msg)
      return "Success"
    if request.method == 'GET':
      return render_template('admin/order.html',product=product)

  