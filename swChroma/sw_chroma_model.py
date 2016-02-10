#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

import cv2
from threading import *
import numpy as np
import os
from subprocess import *
import Image
#import livestreamer
# import urllib
#import librtmp


def esvacio(cadena):
	'''
	Devuelve cierto si la cadena es vacía y falso en caso contrario.
	'''
	if cadena is None:
		return True
	try:
		if len(cadena) == 0:
			return True
	except:
		pass
	try:
		if len(str(cadena)) == 0:
			return True
	except:
		pass
	return False


listaImgs= []
listaVids= []
listaCams= ['camara1', 'camara2']
dicEffectos = {'0':'noEffects',\
				'1':'efecto1',\
				'2':'efecto2',\
				'3':'efecto3',\
				'4':'efecto4',\
				'5':'efecto5',\
				'6':'efecto6',\
				'7':'efecto7',\
				'8':'efecto8',\
				'9':'efecto9',\
				'10':'efecto10',\
				'11':'efecto11',\
				'12':'efecto12',\
				'13':'efecto13',\
				'14':'efecto14'}

dicFonts = {cv2.FONT_HERSHEY_SIMPLEX:"FONT_HERSHEY_SIMPLEX",\
			cv2.FONT_HERSHEY_PLAIN:"FONT_HERSHEY_PLAIN",\
			cv2.FONT_HERSHEY_DUPLEX:"FONT_HERSHEY_DUPLEX",\
			cv2.FONT_HERSHEY_COMPLEX:"FONT_HERSHEY_COMPLEX",\
			cv2.FONT_HERSHEY_TRIPLEX:"FONT_HERSHEY_TRIPLEX",\
			cv2.FONT_HERSHEY_COMPLEX_SMALL:"FONT_HERSHEY_COMPLEX_SMALL",\
			cv2.FONT_HERSHEY_SCRIPT_SIMPLEX:"FONT_HERSHEY_SCRIPT_SIMPLEX",\
			cv2.FONT_HERSHEY_SCRIPT_COMPLEX:"FONT_HERSHEY_SCRIPT_COMPLEX",\
			cv2.FONT_ITALIC:"FONT_ITALIC"}


listFontSize = ['1','2','3','4','5']

esImagen = 0
subir = False
condEfecto = False
pos = 0

#rango de altos y bajos de verdes
verdeoazul = True


# bajosrb=np.array([0,0,0])
# altosrb=np.array([0,0,0])

bajosVerdes = np.array([49, 50, 50], dtype=np.uint8)
altosVerdes = np.array([80, 255, 255], dtype=np.uint8)

bajosAzul = np.array([0,100,100], dtype=np.uint8)
altosAzul = np.array([20, 255, 255], dtype=np.uint8)



class esVerdeoAzul(object):
	"""docstring for esVerdeoAzul"""
	def SetesVerdeoAzul(self, valor):
		global verdeoazul
		verdeoazul = valor

	def GetesVerdeoAzul(self):
		if verdeoazul is True:
			bajos = bajosVerdes
			altos = altosVerdes

		elif verdeoazul is False:
			bajos = bajosAzul
			altos = altosAzul

		return bajos, altos


class ImagenBackground:
	#def __init__(self):
	def selectFromListImg(self, itemImg):
		print "item elegido de a lista ",itemImg
		if esvacio(listaImgs):
			listaImgs.insert(0,str(itemImg))
		else:
			if itemImg in listaImgs:
				print "ya se encuentra"
				listaImgs.remove(itemImg)
				listaImgs.insert(0,str(itemImg))
			else:
				listaImgs.insert(0,str(itemImg))
		print "-> ",listaImgs

	def selectFromListVids(self, itemVideo):
		print "item elegido de a lista ",itemVideo
		if esvacio(listaVids):
			listaVids.insert(0,str(itemVideo))
		else:
			if itemVideo in listaVids:
				print "ya se encuentra"
				listaVids.remove(itemVideo)
				listaVids.insert(0,str(itemVideo))
			else:
				listaVids.insert(0,str(itemVideo))
		print "-> ",listaVids

	def getImgBackground(self):
		return listaImgs[0]

	def getVidBackground(self):
		return listaVids[0]

	def SetIsTrue(self, var):
		global subir
		subir = var
		print "setIsTrue -> ", subir

	def getIsTrue(self):
		return subir

	def seleccionRb(self, selec):
		print "se seleccionó -> ",selec
		global esImagen
		esImagen = selec

	def getSeleccionRb(self):
		return esImagen



valor = 0
txtFromButton = ""
color = (0,0,0)
font = cv2.FONT_HERSHEY_COMPLEX
fontSize = 1
fontGrosor = 1
fontPos = (10,250)

class EffectsCam:
	"""docstring for EffectsCam"""
	#def __init__(self):
	# 	self.arg = arg
	# 	#print self.dicEffectos.get(str(self.valor))
	# 	#self.valor = 0
	# 	#self.frame4efect = 0


	def valorEfecto(self, valorEfecto):
		global valor
		valor = valorEfecto

	def getEfecto(self, frame):
		fEffect = getattr(self,dicEffectos[valor])(frame)
		return fEffect
	# def frame4Efecto(self, frame):
	# 	global frame4efect
	# 	frame4efect = frame

	def efecto1(self, frame):
		#im_gray = cv2.imread(frame4efct, cv2.IMREAD_GRAYSCALE)
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
		return im_color

	def efecto2(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_AUTUMN)
		return im_color

	def efecto3(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_BONE)
		return im_color

	def efecto4(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_WINTER)
		return im_color

	def efecto5(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_RAINBOW)
		return im_color

	def efecto6(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_OCEAN)
		return im_color

	def efecto7(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_SUMMER)
		return im_color

	def efecto8(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_SPRING)
		return im_color

	def efecto9(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_COOL)
		return im_color

	def efecto10(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_HOT)
		return im_color

	def efecto11(self, frame):
		im_color = cv2.bilateralFilter(frame, 9, 75,75)
		# toma los rangos de verdes en hsv
		return im_color

	def efecto12(self, frame):
		#im_color = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
		im_color = cv2.stylization(frame, sigma_s=60, sigma_r=0.07)
		return im_color

	def efecto13(self, frame):
		im_color = cv2.putText(frame, "8====D", (100,200), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0,0,0))
		return im_color

	def efecto14(self, frame):
		im_color = cv2.applyColorMap(frame, cv2.COLORMAP_HOT)
		return im_color

	def SetIsTrueEfect(self, var):
		global condEfecto
		condEfecto = var
		print "setIsTrue -> ", condEfecto

	def noEffects(self, frame):
		self.SetIsTrueEfect(False)

	def getIsTrueEfect(self):
		return condEfecto

	def tomaTexto(self, textofv, colorfv, fontfv, fontSizefv, fontGrosorfv, posfv):
		#global txtFromButton
		# if esvacio(texto):
		# 	self.txtFromButton = ""
		# else:
		global txtFromButton, color, font, fontSize, fontGrosor, fontPos
		txtFromButton = textofv

		# if esvacio(color):
		# 	self.color = (0,0,0)
		# else:
		color = colorfv

		# if esvacio(font):
		# 	self.font = cv2.FONT_HERSHEY_COMPLEX
		# else:
		font = fontfv
		fontSize = fontSizefv
		fontGrosor = fontGrosorfv
		fontPos = posfv
		print "texto->",txtFromButton
		print "color->",color
		print "font->", font
		print "fontSize->", fontSizefv
		print "fontGrosor->", fontGrosor
		print "fontPos->", fontPos

	def addTextCv2(self, frame):
		#self.SetIsTrueEfect(True)
		texto = cv2.putText(frame, txtFromButton, fontPos, font, fontSize, color, fontGrosor)
		return texto


#fourcc = cv2.cv.CV_FOURCC(*'XDIV')
(width,height) = (352,288)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
pathVid ='img/output2.avi'
out = cv2.VideoWriter(pathVid, fourcc, 15, (width,height))
#cmd=("avconv -i img/frames/%07d.jpg -r 10 -vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1")
cmd=("avconv -i /tmp/out.mpg -r 10 -vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1")

cmd = cmd.split()
cmd2=("avconv -y -f image2pipe -vcodec mjpeg -r 24 -i - -vcodec mpeg4 -qscale 5 -r 24 /tmp/out.mpg")
cmd2 = cmd2.split()

posCapStream = 0


class dataFrame(object):
	"""docstring for sendFrameStreaming"""
	def __init__(self):
		super(dataFrame, self).__init__()
		self.i = 0
		#self.streamToNet()

		#p = Popen(cmd, stdin=PIPE)

	def saveFrame(self, frame):
		self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		out.write(self.frame)
		# self.i=0
		# cv2.imwrite('img/frames/%07d.jpg' %self.i,self.frame)
		# self.i+=1
		Popen(cmd2,stdin=PIPE, stdout=PIPE)


		#stdin.read(self.frame)
		# im = Image.fromarray(self.frame)
		# global posCapStream
		# im.save("img/frames/%07d.jpg" %posCapStream,"RGB")
		# posCapStream+=1
		# print "i->",posCapStream
		# im.save(p.stdin,'JPEG')
		#posCapStream = self.i


		# arrayData = np.array(self.frame)
		# im = Image.fromarray(arrayData)
		# call("avconv -f video4linux2 -i %07d mycam2.mpeg") %im

	def sendFrame(self):
		#dato = posCapStream-10
		# i = posCapStream
		Call(cmd)  # %i


		# avconv -i <fuente_archivo> -vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1
		# avconv -f video4linux2 -i /dev/video0 mycam2.mpeg -vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1
		#subprocess.call("avconv","-i",saveOn,"-vcodec","libx264","-f","flv","rtmp://moises.inf.uct.cl/live/canal1")
		#subprocess.call("avconv", "-f", "video4linux2", "-i", "/dev/video0", saveOn, "-vcodec", "libx264", "-f", "flv", "rtmp://moises.inf.uct.cl/live/canal1")

		# im = Image.new("RGB",(width,height))
		# p = call(['ffmpeg','-y','-f','image2pipe','-vcodec','libx264','-f','flv','rtmp://moises.inf.uct.cl/live/canal1'], stdin=PIPE)
		# im.save(p.stdin,'mpeg')
		# p.stdin.close()



		# self.envStream = Popen(["avconv","-i",self.frame,"-vcodec","libx264","-f","flv","rtmp://moises.inf.uct.cl/live/canal1"])  # , stdout=PIPE,stderr=PIPE
		# self.envStream.wait()

		#os.popen("avconv -i saveOn vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1")
		#os.popen("avconv -f video4linux2 -i /dev/video0 img/videostream.mpeg -vcodec libx264 -f flv rtmp://moises.inf.uct.cl/live/canal1")

		# conn = librtmp.RTMP("rtmp://moises.inf.uct.cl/live/canal1", live=True)
		# conn.connect()
		# stream = conn.create_stream()
		# stream.write("img/bg.avi")

def streamToNet():

	# capToStream = cv2.VideoCapture(pathVid)

	# encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
	# imgEncode = cv2.imencode('.jpg', frame, encode_param)
	# arrayData = np.array(imgEncode)
	# strData = arrayData.tostring()

	# capToStream = cv2.VideoCapture(pathVid)
	# ret, imgframe = capToStream.read()
	# if(cv2.CAP_PROP_FRAME_COUNT)>3:
	# 	posFrame = capToStream.get(cv2.CAP_PROP_FRAME_COUNT)-3  # se usa CAP_PROP_FRAME_COUNT para tener el largo del video guardado y de ahi partir el streaming
	# else:
	# 	posFrame = capToStream.get(cv2.CAP_PROP_FRAME_COUNT)
	print cmd
	call(cmd)
	# p.stdin(imgEncode)
	# p.stdin.close()
	# capToStream.set(cv2.CAP_PROP_POS_FRAMES, posFrame)
	# while True:
	# 	#capToStream.set(cv2.CAP_PROP_POS_FRAMES, posFrame)
	# 	ret, imgframe = capToStream.read()
	# 	cv2.imshow('frame',imgframe)
	# 	#encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
	# 	#imgEncode = cv2.imencode('.jpg', frame, encode_param)
	# 	arrayData = np.array(imgframe)
	# 	im = Image.fromarray(arrayData)
	# 	# strData = arrayData.tostring()
	# 	im.save(p.stdin,'JPEG')

	# 	# encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	# 	# result, imgencode = cv2.imencode('%i.jpg'%i, frame, encode_param)
	# 	# data = numpy.array(imgencode)
	# 	# stringData = data.tostring()
	# 	# p.stdin.write(imgframe.tostring())
	# 	#posFrame+=1
	# p.stdin.close()
	# p.wait()

	# capToStream.release()