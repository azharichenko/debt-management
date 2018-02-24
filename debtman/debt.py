from math import exp
COMPOUND_TYPE = {
    "annual": 1,
    "biannual": 2,
    "quarter": 4,
    "month": 12
    }

def debt_per_compound(balance, annual_interest, compound_rate):
    if compound_rate == "continuous":
        return (balance * exp(annual_interest * (1 / 12))) - balance
    return balance * (annual_interest / COMPOUND_TYPE[compound_rate])

def convert_dn_monthly(debt_per_comounding, compound_rate):
    if compound_rate == "continuous":
        return debt_per_compounding
    return debt_per_compounding / (12/COMPOUND_TYPE[compound_rate])
    
def sum_of_monthly_payments(lines_of_credit):
    total = 0
    for line in lines_of_credit:
        total += line["monthly_payment"]
    return total

def loan_min_payment(balance, term, monthly_debt):
    return (balance / term) + monthly_debt
