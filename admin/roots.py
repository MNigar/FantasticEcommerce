from app import app
from flask import Flask,render_template,url_for,request

@app.route('/admin')
def adminindex():
     return render_template('admin/index.html')

@app.route('/plist')
def plist():
     return render_template('admin/ecommerce-product-list.html')

@app.route('/shoplist')
def shoplist():
     return render_template('admin/shoplist.html')
@app.route('/userlist')
def userlist():
     return render_template('admin/userlist.html')
@app.route('/orderlist')
def orderlist():
     return render_template('admin/orderlist.html')