
import time
import random
random.seed(version=2)

# check if txt does contain str
def _contain5(text, str):

    iter_txt = 0
    iter_txt_new = 0
    iter_str = 0

    len_txt = len(text)
    len_str = len(str)

    for iter_txt in range(len_txt):

        iter_txt_new = iter_txt
        iter_str = 0

        while iter_txt_new < len_txt and iter_str < len_str and text[iter_txt_new] == str[iter_str]:
            iter_txt_new += 1
            iter_str += 1

        if iter_str == len_str:
            return True

    return False

# check if text contains any of list strs
def contain5(text, list):
    for str in list:
        if _contain5(text, str):
            return True
    return False

# check if text ends with str
def _end5(text, str):

    iter_str = len(str) - 1
    iter_txt = len(text) - 1

    while iter_str >= 0 and iter_txt >=0:
        if text[iter_txt] != str[iter_str]:
            return False
        iter_str -= 1
        iter_txt -= 1
    
    return True

# check if text ends with any of list strs    
def end5(text, list):
    for str in list:
        if _end5(text, str):
            return True
    return False

# check if text is str
def _i5(text, str):
    
    iter_str = 0
    len_str = len(str)

    for ch in text:
        if ch != str[iter_str]:
            return False
        iter_str += 1
        if iter_str == len_str:
            return True

    if iter_str != len_str:
        return False
    
    return True

# check if text is any of list strs    
def i5(text, list):
    for str in list:
        if _i5(text, str):
            return True
    return False

# choose answer from the list
def choo5e(list):
    return list[random.randint( 0, len(list)-1 )]

# check if text ends with any of list strs    
def endswith_list(text, list):
    for str in list:
        if text.endswith(str):
            return True
    return False

layoutDic = {

    # en2ru
    'q': 'й',
    'w': 'ц',
    'e': 'у',
    'r': 'к',
    't': 'е',
    'y': 'н',
    'u': 'г',
    'i': 'ш',
    'o': 'щ',
    'p': 'з',
    '[': 'х',
    ']': 'ъ',
    'a': 'ф',
    's': 'ы',
    'd': 'в',
    'f': 'а',
    'g': 'п',
    'h': 'р',
    'j': 'о',
    'k': 'л',
    'l': 'д',
    ';': 'ж',
    '\'': 'э',
    'z': 'я',
    'x': 'ч',
    'c': 'с',
    'v': 'м',
    'b': 'и',
    'n': 'т',
    'm': 'ь',
    ',': 'б',
    '.': 'ю',
    '/': '.',
    '`': 'ё',
    '@': '"',
    '#': '№',
    '$': ';',
    '^': ':',
    '&': '?',
    '|': '/',

    # ru2en
    'й': 'q',
    'ц': 'w',
    'у': 'e',
    'к': 'r',
    'е': 't',
    'н': 'y',
    'г': 'u',
    'ш': 'i',
    'щ': 'o',
    'з': 'p',
    'х': '[',
    'ъ': ']',
    'ф': 'a',
    'ы': 's',
    'в': 'd',
    'а': 'f',
    'п': 'g',
    'р': 'h',
    'о': 'j',
    'л': 'k',
    'д': 'l',
    'ж': ';',
    'э': '\'',
    'я': 'z',
    'ч': 'x',
    'с': 'c',
    'м': 'v',
    'и': 'b',
    'т': 'n',
    'ь': 'm',
    'б': ',',
    'ю': '.',
    #'.': '/',
    'ё': '`',
    '"': '@',
    '№': '#',
    #';': '$',
    ':': '^',
    '?': '&',
    '/': '|'
}

# replace incorrect keyboard layout
def replace_layout(text):
    text1 = ''
    for c in text:
        if c in layoutDic:
            text1 += layoutDic[c]
        else:
            text1 += c
    return text1
