import locale

locale.setlocale(locale.LC_ALL, '')


def format_datetime(value, fmt='%Y년 %n월 %d일 %H:%M'):
    return value.strftime(fmt)

