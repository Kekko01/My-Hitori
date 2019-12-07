#!/usr/bin/env python3
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
'''
import g2d as g2d
from boardgame import BoardGame, console_play
from boardgamegui import gui_play
from numpy import diagonal
from time import time

class Hitori(BoardGame):
    """docstring for Boardgame."""

    def __init__(self, file):
        self._start=[]

        with open(file, "r") as target:
            for line in target:
                line=line.strip()
                vector=line.split(",")
                self._start.append(vector)
        self._dimension=len(self._start[0])
        self._play=[0] * self._dimension ** 2
        self._annots=["CLEAR"]*self._dimension**2
        for i in range(self._dimension):
            for j in range(self._dimension):
                self._play[i*self._dimension+j]=self._start[i][j]
                #self._annotation.append(False)
                #self._circle.append(False)

    def play_at(self, x, y):    #annerisce il campo
        cell=self._annots[y*self._dimension+x]
        if cell=="CLEAR":
            self._annots[y*self._dimension+x]="BLACK"
        elif cell=="BLACK":
            self._annots[y*self._dimension+x]="CLEAR"

    def flag_at(self, x, y):    #cerchia il campo
        cell=self._annots[y*self._dimension+x]
        if cell=="CLEAR":
            self._annots[y*self._dimension+x]="CIRCLE"
        elif cell=="CIRCLE":
            self._annots[y*self._dimension+x]="CLEAR"

    def value_at(self,x,y):
        return self._play[y*self._dimension+x]

    def finished(self):
        #Check 2 Same Numbers
        #print("Entro nel controllo dei due numeri sulla stessa riga")

        for i in range(self._dimension):
            listrow=[]
            listrowannots=[]
            listcol=[]
            listcolannots=[]
            for j in range(self._dimension):
                listrow.append(str(self._play[i*self._dimension+j]))
                listrowannots.append(str(self._annots[i*self._dimension+j]))
                listcol.append(str(self._play[j*self._dimension+i]))
                listcolannots.append(str(self._annots[j*self._dimension+i]))

            for k in range(self._dimension):
                for x in range(k+1,self._dimension):
                    r1=listrow[k]
                    r1annots=listrowannots[k]
                    r2=listrow[x]
                    r2annots=listrowannots[x]
                    c1=listcol[k]
                    c1annots=listcolannots[k]
                    c2=listcol[x]
                    c2annots=listcolannots[x]
                    #print("Riga",r1,r2,"\nColonna",c1,c2,"\n")
                    if r1==r2 and r1annots!="BLACK" and r2annots!="BLACK":
                        #print("Controllo errato in",r1,r2)
                        return False
                    if c1==c2 and c1annots!="BLACK" and c2annots!="BLACK":
                        #print("Controllo errato in",c1,c2)
                        return False

        #Check 2 Cell Black
        #print("Entro nel controllo due celle nere affianco")
        for y in range(self._dimension):
            for x in range(self._dimension):
                if self._annots[y*self._dimension+x]=="BLACK":
                    if y - 1 >= 0 and self._annots[(y-1)*self._dimension+x]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return False
                    if x - 1 >= 0 and self._annots[y*self._dimension+(x-1)]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return False
                    if y + 1 < self._dimension and self._annots[(y+1)*self._dimension+x]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return False
                    if x + 1 < self._dimension and self._annots[y*self._dimension+(x+1)]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return False

        #Check Blank not separated
        #print("Controllo celle bianche non separate")
        cellblank=[False]*self._dimension**2
        i=0
        while self._annots[i]=="BLACK":
            i+=1
        cellblank[i]==True
        x,y=i%self._dimension,i//self._dimension
        self.countcell(cellblank,x,y)
        cellcountannots=0
        for i in self._annots:
            if i!="BLACK":
                cellcountannots+=1
        countcellblank=0
        for i in cellblank:
            if i:
                countcellblank+=1

        #print(cellcountannots,countcellblank)

        if cellcountannots!=countcellblank:
            return False
        print("FINITO")
        return True

    def countcell(self,matrix,x,y):
        if y-1>=0 and self._annots[(y-1)*self._dimension+x]!="BLACK" and not matrix[(y-1)*self._dimension+x]:
            matrix[(y-1)*self._dimension+x]=True
            self.countcell(matrix,x,y-1)
        if y+1<self._dimension and self._annots[(y+1)*self._dimension+x]!="BLACK" and not matrix[(y+1)*self._dimension+x]:
            matrix[(y+1)*self._dimension+x]=True
            self.countcell(matrix,x,y+1)
        if x-1>=0 and self._annots[y*self._dimension+(x-1)]!="BLACK" and not matrix[y*self._dimension+(x-1)]:
            matrix[y*self._dimension+(x-1)]=True
            self.countcell(matrix,x-1,y)
        if x+1<self._dimension and self._annots[y*self._dimension+(x+1)]!="BLACK" and not matrix[y*self._dimension+(x+1)]:
            matrix[y*self._dimension+(x+1)]=True
            self.countcell(matrix,x+1,y)

    def checkblack(self,x,y):
        if self._annots[y*self._dimension+x]=="BLACK":
            return True

    def checkcircle(self,x,y):
        if self._annots[y*self._dimension+x]=="CIRCLE":
            return True

    def mark(self):
        #giro=0
        whilecounter=1
        while whilecounter>0:
            whilecounter=0
            #giro+=1
            #print("Giro di mark:",giro)
            for y in range(self._dimension):
                for x in range(self._dimension):
                    if self._annots[y*self._dimension+x]=="BLACK":
                        if y - 1 >= 0 and self._annots[(y-1)*self._dimension+x]=="CLEAR":
                            self.flag_at(x,y-1)
                            whilecounter+=1
                        if x - 1 >= 0 and self._annots[y*self._dimension+(x-1)]=="CLEAR":
                            self.flag_at(x-1,y)
                            whilecounter+=1
                        if y + 1 < self._dimension and self._annots[(y+1)*self._dimension+x]=="CLEAR":
                            self.flag_at(x,y+1)
                            whilecounter+=1
                        if x + 1 < self._dimension and self._annots[y*self._dimension+(x+1)]=="CLEAR":
                            self.flag_at(x+1,y)
                            whilecounter+=1
                    if self._annots[y*self._dimension+x]=="CIRCLE":
                        #print("Entro nel controllo Circle")
                        for j in range(self._dimension):
                            if self._annots[y*self._dimension+j]=="CLEAR" and (y*self._dimension+j)!=(y*self._dimension+x) and self._play[y*self._dimension+x]==self._play[y*self._dimension+j]:
                                self.play_at(j,y)
                                whilecounter+=1
                            if self._annots[j*self._dimension+x]=="CLEAR" and (j*self._dimension+x)!=(y*self._dimension+x) and self._play[y*self._dimension+x]==self._play[j*self._dimension+x]:
                                self.play_at(x,j)
                                whilecounter+=1
                #self.checkdiagonal() Tolto perchè rallentava il tutto

    def checkdiagonal(self):
        #with open("checkdiagonal.txt","a") as target:
            #print("diagonal",file=target)
        #Diagonal Black
        #print("Entro nel checkdiagonal")
        matrixcheck=[]
        for y in range(self._dimension):
            row=[]
            for x in range(self._dimension):
                row.append(str(x)+" "+str(y))
            matrixcheck.append(row)
        for offset in range(-self._dimension+2,self._dimension-1):
            diagonalcheck=diagonal(matrixcheck,offset=offset)
            cellclear=[]
            cellblack=0
            for x in diagonalcheck:
                pos=x.split(" ")
                if not self.checkblack(int(pos[0]),int(pos[1])) and not self.checkcircle(int(pos[0]),int(pos[1])):
                    cellclear.append((int(pos[0]),int(pos[1])))
                    #print("Aggiunta cella vuota")
                    if len(cellclear)>1:
                        return
                elif self.checkblack(int(pos[0]),int(pos[1])):
                    cellblack+=1
                    #print("Aggiunta cella nera")
                elif self.checkcircle(int(pos[0]),int(pos[1])):
                    return
            if len(diagonalcheck)-cellblack==1 and len(cellclear)==1:
                x,y=cellclear[0]
                self.flag_at(x,y)
                #print("Flaggo in ",x,y)
        return

    def help(self):
        starttime=time()
        if self.wrong():
            print("Non entro nel ciclo")
            return
        #with open("test.txt","a") as target:
            #print("Entrato nel Help",file=target)
        test=0
        mosse=1
        #while mosse>0:
        giro=0
        for k in range(self._dimension**2):
            giro+=1
            #print("Giro di Help",giro)
            mosse=0
            #with open("test.txt","a") as target:
                #test+=1
                #print("Giro",test)
                #print("!!GIRO!!",test,file=target)
            for y in range(self._dimension):
                for x in range(self._dimension):
                    backup=self._annots[:]
                    if self._annots[y*self._dimension+x]=="CLEAR":
                        self.play_at(x,y)
                        self.mark()
                        if self.wrong():
                            self._annots=backup[:]
                            self.flag_at(x,y)
                        backupsquare=self._annots[:]
                        self._annots=backup[:]
                        if backupsquare==backup:
                            #with open("test.txt","a") as target:
                                #print("Nessun cambiamento marcando",file=target)
                            mosse=0
                        else:
                            #with open("test.txt","a") as target:
                                #print("cambiamento marcando",file=target)
                            mosse+=1
                        self.flag_at(x,y)
                        self.mark()
                        if self.wrong():
                            self._annots=backup[:]
                            self.play_at(x,y)
                        backupcircle=self._annots[:]
                        if backupcircle==backup:
                            #with open("test.txt","a") as target:
                                #print("Nessun cambiamento cerchiando",file=target)
                            mosse=0
                        else:
                            #with open("test.txt","a") as target:
                                #print("cambiamento cerchiando",file=target)
                            mosse+=1
                        self._annots=backup[:]
                        for i in range(self._dimension**2):
                            if backupcircle[i]==backupsquare[i]:
                                self._annots[i]=backupcircle[i]
                        if self.finished():
                            print(time()-starttime)
                            return
        return

    def wrong(self):
        #print("Wrong")

        #Check 2 Cell Black
        for y in range(self._dimension):
            for x in range(self._dimension):
                if self._annots[y*self._dimension+x]=="BLACK":
                    if y - 1 >= 0 and self._annots[(y-1)*self._dimension+x]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return True
                    if x - 1 >= 0 and self._annots[y*self._dimension+(x-1)]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return True
                    if y + 1 < self._dimension and self._annots[(y+1)*self._dimension+x]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return True
                    if x + 1 < self._dimension and self._annots[y*self._dimension+(x+1)]=="BLACK":
                        #print("Celle nere affianco",x,y)
                        return True

        #Check Blank Cell
        cellblank=[False]*self._dimension**2
        i=0
        while self._annots[i]=="BLACK":
            i+=1
        cellblank[i]==True
        x,y=i%self._dimension,i//self._dimension
        self.countcell(cellblank,x,y)
        cellcountannots=0
        for i in self._annots:
            if i!="BLACK":
                cellcountannots+=1
        countcellblank=0
        for i in cellblank:
            if i:
                countcellblank+=1

        #print(cellcountannots,countcellblank)

        if cellcountannots!=countcellblank:
            #with open("test.txt","a") as target:
                #print("Bianche non adiacenti",file=target)
            return True

        #Check 2 Same Numbers
        for i in range(self._dimension):
            listrow=[]
            listrowannots=[]
            listcol=[]
            listcolannots=[]
            for j in range(self._dimension):
                listrow.append(str(self._play[i*self._dimension+j]))
                listrowannots.append(str(self._annots[i*self._dimension+j]))
                listcol.append(str(self._play[j*self._dimension+i]))
                listcolannots.append(str(self._annots[j*self._dimension+i]))

            for k in range(self._dimension):
                for x in range(k+1,self._dimension):
                    r1=listrow[k]
                    r1annots=listrowannots[k]
                    r2=listrow[x]
                    r2annots=listrowannots[x]
                    c1=listcol[k]
                    c1annots=listcolannots[k]
                    c2=listcol[x]
                    c2annots=listcolannots[x]
                    #print("Riga",r1,r2,"\nColonna",c1,c2,"\n")
                    if r1[0]==r2[0] and r1annots=="CIRCLE" and r2annots=="CIRCLE":
                        #with open("test.txt","a") as target:
                            #print("Cerchi uguali",file=target)
                        return True
                    if c1[0]==c2[0] and c1annots=="CIRCLE" and c2annots=="CIRCLE":
                        #with open("test.txt","a") as target:
                            #print("Cerchi uguali",file=target)
                        return True

        with open("test.txt","a") as target:
            print("Va beneeee (return False wrong)",file=target)
        return False

    def cols(self):
        return self._dimension

    def rows(self):
        return self._dimension

    def message(self):
        return "Hai vinto!"

def main():
    #with open("test.txt","w") as target:
            #print(file=target)
    #with open("checkdiagonal.txt","w") as target:
            #print(file=target)
    with open("tables/config.txt") as target:
        file="tables/"+target.readline().strip()
    play=Hitori(file)
    gui_play(play)
    #console_play(play)

main()
