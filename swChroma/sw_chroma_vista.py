#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

import wx
import sys
import os
#import cv2
from sw_chroma_model import *


tamano_btn = (90, 30)  # tamano de botones

wildcardImagen = "Imagen source (*.jpg, *.png, *.gif)|*.jpg;*.png; *.gif\
				|All files (*.*)|*.*"

wildcardVideo = "Video source (*.avi, *.mp4, *.divx, *.mov)|*.avi; *.mp4; *.divx; *.mov\
				|All files (*.*)|*.*"
currentDirectory = os.getcwd()

def cerrarTodo(self):
	sys.exit(0)

# def onOpenCam(Event):
# 	Event.skip()

#####################################
#******Class VentanaPrincipal*******#
###################################################################################################################
class VentanaPrincipal(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title="Ventana Principal", size=(350, 350), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		#se crea el menuBar y status bar del main frame
		self.statusbar = self.CreateStatusBar()  # barra de estado
		menubar = wx.MenuBar()  # barra de menu

		archivosMenubar = wx.Menu()  # primer menu
		editMenubar = wx.Menu()  # segundo menu
		helpMenubar = wx.Menu()  # tercer menu
		# asignar
		menubar.Append(archivosMenubar, "archivos")
		menubar.Append(editMenubar, "editar")
		menubar.Append(helpMenubar, "ayuda")


		# wx.ID_ABOUT y wx.ID_EXIT son tipos estandard incluidos en wxWidgets
		# Se aconseja usar los tipos estandard para hacer la interfaz
		# más nativa -> http://docs.wxwidgets.org/stable/wx_stdevtid.html

		# primer menu
		arch_nVentana = archivosMenubar.Append(wx.ID_NEW, "&ventana Nueva\tCtrl+N", "click para abrir una nueva ventana")
		arch_open = archivosMenubar.Append(wx.ID_OPEN, "&Abrir...\tCtrl+O ", "Click para abrir un nuevo archivo")
		arch_save = archivosMenubar.Append(wx.ID_SAVE, "&Guardar...\tCtrl+S ", "Click para abrir un nuevo archivo")
		arch_cVentana = archivosMenubar.Append(wx.ID_EXIT, "&Salir\tCtrl+Q", "salir del programa")

		# Binds
		self.Bind(wx.EVT_MENU, self.onOpenNewCam, arch_nVentana)  # nueva ventan
		self.Bind(wx.EVT_MENU, cerrarTodo, arch_cVentana)  # cerrar todo
		self.Bind(wx.EVT_MENU, self.onOpen, arch_open)  # abrir un archivo
		self.Bind(wx.EVT_MENU, self.guardarArchivo, arch_save)  # abrir un archivo

		# tercer menu
		helpMenubar.Append(wx.ID_ABOUT, "&Acerca de","informacion del programa")

		# para agregar barra de menus
		self.SetMenuBar(menubar)  # se anade la barra de menu

		#se agregan los botones a la parte de abajo
		self.m_toolBar1 = self.CreateToolBar(wx.TB_BOTTOM, wx.ID_ANY)

		# agregar boton para webcam
		# self.btn_abrirCam = wx.Button(self.m_toolBar1, wx.ID_ANY, label="webcam", size=tamano_btn)
		# self.m_toolBar1.AddControl(self.btn_abrirCam)
		# #self.Add(btn_abrirCam, pos=(5,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
		# self.btn_abrirCam.Bind(wx.EVT_BUTTON, self.onOpenCam)

		# agrega btn para cerrar programa
		self.btn_cerrarMain = wx.Button(self.m_toolBar1, wx.ID_ANY, label="cerrar", size=tamano_btn)
		self.m_toolBar1.AddControl(self.btn_cerrarMain)
		#self.sizerGrid.Add(btn_cerrarMain, pos=(5,4), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
		self.btn_cerrarMain.Bind(wx.EVT_BUTTON, cerrarTodo)

		# self.m_toolBar1.Realize()

	# def onOpenCam(self, Event):
	# 	Event.skip()

	def onOpenNewCam(self, Event):
		pass

	def onOpen(self, Event):
		Event.skip()

	def guardarArchivo(self, Event):
		Event.skip()
###################################################################################################################


#####################################
#*****Class panel of MainFrame******#
###################################################################################################################
class Panel_Frame(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)  # size=(450,350)
		#se crea un panel para agregar los distintos elementos de las ventanas
		#self.panel = wx.Panel(self)
		self.sizerGrid = wx.GridBagSizer(10,10)

		# agrega etiqueta de saludo u otra cosa
		self.txtSaludo = wx.StaticText(self, label="buenos dias buenas tardes")
		self.sizerGrid.Add(self.txtSaludo, pos=(0,0),flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)
		#se agrega una linea de separacion
		line = wx.StaticLine(self)
		self.sizerGrid.Add(line, pos=(1,0), span=(1,10),flag=wx.EXPAND | wx.BOTTOM)

	#se agregan staticText, combobox y boton para agregar fondos de tipo imagen
		#texto
		self.txtCmboImg = wx.StaticText(self, label=" select a image backgorund : ")
		self.sizerGrid.Add(self.txtCmboImg, pos=(2,0), flag=wx.TOP | wx.EXPAND, border= 5)
		#comboBox

		self.cmboBoxImg = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=listaImgs, value="elija una opcion")
		self.sizerGrid.Add(self.cmboBoxImg, pos=(3,0), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)  # ,  flag=wx.TOP| wx.EXPAND, border=10)
		self.cmboBoxImg.Bind(wx.EVT_COMBOBOX, self.selectItemImg)

		#boton
		self.btnCmboImg = wx.Button(self, label="abrir")
		self.sizerGrid.Add(self.btnCmboImg, pos=(3,2), flag=wx.TOP | wx.RIGHT, border=5)
		self.btnCmboImg.Bind(wx.EVT_BUTTON, self.onOpenImg)
		#boton up imagen bg
		# btnUpImg = wx.Button(self, label="up")
		# self.sizerGrid.Add(btnUpImg, pos=(2,8), flag=wx.TOP | wx.RIGHT, border=5)
		# btnUpImg.Bind(wx.EVT_BUTTON, self.selectItemImg)

	#se agregan staticText, combobox y boton para agregar fondos de tipo video
		#texto
		txtCmboVideo = wx.StaticText(self, label=" select a video backgorund : ")
		self.sizerGrid.Add(txtCmboVideo, pos=(4,0), flag=wx.EXPAND | wx.BOTTOM, border=5)
		#comboBox

		self.cmboBoxVideo = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=listaVids, value="elija una opcion")
		self.sizerGrid.Add(self.cmboBoxVideo, pos=(5,0), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)
		self.cmboBoxVideo.Bind(wx.EVT_COMBOBOX, self.selectItemVideo)
		#boton
		self.btnCmboVideo = wx.Button(self, label="abrir")
		self.sizerGrid.Add(self.btnCmboVideo, pos=(5,2), flag=wx.TOP | wx.RIGHT, border=5)
		self.btnCmboVideo.Bind(wx.EVT_BUTTON, self.onOpenVideo)
	# se agregan unos radioButtom para seleccionar si usamos un fondo de tipo imagen o de tipo Video
		self.radioList = ['Imagen','Video']
		self.rdBox = wx.RadioBox(self, label="Seleccione tipo BackGround", choices=self.radioList)
		# self.rdButtomImage = wx.RadioButton(self.rdBox, label="imagen")
		# self.rdButtomVideo = wx.RadioButton(self.rdBox, label="video")
		self.sizerGrid.Add(self.rdBox, pos=(6,0), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)

		self.radioListBGColor = ['Verde','Azul']
		self.rdBoxBGColor = wx.RadioBox(self, label="Seleccione Color Chroma", choices=self.radioListBGColor)
		self.sizerGrid.Add(self.rdBoxBGColor, pos=(7,0), flag= wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)
		self.rdBoxBGColor.Bind(wx.EVT_RADIOBOX, self.selectRadioBoxBGColor)

		# # agrega btn para abrir cam
		# self.btn_abrirCam = wx.Button(self, wx.ID_ANY, label="webcam", size=tamano_btn)
		# self.sizerGrid.Add(self.btn_abrirCam, pos=(5,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
		# self.btn_abrirCam.Bind(wx.EVT_BUTTON, onOpenCam)

		# # agrega btn para cerrar programa
		# self.btn_cerrarMain = wx.Button(self, wx.ID_ANY, label="cerrar", size=tamano_btn)
		# self.sizerGrid.Add(self.btn_cerrarMain, pos=(5,4), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
		# self.btn_cerrarMain.Bind(wx.EVT_BUTTON, cerrarTodo)

		#se setea el grid
		self.SetSizer(self.sizerGrid)

	#funciones
	# def openCam(self, Event):
	# 	Event.skip()

	def onOpenImg(self, Event):
		dirname = currentDirectory
		dlg = wx.FileDialog(None, "elegir un archivo", dirname, "", wildcardImagen, wx.OPEN)
		# cuando se seleccione alguno -> ok?
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()    # se guarda el nombre del archivo
			self.dirname = dlg.GetDirectory()    # se guarda la ruta al directorio
			self.path = dlg.GetPath()
			print "file name -> %s \n dirname -> %s \n path -> %s" %(str(self.filename), str(self.dirname), str(self.path))
			if self.path in listaImgs:
				wx.MessageBox('Ups! este fondo ya ah sido agregado a la lista', 'Info', wx.OK | wx.ICON_INFORMATION)
			else:
				self.addListImgBg(self.path)
		dlg.Destroy()

	def onOpenVideo(self, Event):
		dirname = currentDirectory
		dlg = wx.FileDialog(None, "elegir un archivo", dirname, "", wildcardVideo, wx.OPEN)
		# cuando se seleccione alguno -> ok?
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()    # se guarda el nombre del archivo
			self.dirname = dlg.GetDirectory()    # se guarda la ruta al directorio
			self.path = dlg.GetPath()
			print "file name -> %s \n dirname -> %s \n path -> %s" %(str(self.filename), str(self.dirname), str(self.path))
			if self.path in listaVids:
				wx.MessageBox('Ups! este fondo ya ah sido agregado a la lista', 'Info', wx.OK | wx.ICON_INFORMATION)
			else:
				self.addListVidBg(self.path)
		dlg.Destroy()

	#se agrega la direccion que contien la imagen a la lista, se setean los valores por defecto de los comboBox y se autoselecciona el item nuevo
	def addListImgBg(self, imageDir):
		print "se agregara la sigte direccion -> ", imageDir
		self.cmboBoxImg.Append(imageDir)
		setValor = self.cmboBoxImg.SetValue(imageDir)
		self.selectItemImg(setValor)

	def addListVidBg(self, videoDir):
		print "se agregara la sigte direccion -> ", videoDir
		self.cmboBoxVideo.Append(videoDir)
		setValor = self.cmboBoxVideo.SetValue(videoDir)
		self.selectItemVideo(setValor)

	#esta funcion enviara los datos a la siguiente clase
	def selectItemImg(self, Event):
		itemselecionado = self.cmboBoxImg.GetValue()
		print "el item seleccionado es -> ", itemselecionado
		ImagenBackground().selectFromListImg(itemselecionado)

	def selectItemVideo(self, Event):
		itemselecionado = self.cmboBoxVideo.GetValue()
		print "el item seleccionado es -> ", itemselecionado
		ImagenBackground().selectFromListVids(itemselecionado)

	def selectRadioBox(self, Event):
		if self.rdBox.GetSelection() == 0:
			self.esImagen = 0
		elif self.rdBox.GetSelection() == 1:
			self.esImagen = 1
		ImagenBackground().seleccionRb(self.esImagen)

	def selectRadioBoxBGColor(self, Event):
		if self.rdBoxBGColor.GetSelection() == 0:
			esVerdeoAzul().SetesVerdeoAzul(True)
		elif self.rdBoxBGColor.GetSelection() == 1:
			esVerdeoAzul().SetesVerdeoAzul(False)

###################################################################################################################


#####################################
#********Class WebCam Frame*********#
###################################################################################################################
class Webcam_Frame(VentanaPrincipal):
	"""docstring for webcam_Frame"""
	def __init__(self, parent):
		VentanaPrincipal.__init__(self, parent)  # ), title="ventana Webcam", size=(400, 400))
		self.SetSize((600,500))  # se setea un nuevo tamaño de ventana
		self.SetTitle("Ventana WebCam")  # se setea un nuevo titulo para la nueva ventana
		self.CentreOnScreen()
		#self.btn_abrirCam.Destroy()  # se elimina el boton para abrr la camara
		self.btn_cerrarMain.Destroy()  # se elimina el boton para abrr la camara

		#cob esto se cambia el texto del statusBar
		self.statusbar.SetStatusText("hola que tal")

		panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)  # panel de arriba
		panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)  # panel de abajo

		panel1.SetBackgroundColour("BLUE")
		panel2.SetBackgroundColour("RED")

		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(panel1, 2, wx.EXPAND)
		box.Add(panel2, 1, wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(box)
		#self.Layout()

		self.vBox = wx.BoxSizer(wx.VERTICAL)  # se crea un boxsizer vertical para agregar los 3 horizontales
		self.hBox1 = wx.BoxSizer(wx.HORIZONTAL)  # contiene elementos en la parte superior
		self.hBox2 = wx.BoxSizer(wx.HORIZONTAL)  # contiene elementos en la parte del medio proyeccion de la camara
		self.hBox3 = wx.BoxSizer(wx.HORIZONTAL)  # contiene elementos en la parte inferior botones

	#se agregan los elementos al Horizontal Box 1
		self.texto = wx.StaticText(panel1, label="Bien Venido al Escenario Virtual!")
		self.hBox1.Add(self.texto, 0, border=10)

	#se agregan los elementos al Horizontal Box 2 que muestra la WebCam

		self.videoPanel = wx.Panel(panel1, 1, size=(352,288))
		self.hBox2.Add(self.videoPanel, 1, flag=wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, border=10)
		self.videoPanel.SetBackgroundColour("black")

		#se crea un nuevo panel para los Botones de efectos y otras aplicaciones
		btnPanel = wx.Panel(panel1, -1)
		#self.vBoxhb2 = wx.BoxSizer(wx.VERTICAL)

		self.gbs = wx.GridBagSizer(7,2)

		#combo box que servira para seleccionar la camara que queremos ocupar
		self.gbs.Add(wx.StaticText(btnPanel, label="Elija una camara"), pos=(0,0), flag=wx.ALIGN_TOP | wx.EXPAND | wx.ALL, border=5)
		self.cmbSelectCam = wx.ComboBox(btnPanel, style=wx.CB_DROPDOWN, choices=listaCams, value="elija una opcion")
		self.gbs.Add(self.cmbSelectCam, pos=(1,0), span=(1,2), flag=wx.ALIGN_TOP | wx.EXPAND | wx.ALL, border=5)

		#combo box que servira para seleccionar los efectos
		self.gbs.Add(wx.StaticText(btnPanel, label="Elija un efecto"), pos=(2,0), flag=wx.ALIGN_TOP | wx.EXPAND | wx.ALL, border=5)
		self.cmbSelectEffect = wx.ComboBox(btnPanel, style=wx.CB_DROPDOWN, choices=sorted(dicEffectos.values()), value="elija una opcion")
		self.gbs.Add(self.cmbSelectEffect, pos=(3,0), span=(1,2), flag=wx.ALIGN_TOP | wx.EXPAND | wx.ALL, border=5)
		self.cmbSelectEffect.Bind(wx.EVT_COMBOBOX, self.onEfecto)

		#btn para agregar textos
		self.btnAddText = wx.Button(btnPanel, label="texto")
		self.gbs.Add(self.btnAddText, pos=(4,0), flag=wx.ALIGN_TOP | wx.ALL, border=1)   #
		self.btnAddText.Bind(wx.EVT_BUTTON, self.onAddText)

		self.btnParaAlgo = wx.Button(btnPanel, label="algo")
		self.gbs.Add(self.btnParaAlgo, pos=(4,1),flag=wx.ALIGN_TOP | wx.LEFT | wx.ALL, border=1)   #
		#self.btnParaAlgo.Bind(wx.EVT_BUTTON, self.onAddText)

		#sizer btnPanel
		btnPanel.SetSizer(self.gbs)

		#se agrega el bagsizer a hBox2
		self.hBox2.Add(btnPanel, 1, flag=wx.ALIGN_TOP | wx.ALL, border=10)

	#se agregan los elementos al Horizontal Box 3

		#btn Start/stop Camera
		self.btnStartCamera = wx.Button(panel1, label="play", size=tamano_btn)
		self.hBox3.Add(self.btnStartCamera, 0, wx.ALIGN_RIGHT)
		self.btnStartCamera.Bind(wx.EVT_BUTTON, self.onStartStopCam)

		#btn ADD Image/video BackGround
		self.addBg = wx.Button(panel1, label="Fondo Chroma", size=tamano_btn)
		self.hBox3.Add(self.addBg, 0, wx.ALIGN_RIGHT)
		self.addBg.Bind(wx.EVT_BUTTON, self.onInitAddBg)

		#se agregan los elementos al vertical Box
		self.vBox.Add(self.hBox1, 0)
		self.vBox.Add(self.hBox2, 0)
		self.vBox.Add(self.hBox3, 0)

		#se setea el panel1
		panel1.SetSizer(self.vBox)

	#panel 2
		self.bagSizer = wx.GridBagSizer(1,10)
		self.btnClose = wx.Button(panel2, label="cerrar")
		self.bagSizer.Add(self.btnClose, pos=(0,10), span=(1,2), flag=wx.EXPAND | wx.RIGHT, border=5)
		self.btnClose.Bind(wx.EVT_BUTTON, cerrarTodo)

		self.btnStreaming = wx.Button(panel2, label="Stremear")
		self.bagSizer.Add(self.btnStreaming, pos=(0,8), span=(1,2), flag=wx.EXPAND | wx.RIGHT, border=5)
		self.btnStreaming.Bind(wx.EVT_BUTTON, self.sendStream)
		#se setea el panel2
		panel2.SetSizer(self.bagSizer)


	############## funciones #########################
	def onInitAddBg(self, Event):
		Event.skip()
	def onCloseCam(self, Event):
		Event.skip()

	def onStartStopCam(self, Event):
		Event.skip()

	def onPaint(self, Event):
		Event.skip()

	def onNextFrame(self, Event):
		Event.skip()

	def onEfecto(self, Event):
		Event.skip()

	def onAddText(self, Event):
		Event.skip()

	def sendStream(self, Event):
		Event.skip()
###################################################################################################################

#####################################
#******Class Add Text Dialog********#
###################################################################################################################
class AgregarTexto(wx.Dialog):

	def __init__(self):
		super(AgregarTexto, self).__init__(None, -1, "Agregar Texto")
		self.SetSize((550, 250))

		# se crea una caja vertical para ir cargano los elementos
		panel = wx.Panel(self)
		self.colourData = (0,0,0)
		self.txtData = ""
		self.fontData = 1
		self.fontSize = 1
		self.fontSizeData = 1
		self.fontSizeGrosorData = 1

		vBox = wx.BoxSizer(wx.VERTICAL)

		sb = wx.StaticBox(panel, -1, label="Agregar un Texto en la Webcam")
		sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)

		# se crean diferente caja horizontales que iran en la vertical
		# Horizontal Box 1
		hBox1 = wx.BoxSizer(wx.HORIZONTAL)

		hBox1.Add(wx.StaticText(panel, -1, 'Texto : '), 0, flag=wx.CENTER)
		self.txtFromTxtctrl = wx.TextCtrl(panel, -1, value='', style=wx.MULTIPLE | wx.EXPAND)
		hBox1.Add(self.txtFromTxtctrl, -1, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
		sbs.Add(hBox1, -1, flag=wx.LEFT | wx.EXPAND | wx.ALL)

		# horzontalBox 2
		hBox2 = wx.BoxSizer(wx.HORIZONTAL)
		# hBox2.Add(wx.StaticText(panel, -1, 'color : '), 1)

		self.btnColor = wx.Button(panel, -1, label='color')
		self.btnColor.Bind(wx.EVT_BUTTON, self.elegirColor)
		hBox2.Add(self.btnColor, 0)

		# self.btnTexto = wx.Button(panel, 0, label='texto')
		# self.btnTexto.Bind(wx.EVT_BUTTON, self.onSetText)
		# hBox2.Add(self.btnTexto, 0)

		self.cmbFontText = wx.ComboBox(panel, -1, style=wx.CB_DROPDOWN, choices=sorted(dicFonts.values()), value="elija una opcion")
		self.cmbFontText.Bind(wx.EVT_COMBOBOX, self.selectFont)
		hBox2.Add(self.cmbFontText,0, flag=wx.LEFT | wx.EXPAND | wx.ALL)

		self.cmbFontSize = wx.ComboBox(panel, -1, style=wx.CB_DROPDOWN, choices=listFontSize, value="1")
		self.cmbFontSize.Bind(wx.EVT_COMBOBOX, self.selectFontSize)
		hBox2.Add(self.cmbFontSize,0, flag=wx.RIGHT | wx.EXPAND | wx.ALL)

		self.cmbFontGrosor = wx.ComboBox(panel, -1, style=wx.CB_DROPDOWN, choices=listFontSize, value="1")
		self.cmbFontGrosor.Bind(wx.EVT_COMBOBOX, self.selectFontGrosor)
		hBox2.Add(self.cmbFontGrosor,0, flag=wx.RIGHT | wx.EXPAND | wx.ALL)

		sbs.Add(hBox2, 0, wx.LEFT | wx.EXPAND)

		hBox3 = wx.BoxSizer(wx.HORIZONTAL)
		hBox3.Add(wx.StaticText(panel, -1, 'Posicion : '), 0, flag=wx.CENTER)

		sbs.Add(hBox3, 0, wx.LEFT)

		hBox4 = wx.BoxSizer(wx.HORIZONTAL)

		hBox4.Add(wx.StaticText(panel, -1, 'X : '), 0, flag=wx.CENTER)
		self.txtCtrl4PosX = wx.TextCtrl(panel, -1, value='10')
		hBox4.Add(self.txtCtrl4PosX, 0, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)

		hBox4.Add(wx.StaticText(panel, -1, 'Y : '), 0, flag=wx.CENTER)
		self.txtCtrl4PosY = wx.TextCtrl(panel, -1, value='250')
		hBox4.Add(self.txtCtrl4PosY, 0, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)

		sbs.Add(hBox4, 0, wx.LEFT)

		panel.SetSizer(sbs)
		# botones
		hBoxBotones = wx.BoxSizer(wx.HORIZONTAL)
		okButton = wx.Button(self, 0, label="ok")
		cnclButton = wx.Button(self, 0, label="close")
		hBoxBotones.Add(okButton)
		hBoxBotones.Add(cnclButton)

		# se agregan los paneles al vertical Box
		vBox.Add(panel, -1, wx.ALL | wx.EXPAND, border=10)
		vBox.Add(hBoxBotones, 0, wx.ALIGN_CENTER | wx.BOTTOM, border=10)
		self.SetSizer(vBox)

		cnclButton.Bind(wx.EVT_BUTTON, self.cerrar)
		okButton.Bind(wx.EVT_BUTTON, self.sendText)

	def elegirColor(self, Event):
		dialog = wx.ColourDialog(None)
		dialog.GetColourData().SetChooseFull(True)
		if dialog.ShowModal() == wx.ID_OK:
			self.dataColour = dialog.GetColourData()
			print 'You selected: %s\n' % str(self.dataColour.GetColour().Get())
		self.colourData = self.dataColour.GetColour().Get()
		dialog.Destroy()

	def onSetText(self, Event):
	# 	dialog = wx.FontDialog(None, wx.FontData())
	# 	if dialog.ShowModal() == wx.ID_OK:
	# 		self.dataTxt = dialog.GetFontData()
	# 		self.font = self.dataTxt.GetChosenFont()
	# 		#print "data", self.dataTxt.GetFontData()
	# 		print 'You selected: \nFontFamily: %s \nPoint: %d \naquii->: %s' % (self.font.GetFaceName(), self.font.GetPointSize(), self.font.GetStyle())
	# 	self.fontData = self.dataTxt.GetChosenFont()
	# 	dialog.Destroy()
		pass

	def selectFont(self, Event):
		self.fontData = dicFonts.keys()[dicFonts.values().index(self.cmbFontText.GetValue())]
		print "font data from comboBox ->",self.fontData

	def selectFontSize(self, Event):
		self.fontSizeData = self.cmbFontSize.GetValue()
		print "font Size data from comboBox ->",self.fontSizeData

	def selectFontGrosor(self, Event):
		self.fontSizeGrosorData = self.cmbFontGrosor.GetValue()
		print "font Size data from comboBox ->",self.fontSizeGrosorData
	#size=(352,288)
	def sendText(self, Event):
		txt = self.txtFromTxtctrl.GetValue()
		txtPosX = int(self.txtCtrl4PosX.GetValue())
		txtPosY = int(self.txtCtrl4PosY.GetValue())
		if txtPosX > 352 or txtPosY > 288:
			wx.MessageBox('Estas saliendo de los margenes correspondientes, el valor de las posiciones se deben encontrar dentro del siguiente rango\n \nX : 0 < 350 \nY : 0 < 290', 'Info', wx.OK | wx.ICON_INFORMATION)
			pos = (10,250)
		else:
			pos = (txtPosX, txtPosY)
		font = self.fontData
		color = self.colourData
		fontSize = int(self.fontSizeData)
		fontGrosor = int(self.fontSizeGrosorData)
		EffectsCam().tomaTexto(txt, color, font, fontSize, fontGrosor, pos)
		#self.Destroy()

	def cerrar(self, Event):
		self.Destroy()