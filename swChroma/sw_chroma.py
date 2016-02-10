#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

import wx
import sys
import numpy as np
import os
import cv2
from sw_chroma_vista import VentanaPrincipal, Panel_Frame, Webcam_Frame, AgregarTexto
from sw_chroma_model import *
import threading

tamano_btn = (90, 30)  # tamano de botones

wildcardAll = "All files (*.*)|*.*"
wildcardImagen = "Imagen source (*.jpg, *.png, *.gif)|*.jpg;*.png; *.gif\
				|All files (*.*)|*.*"

wildcardVideo = "Video source (*.avi, *.mp4, *.divx, *.mov)|*.avi; *.mp4; *.divx; *.mov\
				|All files (*.*)|*.*"
currentDirectory = os.getcwd()


def cerrarTodo(self):
	sys.exit(0)

#####################################
#******Class frame_principal********#
#####################################
class WebcamFrame(Webcam_Frame):
	"""clase que contiene el panel de la webcam y su uso con chromakey"""
	def __init__(self):
		Webcam_Frame.__init__(self, None)

	def onCloseCam(self, Event):
		self.Close(True)

	def onInitCam(self):
		self.capture = cv2.VideoCapture(0)

		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)  # set Width
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)  # set Height
		self.capture.set(cv2.CAP_PROP_FPS, 15)  # set fps

		ret, frame = self.capture.read()

		(height, width) = frame.shape[:2]
		self.bmp = wx.BitmapFromBuffer(width, height, frame)
		#print "a ved -> ", self.bmp.GetSize()

		# self.capVid = cv2.VideoCapture(str(listaVids[0]))
		# retv, self.frameV = self.capVid.read()
		# self.bmpVid = wx.BitmapFromBuffer(width, height, self.frameV)

		# los siguientes codigos son para que se capture los videos framexframe
		# se toma un timer para iniciar la secuencia de frames
		fps= 12.5
		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)

		self.Bind(wx.EVT_PAINT, self.onPaint)
		self.Bind(wx.EVT_TIMER, self.onNextFrame)

	def onPaint(self, Event):
		self.dc = wx.PaintDC(self.videoPanel)
		self.dc.DrawBitmap(self.bmp, 0, 0)

	def onNextFrame(self, Event):
		ret, self.frame = self.capture.read()
		self.frame= cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		self.frame = cv2.flip(self.frame,1,self.frame)


		hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
		# toma los rangos de verdes en hsv

		bajosrb, altosrb = esVerdeoAzul().GetesVerdeoAzul()

		mask = cv2.inRange(hsv, bajosrb, altosrb)
		# para refinar la maskara se le aplica la operacion morfologica openig y creamo un kernel
		kernel = np.ones((7, 7), np.uint8)
		# refina el ruido externo a las regiones blancas correspondientes
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		mask = cv2.dilate(mask, kernel, iterations=1)
		#ret, mask = cv2.threshold(mask, 100,255, cv2.THRESH_BINARY)
		mask = cv2.GaussianBlur(mask, (7,7),0)
		#cv2.imshow('mask con opening', mask)

		#se se invierte la mascara para mostrar los verdes en negro con la aplicacion de filtros

		#se produce una segunda mascara para luego utilizarla con el fondo
		ret, mask = cv2.threshold(mask, 170,255,cv2.THRESH_BINARY)
		mask_inv = cv2.bitwise_not(mask)
		mask_inv = cv2.GaussianBlur(mask_inv, (5,5),0)
		mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_OPEN,kernel)

		if ImagenBackground().getSeleccionRb() == 0 and ImagenBackground().getIsTrue() is True:
			self.ChromaKeyBgImage(mask, mask_inv)

		elif ImagenBackground().getSeleccionRb() == 1 and ImagenBackground().getIsTrue() is True:
			capVid = cv2.VideoCapture(str(listaVids[0]))
			self.ChromaKeyBgVideo(mask, mask_inv, capVid)
			# thread = th.Thread(target=videoBg())
			# thread.start()
		else:
			self.refreshCam()

	def ChromaKeyBgImage(self, mask, mask_inv):
		bgimg = cv2.imread(str(listaImgs[0]))
		bgimg = cv2.cvtColor(bgimg, cv2.COLOR_BGR2RGB)
		size_bg = bgimg.shape[:2]
		size_ibi = mask_inv.shape[:2]

		(x,y) = size_ibi
		if size_bg != size_ibi:
			bgimg = cv2.resize(bgimg,(y,x))

		#seleccion area de interes
		roi = cv2.bitwise_and(bgimg, bgimg, mask=~mask_inv)
		#cv2.imshow('roi', roi)

		# invierte los colores de la mascara
		mask = cv2.bitwise_and(self.frame, self.frame, mask=~mask)
		# se superponen las dos capas de imagenes para mostrar el chroma

		self.frame = cv2.add(roi, mask)
		#self.ShowCk(self.frame)

		self.refreshCam()

	def ChromaKeyBgVideo(self, mask, mask_inv, capVid):
		#capVid = cv2.VideoCapture(str(listaVids[0]))
		global pos
		capVid.set(cv2.CAP_PROP_POS_FRAMES, pos)
		ret2, bgimg = capVid.read()

		size_bg = bgimg.shape[:2]
		size_ibi = mask_inv.shape[:2]

		(x,y) = size_ibi
		if size_bg != size_ibi:
			bgimg = cv2.resize(bgimg,(y,x))

		#seleccion area de interes
		roi = cv2.bitwise_and(bgimg, bgimg, mask=~mask_inv)
		#cv2.imshow('roi', roi)

		# invierte los colores de la mascara
		mask = cv2.bitwise_and(self.frame, self.frame, mask=~mask)

		# se superponen las dos capas de imagenes para mostrar el chroma
		self.frame = cv2.add(roi, mask)

		if pos >= (capVid.get(cv2.CAP_PROP_FRAME_COUNT)-3):
			print "largo? ->",capVid.get(cv2.CAP_PROP_FRAME_COUNT)
			pos = 0
		else:
			pos+=1.5
		self.refreshCam()

	def refreshCam(self):
		if EffectsCam().getIsTrueEfect() is True:
			self.frame = EffectsCam().getEfecto(self.frame)
		else:
			pass
		try:
			self.frame = EffectsCam().addTextCv2(self.frame)
			self.bmp.CopyFromBuffer(self.frame)
			self.Refresh()
		except:
			print"IOException: problems for reload imagen camera"
		#print "tipo",type(self.frame)
		dataFrame().saveFrame(self.frame)


	def onStartStopCam(self, Event):
		if self.btnStartCamera.GetLabel() == "play":
			self.btnStartCamera.SetLabel("Stop")
			self.onInitCam()
		else:
			self.btnStartCamera.SetLabel("play")
			self.timer.Stop()  # para el timer
			self.capture.release()  # para la capturaṕara que pueda ser leida nuevamente

	def onInitAddBg(self, Event):
		if self.addBg.GetLabel()=="Fondo Chroma":
			if len(listaImgs) != 0 or len(listaVids) != 0:
				self.addBg.SetLabel("Stop Chroma")
				ImagenBackground().SetIsTrue(True)
			else:
				wx.MessageBox('Ups! no hay un fondo de para agregar a la imagen \n asegurese de ingresar al menos uno a la lista', 'Info', wx.OK | wx.ICON_INFORMATION)
		else:
			self.addBg.SetLabel("Fondo Chroma")
			ImagenBackground().SetIsTrue(False)

	#efectos del comboBox de efectos
	def onEfecto(self, Event):
		self.valor = dicEffectos.keys()[dicEffectos.values().index(self.cmbSelectEffect.GetValue())]
		print "ver que secciona del diccionario ->", self.valor
		EffectsCam().SetIsTrueEfect(True)
		EffectsCam().valorEfecto(self.valor)

	def onAddText(self, Event):
		#dialogo para abrir la paleta para poner un texto
		addtxt = AgregarTexto()
		addtxt.ShowModal()
		addtxt.Destroy()

	def sendStream(self, Event):
		if self.btnStreaming.GetLabel() == "Stremear":
			self.btnStreaming.SetLabel("Stop Streaming")
			self.dataStream = threading.Thread(target=dataFrame().sendFrame)
			self.dataStream.start()
		else:
			self.btnStreaming.SetLabel("Stremear")
			#aqui se supone que debo parar el streming y elimnar los datos de buffer

#####################################
#******Class frame_principal********#
#####################################
class MainFrame_App(VentanaPrincipal):
	#constructor
	def __init__(self):
		VentanaPrincipal.__init__(self, None)
		self.panel = Panel_Frame(self)
		self.onOpenCam()


	def onOpen(self, Event):
		dirname = currentDirectory
		dlg = wx.FileDialog(None, "elegir un archivo", dirname, "", wildcardAll, wx.OPEN)
		# cuando se seleccione alguno -> ok?
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()	 # se guarda el nombre del argivo
			self.dirname = dlg.GetDirectory()	 # se guarda la ruta al directorio
			self.path = dlg.GetPath()	 # esta guarda toda la ruta completa
			print "file name -> %s \n dirname -> %s \n path -> %s" %(str(self.filename), str(self.dirname), str(self.path))
		dlg.Destroy()

	def onOpenCam(self):
		#if len(listaImgs) != 0 or len(listaVids) != 0:
		screenCam = WebcamFrame()
		screenCam.Show()
		# else:
		# 	print "agrega algun tipo de fondo"
		# 	wx.MessageBox('Ups! no has agregando un fondo de Imagen o Video', 'Info', wx.OK | wx.ICON_INFORMATION)

#Se crea la aplicación gráfica.
app = wx.App()
frame = MainFrame_App()
frame.Show()
app.MainLoop()