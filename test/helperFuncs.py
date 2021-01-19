from random import choice, randrange
from datetime import datetime
from calendar import monthrange
import re


def n_to_str(n):
    if n < 10:
        return '0'+str(n)
    else:
        return str(n)


def multiplier(i):
    return 2 if i % 2 == 0 else 1


def check_sum(s):
    digits = [int(d) for d in re.sub(r'\D', '', s)][-9:]
    if len(digits) != 9:
        return None
    even_digitsum = sum(x if x < 5 else x - 9 for x in digits[::2])
    check_digit = sum(digits, even_digitsum) % 10
    return str(10 - check_digit if check_digit else 0)


def mk_random_ssn(age_range: list=None, sex: str=None):
    """

    :param age_range: List contain [min_age, max_age]
    :param sex: str containing "M", "m", "Male", "male"  or "F", "f", "Female", "female"
    :return:
    """
    if age_range:
        min_age = age_range[0]
        max_age = age_range[1]
    else:
        min_age = 0
        max_age = 100
    acc_male, acc_female = ["M", "m", "Male", "male"], ["F", "f", "Female", "female"]
    year = datetime.now().year - randrange(min_age, max_age)
    month = randrange(1, 12)
    date = randrange(1, monthrange(year, month)[1])
    f_1 = randrange(0, 9)
    f_2 = randrange(0, 9)
    if sex in acc_male:
        f_3 = choice([1, 3, 5, 7, 9])
    elif sex in acc_female:
        f_3 = choice([0, 2, 4, 6, 8])
    else:
        f_3 = randrange(0, 9)

    s_num = str(year)+n_to_str(month)+n_to_str(date)+str(f_1)+str(f_2)+str(f_3)
    c_num = check_sum(s_num[2:])
    return s_num + c_num


for x in range(1, 4
               ):
    print(mk_random_ssn())
