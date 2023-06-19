level_2=[
    'XXXXXXXXXXXXXXXXXXXXXXXXX',
    'X  P    X         X     X',
    'X XXXXX XXXXXXXXX X XXX X',
    'X X     X     T   X E X X',
    'X X XXXXX XXX XXX XXXXX X',
    'X X     X X   X X     X X',
    'X XXXXX X X X X XXXXXXX X',
    'X     X   X X X       X X',
    'X XXX X X XXX XXX XXXXX X',
    'X E X X X X             X',
    'X XXX X X XXXXXXXXXXX X X',
    'X X   X X             X X',
    'X X XXXXXXXXXXXXXXX X X X',
    'X X           T     X X X',
    'X XXXXXXXXXXXXXXXXX X X X',
    'X             E     X X X',
    'X XXXXXXXXXXXXXXXXX XXX X',
    'X           X           X',
    'X XXXXXXXXX X XXX XXXXXXX',
    'X X       X X X   X     X',
    'X X XXXXX X X XXX X XXX X',
    'X X X T X     X X   X X X',
    'X X X X X XXXXX X X X X X',
    'X XEX X   X     X X X X X',
    'X X XXXXX X XXXXX X X X X',
    'X X       X       X T X X',
    'XXXXXXXXXXXXXXXXXXXXXXXXX'

]
level_1=[
'xxxxxxxxxxxxxxxxxxxxxxxxx',
'xP xxxxxxx          xxxxx',
'x  xxxxxxx  xxxxxx  xxxxx',
'x       xx  xxxxxx  xxxxx',
'x       xx  xxx        xx',
'x  xxx  xx  xxx      T xx',
'x  xxx  xx  xx      xxxxx',
'x  xxx  xx          xxxxx',
'x  xxx        xxxx Exxxxx',
'x  xxx  xxxxxxxxxx      x',
'x         xxxxxxxxxxx  xx',
'x    T           xxxxx  x',
'xxx  xxxxxxx            x',
'xxx  xxxxxxx  x         x',
'x         xx  x      xxxx',
'xxxE                    x',
'xxx         xxxxxxxxxxxxx',
'xxx  xxxxx  xxxxxxxxxxxxx',
'xxx  xxxxx              x',
'xx   xxxxx     T        x',
'xx   xxxxxxxxxxxxx  xxxxx',
'xx   T xxxxxxxxxxx  xxxxx',
'xx          xxxx        x',
'xxxx                    x',
'xxxxxxxxxxxxxxxxxxxxxxxxx'
]
glevel=[level_1,level_2]
# print(len(level_1),len(level_1[0]))
# print(len(level_2),len(level_2[0]))
c=0
for i in level_2:
    for j in i:
        if j=='E':
            c+=1
print(c)