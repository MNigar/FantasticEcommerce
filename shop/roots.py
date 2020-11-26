from app import app
from flask import Flask,render_template,url_for,request

@app.route('/shopindex')
def shopindex():
     return render_template('shop/index.html')

@app.route('/insertproduct')
def insertproduct():
     return render_template('shop/insertproduct.html')