import re
rmap = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}
vmap = {val: key for key, val in rmap.items()}

def to_roman(num):
    dlist = [int(n) for n in [str(num)[:-3], *str(num)[-3:]] if n != ''] # splits num to [thousands, hundreds, tens, ones]
    dlist = [0] * (4 - len(dlist)) + dlist
    roman = ''
    roman += vmap[1000] * dlist[0] # 3 => MMM

    for i, n in enumerate(dlist):
        l = []
        if i == 0: continue
        if n + 1 in (5, 10):
            l.append(1)
            l.append(n + 1)
            n = 0
        if n >= 5:
            l.append(5)
            n -= 5
        l += [1] * n

        roman += ''.join(vmap[e * 10 ** (3 - i)] for e in l)
    
    return roman

def from_roman(roman):
    # def basic vars
    rsum = 0
    last = 0
    # sanitize input
    roman = re.sub(r'[^'+ ''.join(rmap.keys()) + r']', '', roman.upper())
    for c in roman[::-1]:
        v = rmap[c]

        if v < last:
            rsum -= v
        else:
            rsum += v

        last = v
    return rsum