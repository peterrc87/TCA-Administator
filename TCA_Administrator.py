# -*- coding: utf-8 -*-
import sqlite3
import wx
import os, winsound 
version="1.0"
from crea_base import class_base as tb 
from popmenu import pmenu_func as tm
from tools import tools_func as to 

class TCA_admin(wx.Frame):
	def __init__(self, parent, title):
		super(TCA_admin, self).__init__(parent=parent, title=title, size=(600, 500))
		#llamo a la creación de la base de datos:
		tb.Base()
		self.version = version 
		#creo un panel.
		p1 = wx.Panel(self)
#creo un sizer para organizar los controles.		
		gsz = wx.GridBagSizer(4, 3)
		#controles necesario:
		st = wx.StaticText(p1, -1, "&Administrador")
		self.cho_ops_a = ["Diego", "Libardo", "Marisol", "Peter", "Ricardo", "Roberto", "Sigifredo"]
		self.cho_a =wx.Choice(p1, -1, choices=self.cho_ops_a)
		self.Bind(wx.EVT_CHOICE, self.on_cho_a, self.cho_a)
		st1 = wx.StaticText(p1, -1, "&Teléfono integrante")
		self.text1 = wx.TextCtrl(p1, -1, "")
		st2 = wx.StaticText(p1, -1, "&Nómbre integrante")		
		self.text2 = wx.TextCtrl(p1, -1, "")
		self.che =wx.CheckBox(p1, -1, "Observaciones")
		self.obs = ""
		self.lista = wx.ListBox(p1)
		self.lista.Disable()
		#evento para capturar el string de la lista.
		self.Bind(wx.EVT_LISTBOX, self.on_string, self.lista)

		self.bt2 = wx.Button(p1, -1, "A&cciones")
		self.Bind(wx.EVT_BUTTON, self.ac_menu, self.bt2)
		
		self.bt = wx.Button(p1, -1, "C&onsultas")
		self.Bind(wx.EVT_BUTTON, self.ac_menu2, self.bt)
		self.it_cho_a = None
		
		#añadimos al sizer.
		gsz.Add(st, (0,0), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.cho_a, (0,1), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(st1, (1,0), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.text1, (1,1), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(st2, (2,0), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.text2, (2,1), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.che, (2,2), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.bt2, (3,1), (1,1), wx.EXPAND|wx.ALL, 10)
		gsz.Add(self.bt, (3,2), (1,1), wx.EXPAND|wx.ALL, 10)
		p1.SetSizer(gsz)
		
		#llamamos a la creación del popmenu.
		tm.create_menu(self)
		
		#llamamos a la creación del menú contexto.
		tm.context_menu(self)
		
		#llamamos a la creación de la barra de menú.
		tm.create_menubar(self)
		self.Centre(True)
		self.Show()
		
	#métodos.
	#método para capturar el string de la lista.
	def on_string(self, event):
		l_str = self.lista.GetStringSelection()
		self.it_tlf = l_str.split(" ") 	
		return self.it_tlf[1]
	def on_cho_a(self, event):
		self.it_cho_a = self.cho_a.GetStringSelection()
		print("el administrador es: {}".format(self.it_cho_a))
	def añadir_base(self, event, *args):
		if self.text1.GetValue() != "" and self.text2.GetValue() != "":
			tb.Base.agregar(self)
			self.lista.Clear()
			#self.lista.Enable()
			tb.Base.mostrar_tm(self)

		else:
			wx.MessageBox("Debe ingresar un número de teléfono, y un nombre de integrante para añadir un miembro", "Atención faltan datos")
	
	#método para mostrar miembros con faltas.
	def mostrar(self, event):
		if self.text1.GetValue() != "":			
			self.lista.Enable()
			self.lista.Clear()
			tb.Base.mostrar_f(self)
		else:
			wx.MessageBox("Debe ingresar un número de teléfono, para consultar las faltas", "Atención falta el teléfono")
	
	
	def añadir_falta(self, event):
		if self.text1.GetValue() != "" and self.it_cho_a != None:
			tb.contar_f(self)
			if self.mi == None:
				wx.MessageBox("no existe el miembro en la base de datos\n No es posible agregar faltas", "No se puede realizar la operación!")
			else:
				tb.Base.faltas(self)
		else:
			wx.MessageBox("Debe escoger un administrador, e ingresar un número de teléfono válido, para añadir una falta.",  "Atentción faltan opciones")
	
		

		
			

	#método para el poppup1 
	def ac_menu(self, event):
		
		ps = self.bt2.GetPosition()
		self.PopupMenu(self.p_menu, ps)		
		
	#popup menu para el botón 2.
	def ac_menu2(self, event):
		ps2 = self.bt.GetPosition()
		self.PopupMenu(self.p2_menu, ps2)
	
	#método para mostrar todos los miembros.
	def mostrar_tm(self, event):
		self.lista.Clear()
		self.lista.Enable()
		tb.Base.mostrar_tm(self)

	#método llamar al menú de contexto.
	def showPopupMenu(self, event):
		position = event.GetPosition()
		self.PopupMenu(self.m_context,position)

	#método para llamar a la función eliminar.
	def elimina(self, event):
		tb.Base.eliminar(self)
		self.lista.Clear()
		#self.lista.Enable()
		tb.Base.mostrar_tm(self)

	#método que llama al copiado del teléfono.
	def copiar_tlf(self, event):
		tb.Base.copyclipboard_pg(self)

	#método para llamar a la función mostrar eliminados.
	def muestra_el(self, event):
		self.lista.Clear()
		self.lista.Enable()
		tb.Base.muestra_el(self)

	#método para llamar a la función que cambia el número de teléfono.
	def edita_tlf(self, event):
		tb.Base.editar_tlf(self)
		self.lista.Clear()
		tb.Base.mostrar_tm(self)
	
	#método que llama a la función para cambiar el nombre a un miembro.
	def cambia_nombre(self, event):
		tb.Base.editar_nombre(self)
		self.lista.Clear()
		tb.Base.mostrar_tm(self)
	
	#método para llamar a la función editar observaciones.
	def edita_obs(self, event):
		tb.Base.editar_obs(self)
		self.lista.Clear()
		tb.Base.mostrar_tm(self)



if __name__ == "__main__":
	root= wx.App()
	TCA_admin(None, "TCA Administrador de Grupos {} Beta07".format(version))
	root.MainLoop()