
from string import whitespace

# ------------------------------------------------------------------------

def _common_white_prefix(lstr):
    try: first = lstr[0] 
    except: return ''
    stop = False 
    ind = -1
    while not stop:
        ind += 1
        cur = first[ind]
        if cur not in whitespace:
            break
        for s in lstr[1:]:
            if s[ind] != cur:
                stop = True 
                break
    return first[:ind]