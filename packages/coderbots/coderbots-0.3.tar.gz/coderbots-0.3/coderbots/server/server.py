import asyncio, time, sys
from tkinter import *

## Levels may never have a newline at the start.
## ZeroDivisionError and other very fun things
class Levels:
    lvl1='''mmmmmmmmmm
ms       m
m        m
m        m
m        m
m        m
m        m
m        m
m       fm
mmmmmmmmmm'''
    lvl2='''mmmmmmmmmm
ms       m
mmmmmmmm m
m        m
m mmmmmm m
m     m  m
m       mm
m        m
m       fm
mmmmmmmmmm'''


class PlayerV1:
    def __init__(self,x,y,game,color,pid,direction):
        self.xv=0
        self.yv=0
        self.dist=0
        self.speed=20
        self.writer=None
        self.direction=direction
        self.pid=pid
        self.color=color
        self.game=game
        self.blocksize=game.blocksize
        self.id=game.canvas.create_rectangle(x*game.blocksize,y*game.blocksize,(x+1)*game.blocksize,(y+1)*game.blocksize,outline="",fill=color)
    def run(self):
        if self.xv+self.yv!=0:
            if self.dist!=0:
                self.dist-=1
                self.game.canvas.move(self.id,self.xv,self.yv)
                self.collide([self.xv,self.yv])
            else:
                self.xv=0
                self.yv=0
    def delete(self):
        self.game.canvas.delete(self.id)
    def getsolidoverlapping(self,game,bbox):
        first=game.canvas.find_overlapping(bbox[0],bbox[1],bbox[2],bbox[3])
        second=[]
        for x in first:
            if x in game.solid:
                second.append(x)
        return second
    def collide(self,lastm):
        while len(self.getsolidoverlapping(self.game,self.game.canvas.bbox(self.id)))>0:
            xm=(0 if lastm[0]==0 else abs(lastm[0])/lastm[0])*-1
            ym=(0 if lastm[1]==0 else abs(lastm[1])/lastm[1])*-1
            self.game.canvas.move(self.id,xm,ym)
    def point(self,direction):
        self.direction=direction
    def move(self,amnt,writer):
        if self.direction=="0":
            self.xv=self.speed/self.blocksize*(amnt/abs(amnt))
        elif self.direction=="1":
            self.yv=self.speed/self.blocksize*(amnt/abs(amnt))
        elif self.direction=="2":
            self.xv=self.speed/-self.blocksize*(amnt/abs(amnt))
        elif self.direction=="3":
            self.yv=self.speed/-self.blocksize*(amnt/abs(amnt))
        self.dist=self.speed*abs(amnt)
        self.writer=writer
    def changeColor(self,newcolor):
        self.game.canvas.itemconfig(self.id,fill=newcolor)


class Game:
    def __init__(self,active,blocksize):
        self.tk=Tk()
        width=self.tk.winfo_screenwidth()
        height=self.tk.winfo_screenheight()
        width-=width%blocksize
        height-=height%blocksize
        self.tk.resizable(0,0)
        self.canvas=Canvas(self.tk,width=width,height=height,background="white")
        self.canvas.pack()
        self.players={}
        self.toppid=1
        self.solid=[]
        self.startpos=[]
        self.endpos=[]
        self.blocksize=blocksize
        self.fillBlockSet(active)
        for x in range(0,int(width/blocksize)):
            self.canvas.create_line(x*blocksize,0,x*blocksize,height)
        for y in range(0,int(height/blocksize)):
            self.canvas.create_line(0,y*blocksize,width,y*blocksize)
    def setStartPos(self,x,y):
        self.startpos=[x,y]
    def setEndPos(self,x,y):
        self.endpos=[x,y]
    def fillBlockSet(self,level):
        n=len(level.split("\n")[0])
        level=level.replace("\n","")
        for ex in range(0,len(level)):
            x=ex%n
            y=(ex-x)/n
            tp=level[ex]
            if tp==" ":
                self.canvas.create_rectangle(x*self.blocksize,y*self.blocksize,(x+1)*self.blocksize,(y+1)*self.blocksize,fill="lightgreen",outline="")
            elif tp=="s":
                self.canvas.create_rectangle(x*self.blocksize,y*self.blocksize,(x+1)*self.blocksize,(y+1)*self.blocksize,fill="yellow",outline="")
                self.setStartPos(x,y)
            elif tp=="f":
                self.canvas.create_rectangle(x*self.blocksize,y*self.blocksize,(x+1)*self.blocksize,(y+1)*self.blocksize,fill="blue",outline="")
                self.setEndPos(x,y)
            elif tp=="m":
                self.solid.append(self.canvas.create_rectangle(x*self.blocksize,y*self.blocksize,(x+1)*self.blocksize,(y+1)*self.blocksize,outline="",fill="brown"))
    def run(self):
        for x in self.players.values():
            x.run()
        self.tk.update()
        self.tk.update_idletasks()
        
    def handle(self,data,writer):
        if data["EVENT"]=="login":
            writer.write(str(self.toppid).encode())
            self.players[self.toppid]=PlayerV1(self.startpos[0],self.startpos[1],self,data["color"],self.toppid,data["direction"])
            self.toppid+=1
        elif data["EVENT"]=="move":
            self.players[int(data["pid"])].move(int(data["amnt"]),writer)
        elif data["EVENT"]=="point":
            self.players[int(data["pid"])].point(data["dir"])
        elif data["EVENT"]=="chcolor":
            self.players[int(data["pid"])].changeColor(data["color"])
        elif data["EVENT"]=="check-movedone":
            if self.players[int(data["pid"])].dist==0:
                writer.write("Y".encode())
                print("Move over!")
            else:
                writer.write("N".encode())
        elif data["EVENT"]=="logoff":
            self.players[int(data["pid"])].delete()
            del self.players[int(data["pid"])]


class Server:
    def __init__(self,leveln=None,level=None,blocksize=50,host="localhost",port=8877):
        levels=[Levels.lvl1,Levels.lvl2]
        levela=""
        if level==None:
            levela=levels[leveln]
        else:
            levela=level
        self.game=Game(levela,blocksize)
        self.loop=asyncio.get_event_loop()
        self.loop.create_task(self.tktasks())
        self.coro=asyncio.start_server(self.ondatarecv,host,port)
        self.server=self.loop.run_until_complete(self.coro)
        self.loop.run_forever()
    async def ondatarecv(self,reader,writer):
        data=await reader.read(100)
        message=data.decode()
        ppt={}
        for x in message.split("\n"):
            d=x.split(": ")
            ppt[d[0]]=d[1]
        await self.handle(ppt,writer)
        await writer.drain()
        writer.close()
    async def tktasks(self):
        while 1:
            self.game.run()
            await asyncio.sleep(0.01)
    async def handle(self,data,writer):
        self.game.handle(data,writer)

print(sys.argv)
