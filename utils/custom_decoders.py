


def Decode_Unity_Cookies(cookie):
    dict = {''.join(x[0:x.find('=')]): ''.join(x[x.find('=') + 1:len(x)]) for x in cookie.split(',')}
    return dict