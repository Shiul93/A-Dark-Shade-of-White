# -*- coding: utf-8 -*-

import pygame, sys, os, math

PI=math.pi

def dist(punto1,punto2):
    return math.hypot(punto1[0]-punto2[0],punto1[1]-punto2[1])

def anguloEnRango(angulo,direccion,rango):
    firstang=normalizarAngulo(direccion-rango/2)
    secondang=normalizarAngulo(direccion+rango/2)
    return anguloEntre(angulo,firstang,secondang)

def anguloEntre(angulo,primerangulo,segundoangulo):
    if(primerangulo<segundoangulo):
        return angulo>primerangulo and angulo<segundoangulo
    else:
        return angulo>primerangulo or angulo<segundoangulo

def normalizarAngulo(angulo):
    return angulo-2*PI*int((angulo/PI))