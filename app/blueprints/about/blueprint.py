from flask import Blueprint, render_template

aboutpage = Blueprint('aboutpage', __name__)

@aboutpage.route('/about')
def about():
    return render_template('about.html')