from flask import Flask

app = Flask(__name__,template_folder='../template',static_folder='../assets')


from app import roots
from admin import roots
from shop import roots

