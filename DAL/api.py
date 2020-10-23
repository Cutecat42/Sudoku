import requests

from models import data

def get_level(level):
    if level == "e":
        r = requests.get('https://sudoku.com/api/getLevel/easy').json()
        data.board = r['desc'][0]
        data.solved = r['desc'][1]
        data.level = "Easy"
        data.clock = None
    if level == "m":
        r = requests.get('https://sudoku.com/api/getLevel/medium').json()
        data.board = r['desc'][0]
        data.solved = r['desc'][1]
        data.level = "Medium"
        data.clock = None
    if level == "h":
        r = requests.get('https://sudoku.com/api/getLevel/hard').json()
        data.board = r['desc'][0]
        data.solved = r['desc'][1]
        data.level = "Hard"
        data.clock = None

    return data.board, data.solved, data.level

def requesting(request):

    board = request['board']
    solved = request['solved']
    level = request['level']
    clock = request['clock']

    return board, solved, level, clock

def set_clock(clock):

    if clock == None:
        clock = "00:00:00"
    if len(clock) == 5:
        if clock == "00:00":
            clock = "00:00:00"
        else:
            clock = "00:" + clock

    clock_cut1 = slice(0,2)
    clock_cut2 = slice(3,5)
    clock_cut3 = slice(6,8)
    data.clock1 = clock[clock_cut1]
    data.clock2 = clock[clock_cut2]
    data.clock3 = clock[clock_cut3]

    return clock
