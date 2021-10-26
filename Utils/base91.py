BASE91_ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'
MASK1 = 2**13 - 1
MASK2 = 2**14 - 1
MASK3 = 2**8 - 1

def b91encode(num):
    encoded = ""
    n = 0
    b = 0
    
    for digit in num.encode('latin-1'):
        b |= (digit << n)
        n += 8
        if n > 13:
            v = b & MASK1
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & MASK2
                b >>= 14
                n -= 14
            encoded += BASE91_ALPHA[v % 91] + BASE91_ALPHA[v // 91]    
    if n:
        encoded += BASE91_ALPHA[b % 91]
        if n > 7 or b > 90:
            encoded += BASE91_ALPHA[b // 91]
    return encoded

def b91decode(num):
    decoded = ""
    n = 0
    b = 0
    v = -1
    
    for digit in num:
        c = BASE91_ALPHA.index(digit)        
        if v < 0:
            v = c
        else:
            v += c * 91
            b |= (v << n)
            if (v & MASK1) > 88:
                n += 13
            else:
                n += 14
            while n > 7:
                decoded += chr(b & MASK3)
                b >>= 8
                n -= 8
            v = -1
    if v+1:
        decoded += chr((b | v << n) & MASK3)               
    return decoded

def b91check(num):
    return set(num).issubset(set(BASE91_ALPHA))

assert b91decode(b91encode(BASE91_ALPHA)) == BASE91_ALPHA