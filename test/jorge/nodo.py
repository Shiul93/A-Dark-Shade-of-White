# -*- encoding: utf-8 -*-
from auxiliares import *

class Nodo(object):
    def __init__(self,pos,padre,distancia):
        self.pos=pos
        self.padre=padre
        self.dist=distancia
        self.visitado=False
        self=pos

    def __str__(self):
        return "Nodo de : " + str(self.pos) + " padre: "+ str(self.padre) + " distancia : " + str(self.dist)

    def actualizar(self,nuevopadre,nuevadistancia):
        self.padre=nuevopadre
        self.dist=nuevadistancia

    @classmethod
    def mejor_nodo(cls,frontera,dest):
        minlength=frontera[0].dist+dist(frontera[0].pos,dest)
        minindex=0
        for i in range (0,len(frontera)):
            length=frontera[i].dist+dist(frontera[i].pos,dest)
            if length<minlength:
                minlength=length
                minindex=i
        return minindex
