from flask import Flask

app = Flask(__name__,template_folder='../template',static_folder='../asset')


from app import roots
from admin import roots