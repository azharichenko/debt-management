from debtman.debt import sum_of_monthly_payments, find_ratio, reach_28


def _get_top_three(credit_lines):
    data = [(line['interest_rate'], line) for line in credit_lines]
    top_three = sorted(data, key=lambda x: x[0], reverse=True)[:3]
    return top_three


def get_results(data):
    sum = sum_of_monthly_payments(data['credit_lines'])
    ratio = find_ratio(data['user'], sum)
    max = 0
    user_dct = {"sum_of_monthly_payments": sum,
                "debt_ratio": ratio,
                "max_monthly_payments": max,
                "top_3_lines": _get_top_three(data['credit_lines'])
                }
    if ratio < 28:
        # find 3 lines of credit with highest interest rate and add to user_dct and return to prioritize
        # make an array where the question lines are
        # remember to implement deferment
        # if defered then ignore that credit line
        max = reach_28(sum, ratio, data['user'])
        return user_dct
    elif ratio == 28:
        return user_dct  # only show user sum_of_monthly_payment and debt_ratio
    else:
        for line in data['credit_lines']:
            if "monthly_payment" in line:
                line["monthly_payment"] = line["monthyl_payment"] / 2
        sum = sum_of_monthly_payments(data['credit_lines'])
        user_dct["sum_of_monthyl_payments"] = sum
        return user_dct  # only show user sum_of_monthly_payment and debt_ratio
