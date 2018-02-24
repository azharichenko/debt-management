from flask import (
    Flask,
    render_template
)
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/setup')
def collect_basic_data():
    return render_template("data.html")



@app.route('/data')
def collect_debt_data():
    if len(session['data']['lines']) == 0:
        return render_template("debtstart.html")
    return render_template("debt.html")

@app.route('/final')
def strategy():
    return render_template("final.html") 
