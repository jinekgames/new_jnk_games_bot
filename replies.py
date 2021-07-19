import random
from time import daylight
random.seed(version=2)

import datetime

from scedullar import mmm19_scedullar


# check if txt does contain str
def _contain5(txt, str):

    iter_txt = 0
    iter_txt_new = 0
    iter_str = 0

    len_txt = len(txt)
    len_str = len(str)

    for iter_txt in range(len_txt):

        iter_txt_new = iter_txt
        iter_str = 0

        while iter_txt_new < len_txt and iter_str < len_str and txt[iter_txt_new] == str[iter_str]:
            iter_txt_new += 1
            iter_str += 1

        if iter_str == len_str:
            return True

    return False

# check if txt contains any of list strs
def contain5(txt, list):
    for str in list:
        if _contain5(txt, str):
            return True
    return False

# check if txt end woth str
def end5(txt, str):

    iter_str = len(str) - 1
    iter_txt = len(txt) - 1

    while iter_str >= 0 and iter_txt >=0:
        if txt[iter_txt] != str[iter_str]:
            return False
        iter_str -= 1
        iter_txt -= 1
    
    return True

# check if txt is str
def _i5(txt, str):
    
    iter_str = 0

    for ch in txt:
        if ch != str[iter_str]:
            return False
        iter_str += 1
    
    return True

# check if txt is any of list strs    
def i5(txt, list):
    for str in list:
        if _i5(txt, str):
            return True
    return False

# choose answer from the list
def choo5e(list):
    return list[random.randint( 0, len(list)-1 )]
            


# returns answer accornding to message
def msgProc(msg):



    # BASE ANSWERS

    if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам' ]):
        return choo5e([ 'привет', 'здарова заебал', 'как сам чел' ])

    elif end5(msg, 'да'):
        return choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова' ])

    elif end5(msg, 'нет'):
        return choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])



    # SHARAGA
        
    if i5(msg, [ 'пн', 'понедельник' ]):
        return mmm19_scedullar[0]
    if i5(msg, [ 'вт', 'вторник' ]):
        return mmm19_scedullar[1]
    if i5(msg, [ 'ср', 'среда' ]):
        return mmm19_scedullar[2]
    if i5(msg, [ 'чт', 'четверг' ]):
        return mmm19_scedullar[3]
    if i5(msg, [ 'пт', 'пятница' ]):
        return mmm19_scedullar[4]
    if i5(msg, [ 'сб', 'суббота' ]):
        return mmm19_scedullar[5]
    if i5(msg, [ 'вс', 'воскресенье' ]):
        return mmm19_scedullar[6]

    if i5(msg, [ 'сегодня' ]):
        return mmm19_scedullar[datetime.datetime.today().weekday()]
    if i5(msg, [ 'завтра' ]):
        today = datetime.date.today()
        tomorrow = datetime.date(today.year, today.month, today.day+1)
        return mmm19_scedullar[tomorrow.weekday()]
