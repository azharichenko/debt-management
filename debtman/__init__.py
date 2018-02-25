from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for
)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DecimalField,
    RadioField
)
from wtforms.validators import (
    DataRequired,
    NumberRange
)
from pprint import pprint
from debtman.strategy import  get_results

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
        "Current Total Savings: "  # ,
        # validators=[Optional]  # , NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    savings_goal = DecimalField(
        "Savings Goal: "  # ,
        # validators=[Optional]  # , NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )


class CreditCardForm(FlaskForm):
    name = StringField(
        "Enter name of bank: ",
        validators=[DataRequired()]
    )
    balance = DecimalField(
        "Enter current balance: ",
        validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    # TODO(azharichenko): divide by 100
    # Assume no zero APR yet
    interest_rate = DecimalField(
        "Enter interest rate: ",
        validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    min_payment = DecimalField(
        "Enter minimum payment: ",
        validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    compound_type = RadioField(
        "Select compound type: ",
        choices=[('annual', "Annually"), ('biannual', "Biannually"), ('quarter', "Quarterly"), ('monthly', "Monthly"),
                 ('continous', 'Continously')],
        # Excluding compounded continously
        validators=[DataRequired()]
    )


class LoanForm(FlaskForm):
    name = StringField(
        "Enter name of lender: ",
        validators=[DataRequired()]
    )
    balance = DecimalField(
        "Enter current balance: ",
        validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    # TODO(azharichenko): divide by 100
    # Assume no zero APR yet
    interest_rate = DecimalField(
        "Enter interest rate: ",
        validators=[DataRequired(), NumberRange(min=0.01, message="Please enter a value above 0.01")]
    )
    compound_type = RadioField(
        "Select compound type: ",
        choices=[('annual', "Annually"), ('biannual', "Biannually"), ('quarter', "Quarterly"), ('monthly', "Monthly"),
                 ('continous', 'Continously')],  # Excluding compounded continously
        validators=[DataRequired()]
    )
    term_length = IntegerField(
        "Enter term length (in months): ",
        validators=[DataRequired(), NumberRange(min=1, message="Please enter a value above 1")]
    )


data = {}


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/setup', methods=('GET', 'POST'))
def collect_basic_data():
    if 'csrf_token' in session:
        if session['csrf_token'] in data:
            data[session['csrf_token']] = {'user': {}, 'credit_lines': []}
    form = UserForm()
    if form.validate_on_submit():
        if session['csrf_token'] not in data:
            data[session['csrf_token']] = {'user': {}, 'credit_lines': []}
            data[session['csrf_token']]['user'] = {'net_income': int(form.net_income.data)}
        return redirect(url_for('collect_debt_data'))
    return render_template("userform.html", form=form)


@app.route('/data', methods=('GET', 'POST'))
def collect_debt_data():
    if len(data[session['csrf_token']]['credit_lines']) == 0:
        return render_template("debtstart.html")
    return render_template("debt.html")


@app.route('/credit', methods=('GET', 'POST'))
def collect_credit_card():
    form = CreditCardForm()
    if form.validate_on_submit():
        data[session['csrf_token']]['credit_lines'].append(
            {
                'name': str(form.name.data),
                'interest_rate': float(form.interest_rate.data) / 100,
                'compound_rate': str(form.compound_type.data),
                "balance": float(form.balance.data),
                "min_payment": float(form.min_payment.data),
                'deferment': False,
                'deferment_end': None
            }
        )
        return redirect('/data')
    return render_template("creditform.html", form=form)


@app.route('/loan', methods=('GET', 'POST'))
def collect_loan():
    form = LoanForm()
    if form.validate_on_submit():
        data[session['csrf_token']]['credit_lines'].append(
            {
                'name': str(form.name.data),
                'term': int(form.term_length.data),
                'interest_rate': float(form.interest_rate.data) / 100,
                'compound_rate': str(form.compound_type.data),
                "balance": float(form.balance.data),
                "monthly_payment": None,
                'deferment': False,
                'deferment_end': None
            }
        )
        pprint(session)
        return redirect('/data')
    return render_template("loanform.html", form=form)


@app.route('/final')
def strategy():
    results = get_results(data[session['csrf_token']])
    return render_template("final.html", result=results)
