import socket
import time
class Robot:
    def __init__(self,clonepid=0,version=1,host="localhost",port=8877):
        self.host=host
        self.port=port
        self.pid=clonepid
        self.version=1
    def _makeSocket(self):
        sckt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sckt.connect((self.host,self.port))
        return sckt
    def _processEvent(self,event,data):
        dt="EVENT: "+event
        for x,y in data.items():
            dt+="\n"+str(x)+": "+str(y)
        return dt
    def _waitUntilAckn(self,socket):
        ackn="N"
        while ackn[-1]!="Y":
            sckt=self._makeSocket()
            sckt.send(self._processEvent("check-movedone",{"pid":self.pid}).encode())
            ackn+=sckt.recv(1).decode()
            time.sleep(0.1)
    def login(self,color,direction=0):
        if self.pid==0:
            sckt=self._makeSocket()
            sckt.send(self._processEvent("login",{"pversion":self.version,"color":color,"direction":direction}).encode())
            data=sckt.recv(3)
            self.pid=int(data)
        else:
            print("Already logged on!")
    def logoff(self):
        sckt=self._makeSocket()
        sckt.send(self._processEvent("logoff",{"pid":self.pid}).encode())
    def point(self,direction):
        sckt=self._makeSocket()
        sckt.send(self._processEvent("point",{"pid":str(self.pid),"dir":str(direction)}).encode())
    def move(self,amnt):
        sckt=self._makeSocket()
        sckt.send(self._processEvent("move",{"pid":str(self.pid),"amnt":str(amnt)}).encode())
        self._waitUntilAckn(sckt)
    def chcolor(self,newcolor):
        sckt=self._makeSocket()
        sckt.send(self._processEvent("chcolor",{"pid":str(self.pid),"color":newcolor}).encode())
