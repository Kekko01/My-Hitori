#!/usr/bin/env python3
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
'''
print("Welcome to Hitori Configurator")
print("Select the level:")
print("1. 5*5 Easy")
print("2. 6*6 Medium")
print("3. 8*8 Hard")
print("4. 9*9 Very Hard")
print("5. 12*12 Super Hard")
print("6. 15*15 Impossible")
choose=int(input())
with open("tables/config.txt","w") as target:
    if choose==1:
        print("5easy.txt",file=target)
        print("Setted")
    elif choose==2:
        print("6medium.txt",file=target)
        print("Setted")
    elif choose==3:
        print("8hard.txt",file=target)
        print("Setted")
    elif choose==4:
        print("9veryhard.txt",file=target)
        print("Setted")
    elif choose==5:
        print("12superhard.txt",file=target)
        print("Setted")
    elif choose==6:
        print("15impossible.txt",file=target)
        print("Setted")
    else:
        print("Wrong Choice.")
