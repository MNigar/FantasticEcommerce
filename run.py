from ecommerce import app,db
from ecommerce.models import *
from flask import Flask,render_template,url_for,request,redirect, Blueprint
from jinja2 import Template
@app.context_processor
def some_processor():
    def femalecat():
        catlist=Category.query.filter_by(ParentCategoryId=1).all()
        return catlist
    return {'femalecat': femalecat}
@app.context_processor
def some_processorr():
    def malecat():
        catlist=Category.query.filter_by(ParentCategoryId=2).all()
        return catlist
    return {'malecat': malecat} 
if __name__ == '__main__':    
     app.run(debug=True)
