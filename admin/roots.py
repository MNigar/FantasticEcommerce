from app import app
from flask import Flask,render_template,url_for,request

@app.route('/admin')
def adminindex():
     return render_template('admin/index.html')
    