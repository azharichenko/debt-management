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


@app.route('/')
def index():
    if session['user_info'] is None:
        session['user_info'] = {'user': {}, 'lines': []}
    return render_template("home.html")


@app.route('/setup', methods=('GET', 'POST'))
def collect_basic_data():
    form = UserForm()
    if form.validate_on_submit():
        session['user_info']['user'] = {'net_income': int(form.net_income.data)}
        pprint(session)

        return redirect(url_for('collect_debt_data'))
    return render_template("userform.html", form=form)


@app.route('/data', methods=('GET', 'POST'))
def collect_debt_data():
    print("think")
    print(len(session['user_info']['lines']))
    pprint(session)
    if len(session['user_info']['lines']) == 0:
        return render_template("debtstart.html")
    return render_template("debt.html")


@app.route('/credit', methods=('GET', 'POST'))
def collect_credit_card():
    form = CreditCardForm()
    if form.validate_on_submit():
        session['user_info']['lines'].append(
            {
                'name': form.name.data,
                'interest_rate': form.interest_rate.data,
                'compound_rate': form.compound_type.data,
                "balance": form.balance.data,
                "min_payment": form.min_payment.data,
                'deferment': False,
                'deferment_end': None
            }
        )
        pprint(session)
        return redirect('/data')
    return render_template("creditform.html", form=form)


@app.route('/loan', methods=('GET', 'POST'))
def collect_loan():
    form = LoanForm()
    if form.validate_on_submit():
        session['user_info']['lines'].append(
            {
                'name': form.name.data,
                'term': form.term_length.data,
                'interest_rate': form.interest_rate.data,
                'compound_rate': form.compound_type.data,
                "balance": form.balance.data,
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
    return render_template("final.html")
