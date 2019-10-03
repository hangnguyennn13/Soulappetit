from flask import Flask, render_template, request
from blueprints import *
import base64
import re
app = Flask(__name__)

app.register_blueprint(homepage)
app.register_blueprint(aboutpage)
app.register_blueprint(modelpage)

if __name__ == "__main__":
    app.run(debug=True)