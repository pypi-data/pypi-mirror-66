
def sheet(dt, ext='txt'):
    '''
    readlines
    '''
    o = open(dt+'.'+ext, "rb")
    r = o.readlines()
    return [i.decode("utf-8").strip() for i in r]