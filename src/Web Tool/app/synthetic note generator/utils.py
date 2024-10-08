import datetime
import random


def get_feature_probabilities():
    probabilities = {
        'note_cosigner': 1.0,
        'problem_list': 1.0,
        'medication_list': 1.0,
        'allergies_list': 1.0,
        'ct': 1.0,
        'mri': 1.0,
        'bone_scan': 1.0,
        'alcohol_status':  [0.0, 1/3., 1/3., 1/3.],
        'smoking_status':  [0.0, 1/3., 1/3., 1/3.],
    }
    return probabilities


def random_time_period(min_period=1, max_period=2, time_period='month'):
    if time_period == 'month':
        single = 'month'
        multiple = 'months'
    elif time_period == 'week':
        single = 'week'
        multiple = 'weeks'
    elif time_period == 'year':
        single = 'year'
        multiple = 'years'
    else:
        single = ''
        multiple = ''
        assert f'Invalid time period {time_period}'

    period = random.randint(min_period, max_period)
    if period < 1:
        period = 1
    if period == 1:
        return f'{period} {single}'
    else:
        return f'{period} {multiple}'


def format_date(dt, date_format=None):
    if dt is None:
        return None
    else:
        if date_format is None:
            date_format_index = random.randint(0, 3)
        else:
            date_format_index = date_format
        if date_format_index == 0:
            return dt.strftime('%m/%d/%Y')
        elif date_format_index == 1:
            return dt.strftime('%m-%d-%Y')
        elif date_format_index == 2:
            return dt.strftime('%Y-%m-%d')
        else:
            return dt.strftime('%b %d, %Y')


def date_offset(years=0, months=0, days=0):
    return datetime.timedelta(days=years * 365 + months * 30 + days)
