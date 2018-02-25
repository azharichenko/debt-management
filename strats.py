from . import sum_of_monthly_payments
from . import find_ratio
from . import reach_28

def strategy(credit_lines):
	sum = sum_of_monthly_payments(credit_lines)
	ratio = find_ratio(user, sum)
	max = 0
	user_dct = {"sum_of_monthly_payments":sum,
		    "debt_ratio":ratio,
		    "max_monthly_payments":max
		    "top_3_lines":?????????
		   }
	if(ratio < 28):
		#find 3 lines of credit with highest interest rate and add to user_dct and return to prioritize
		#make an array where the question lines are
		max = reach_28(sum, ratio, user)
		return user_dct
	elif(ratio == 28):
		return user_dct		#only show user sum_of_monthly_payment and debt_ratio
	else:
		for line in credit_line:
			if "monthly_payment" in line:
            			line["monthly_payment"] = line["monthyl_payment"]/2
		sum = sum_of_monthly_payments(credit_lines)
		user_dct["sum_of_monthyl_payments"] = sum
		return user_dct		#only show user sum_of_monthly_payment and debt_ratio
