from flask import Flask
from flaskext.markdown import Markdown

app = Flask(__name__)
md = Markdown(app,extentions = ['codehilite'])

import views

