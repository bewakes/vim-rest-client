import datetime


def print_date():
    print(datetime.datetime.now())


def print_input(s):
    print(s.upper())


def process_input(line, text):
    line = int(line)
    lines = text.split('\n')
    print(lines[line-1])
