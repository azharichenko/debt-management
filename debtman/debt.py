from math import exp
COMPOUND_TYPE = {
    "annual": 1,
    "biannual": 2,
    "quarter": 4,
    "month": 12
    }

def debt_per_compound(balance, annual_interest, compound_rate): #finds minimum loan payment per compounding
    if compound_rate == "continuous":
        return (balance * exp(annual_interest * (1 / 12))) - balance
    return balance * (annual_interest / COMPOUND_TYPE[compound_rate])

def convert_dn_monthly(debt_per_comounding, compound_rate): #takes minimum loan payment per compounding and converts to minimum loan payment per month
    if compound_rate == "continuous":
        return debt_per_compounding
    return debt_per_compounding / (12/COMPOUND_TYPE[compound_rate])    
def sum_of_monthly_payments(credit_lines): #takes dictionary and calculates sum of the recommended monthly and min payments
    total = 0
    for line in credit_lines:
        if "min_payment" in line:
            total += line["min_payment"]
        else:
            line["monthly_payment"] = loan_min_payment(line["balance"], line["term"], convert_dn_monthly(debt_per_compound(line["balance"], line["interest_rate"], line["compound_rate"]),line["compound_rate"]))
            total += line["monthly_payment"]
    return total

def loan_min_payment(balance, term, monthly_debt): #calculates the minimum loan payment to pay it off before term ends
    return (balance / term) + monthly_debt

def find_ratio(user, sum): #needs sum monthly payments from each debt item and net_income, finds debt/income
    return sum / user["net_income"]

"""
def reach_28(): #
    ...
    while ratio < 28 || 
        if "min_payment" in line:
            ... 
        else:
            ...
"""
