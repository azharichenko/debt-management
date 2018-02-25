from flask import (
    Flask,
    render_template,
    session,
    redirect
)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalField
)
from wtforms.validators import (
    DataRequired,
    NumberRange,
    Optional
)

app = Flask(__name__)
Bootstrap(app)

app.secret_key = "super secret don't tell"

class UserForm(FlaskForm):
    net_income = DecimalField(
                "Net Income: ", 
                validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    # Currently not being implemented
    savings = DecimalField(
                "Current Total Savings: ",
                validators=[Optional] #, NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    savings_goal = DecimalField(
                "Savings Goal: ",
                validators=[Optional] #, NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )

class CreditCardForm(FlaskForm):
    pass

class LoanForm(FlaskForm):
    pass





@app.route('/')
def index():
    session['user_info'] = {'user':{}, 'lines': []}
    return render_template("home.html")

@app.route('/setup', methods=('GET', 'POST'))
def collect_basic_data():
    form = UserForm()
    if form.validate_on_submit():
        return redirect('/data')
    return render_template("userform.html", form=form)

@app.route('/data', methods=('GET', 'POST'))
def collect_debt_data():
    if len(session['user_info']['lines']) == 0:
        return render_template("debtstart.html")
    return render_template("debt.html")

@app.route('/final')
def strategy():
    return render_template("final.html") 
