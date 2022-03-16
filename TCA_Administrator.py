# -*- coding: utf-8 -*-
import sqlite3
import wx
import os, winsound 
version="1.0"
from crea_base import class_base as tb 
from popmenu import pmenu_func as tm

class TCA_admin(wx.Frame):
	def __init__(self, parent, title):
		super(TCA_admin, self).__init__(parent=parent, title=title, size=(600, 500))
		#llamo a la creación de la base de datos:
		tb.Base()
		self.version = version 
		#creo un panel.
		p1 = wx.Panel(self)
		
		#controles necesario:
		st = wx.StaticText(p1, -1, "&Administrador")
		self.cho_ops_a = ["Diego", "Libardo", "Marisol", "Peter", "Ricardo", "Roberto", "Sigifredo"]
		self.cho_a =wx.Choice(p1, -1, choices=self.cho_ops_a)
		self.Bind(wx.EVT_CHOICE, self.on_cho_a, self.cho_a)
		st1 = wx.StaticText(p1, -1, "&Teléfono integrante")
		self.text1 = wx.TextCtrl(p1, -1, "")
		st2 = wx.StaticText(p1, -1, "&Nómbre integrante")
		self.text2 = wx.TextCtrl(p1, -1, "")
		self.bt2 = wx.Button(p1, -1, "A&cciones")
		self.Bind(wx.EVT_BUTTON, self.ac_menu, self.bt2)
		self.lista = wx.ListBox(p1)
		self.lista.Disable()
		self.bt = wx.Button(p1, -1, "&Mostrar")
		self.Bind(wx.EVT_BUTTON, self.mostrar, self.bt)
		self.it_cho_a = None
		#llamamos a la creación del menu.
		tm.create_menu(self)
		self.Centre(True)
		self.Show()
		
		#métodos.
		
	def on_cho_a(self, event):
		self.it_cho_a = self.cho_a.GetStringSelection()
		print("el administrador es: {}".format(self.it_cho_a))
	def añadir_base(self, event, *args):
		if self.text1.GetValue() and self.text2.GetValue() != "" and self.it_cho_a != None:
			tb.Base.agregar(self)
		else:
			pass
	def mostrar(self, event):
		self.lista.Enable()
		self.lista.Clear()
		tb.Base.mostrar(self)
	
	def contar(self, event):
		tb.Base.contar(self)
	
	
	def añadir_falta(self, event):
		if self.text1.GetValue() and self.it_cho_a != None:
			tb.Base.faltas(self)
			
		else:
			pass

		
	#método para el poppup 
	def ac_menu(self, event):
		ps = self.bt2.GetPosition()
		self.PopupMenu(self.p_menu, ps)
		print("en ps hay: ", ps)

		
if __name__ == "__main__":
	root= wx.App()
	TCA_admin(None, "TCA Administrador de Grupos {} Beta02".format(version))
	root.MainLoop()