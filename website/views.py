from flask import Blueprint, render_template 

views = Blueprint('views', __name__) 

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/involvement')
def get_involved():
    return render_template("involvement.html")