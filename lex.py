import sys
import json

args = sys.argv

if len(args) > 1:
    inp = args[1]
else:
    inp = 'in.txt'

if len(args) > 2:
    outp = open(args[2], "w")
else:
    outp = open('out.txt', "w")

with open(inp, "r") as read_file:
    st = read_file.read()

print(st)
print(len(st))

if len(args) > 3:
    inp = args[3:]
else:
    inp = ['close_bkt.json',
           'com.json',
           'id.json',
           'num.json',
           'op_eq.json',
           'op.json',
           'open_bkt.json',
           'semicolon.json',
           'str.json',
           'ws.json',
           'kw.json']

A = []
for name in inp:
    with open(name, "r") as read_file:
        A.append(json.load(read_file))


def fnd(l, a, b):
    for i in l:
        if i[0] == a and i[2] == b:
            return i[1]
    return -1


def maxString(A, st, l):
    m = 0  #
    flag = False
    curstate = A['beg']
    if curstate in A['fin']:
        flag = True
    for i in range(l, len(st)):
        if not (st[i] in A['inp']) and '?' in A['inp']:
            ch = A['inp']['?'] #
        elif not (st[i] in A['inp']):
            if A['lex'] == 'KW':
                print("not in inp")
            break
        else:
            ch = A['inp'][st[i]]
        if not curstate in A['states']:
            if A['lex'] == 'KW':
                print("not in states")
            break
        if fnd(A['f'], A['states'][curstate], ch) == -1:
            if A['lex'] == 'KW':
                print(A['states'][curstate], " ", ch, " = -1")
            break
        else:
            if A['lex'] == 'KW':
                print(A['states'][curstate], " ", ch, " ", fnd(A['f'], A['states'][curstate], ch))
            curstate = fnd(A['f'], A['states'][curstate], ch)
        if curstate in A['fin']:
            flag = True
            m = i - l + 1
    return flag, m


k = 0
while k < len(st):
    m = 0
    curlex = None
    curpr = 0
    for M in A:
        res, r = maxString(M, st, k)
        if res:
            if m < r:
                m = r
                curlex = M["lex"]
                curpr = M["pr"]
            elif m == r and curpr < M["pr"]:
                m = r
                curlex = M["lex"]
                curpr = M["pr"]
    if m > 0:
        cur_st = st[k:k + m]
        cur_st = cur_st.replace('\n', '\\n')
        cur_st = cur_st.replace('\r', '\\r')
        cur_st = cur_st.replace('\t', '\\t')
        outp.write("<" + curlex + ", " + cur_st + ">" + "\n")
        k += m
    else:
        outp.write("<error, " + st[k] + ">" + "\n")
        k += 1

outp.close()