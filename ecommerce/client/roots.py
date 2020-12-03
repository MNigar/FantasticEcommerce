from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect,make_response, session
from datetime import datetime

from werkzeug.utils import secure_filename
import os
import random
import string

#ProductDetail
@app.route('/prodetails/<int:id>', methods = ['GET','POST'])
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
      UserId=7
      ProductId=product.Id
      price=int(request.form['Price'])
      shopId=request.form['ShopId']
      SizeId=request.form['size']
      ColorId=request.form['color']
      count=request.form['count']
      Status=0
      CreateDate=datetime.now()
      Total=price
      Address=request.form['Address']
      Phone=request.form['Phone']
      Email=request.form['Email']
      order=Order(ProductId=ProductId,UserId=UserId,Count=count,Price=price,ShopId=shopId,SizeId=SizeId,ColorId=ColorId,Status=Status,CreateDate=CreateDate,Address=Address,Total=Total,Phone=Phone,Email=Email)
      db.session.add(order)
      db.session.commit()
      return "Success"
    if request.method == 'GET':
      return render_template('admin/order.html',product=product)

  