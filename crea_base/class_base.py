import sqlite3
import winsound, os, wx
import datetime, locale
from deco.deco_func import *
locale.setlocale(locale.LC_ALL, "es")
#creo la clase.
class Base():
	def  __init__(self, *arg, **kwargs):
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()		
		self.cursor.execute("create table if not exists miembros (id integer primary key autoincrement, tlf varchar(20) unique not null, nombre varchar(150) not null,  fecha_hora varchar(100), observaciones text)")
		print("se creó la tabla miembros")
		self.cursor.execute("create table if not exists faltas (id integer primary key autoincrement, n_faltas varchar(20) not null, fecha varchar(100), admin varchar(100), obs_fal text, foreign key(n_faltas) references miembros(tlf))")		
		print("se acaba de crear la segunda tabla faltas")
		self.cursor.execute("create table if not exists eliminados (id integer primary key autoincrement, tlf_el varchar(20) not null, nombre_el varchar(150) not null, fecha_el varchar(100), obs_el text, foreign key(tlf_el) references miembros(tlf))")
		print("se ha creado la tabla tercera eliminados")
		self.conexion.close()

	#los métodos de la clase:		
	@co
	def agregar(self):
		self.obs = ""
		dt = datetime.datetime.now()
		ob_func(self)
		
		#compruebo si solo  son números los introducidos en el campo self.text1
		try:
			eval(self.text1.GetValue().replace(" ", ""))*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into miembros values (null, '{}', '{}', '{}', '{}')".format(self.text1.GetValue().strip().replace("-","").replace("+","").replace(" ", ""), self.text2.GetValue().title().strip(), dt.strftime("%A%d%B%Y"), self.obs))
			self.conexion.commit()
			winsound.PlaySound("waves/in.wav", winsound.SND_FILENAME)
		self.che.SetValue(False)
		self.text1.SetLabel("")
		self.text2.SetLabel("")

	#método miembros con faltas en la base de datos.
	@co
	def mostrar_f(self):
		contar_f(self)
		for usu in self.num_faltas:
			self.lista.Append("TEL: {} {} {} Fecha: {} Total faltas: {} OBservaciones: {}".format(str(self.mi[1]), str(self.mi[2]), usu[-2], usu[-3], len(self.num_faltas), usu[-1]))
		self.text1.SetLabel("")
		foco_so(self)
	
	#Método queañadirá una falta a algún miemro.
	@co
	def faltas(self):
		self.obs = ""
		dt = datetime.datetime.now()
		ob_func(self)
		try:
			eval(self.text1.GetValue().replace(" ",""))*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into faltas values (null, '{}', '{}', 'Admin-{}', '{}')".format(self.text1.GetValue().strip().replace("-","").replace("+","").replace(" ", ""),  dt.strftime("%A%d%B%Y"), self.it_cho_a, self.obs))
			self.conexion.commit()
			winsound.PlaySound("waves/fal.wav", winsound.SND_FILENAME)
		self.che.SetValue(False)
		self.text1.SetLabel("")
		self.text2.SetLabel("")
	
	#Método para mostrar la lista de todos los miembros.
	@co
	def mostrar_tm(self):
		self.cursor.execute("select * from miembros")
		t_mi = self.cursor.fetchall()
		for i in t_mi:
			self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
			u = self.cursor.fetchall()
			self.lista.Append("TEL: {} {} Fecha de ingreso: {} Número de faltas: {} Observaciones: {}".format(str(i[1]), str(i[2]), str(i[-2]), len(u), str(i[-1])))
		foco_so(self)
	
	#método para eliminar miembros.
	@co
	def eliminar(self):
		#antes llamo a la función eliminados para que inserte en la tabla eliminados al integrante.
		eliminados(self)
		self.cursor.execute("delete from faltas where n_faltas={}".format(self.it_tlf[1]))
		self.conexion.commit()
		self.cursor.execute("delete from miembros where tlf={}".format(self.it_tlf[1]))
		self.conexion.commit()
		winsound.PlaySound("waves/del.wav", winsound.SND_FILENAME)

	#método para copiar elteléfono al portapapeles.
	def copyclipboard_pg(self):
		texto_portapapeles =wx.TextDataObject(str(self.it_tlf[1]))
		#print("el eelemento al portapapeles es: ",type(self.d_f[self.it2]))
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(texto_portapapeles)
			wx.TheClipboard.Flush()
		winsound.PlaySound("waves/clip.wav", winsound.SND_FILENAME)

	
	#método para mostrar los miembros eliminados.
	@co
	def muestra_el(self):
		#ahora contar en la tabla eliminados
		self.cursor.execute("select * from eliminados")
		self.t_el =self.cursor.fetchall()

		for el in self.t_el:
			self.cursor.execute("select * from eliminados where tlf_el={}".format(el[1]))
			u_el = self.cursor.fetchall()
			self.lista.Append("TEL {} {} fecha eliminación: {} veces eliminado {} Observaciones: {}".format(str(el[1]), el[2], el[-2], len(u_el), el[-1]))
		foco_so(self)

	#método para editar número de teléfono.
	@co
	def editar_tlf(self):
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí el nuevo número de teléfono", "Editando teléfono")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			n_tlf = dlg2.GetValue().strip().replace("+", "").replace("-", "").replace(" ", "")		
		else:
			dlg2.Destroy()
		try:
			eval(n_tlf)*0
		except:
			wx.MessageBox("Debe ingresar un número de teléfono válido", "Atención número incorrecto")
		else:
			self.cursor.execute("update miembros set tlf = {} where tlf = {}".format(n_tlf, self.it_tlf[1]))
			self.cursor.execute("update faltas set n_faltas = {} where n_faltas = {}".format(n_tlf, self.it_tlf[1]))
			self.cursor.execute("update eliminados set tlf_el = {} where tlf_el = {}".format(n_tlf, self.it_tlf[1]))
			self.conexion.commit()
			
	#método para editar el nombre de un miembro.
	@co
	def editar_nombre(self):
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí el nuevo nombre de integrante", "Editando nombre")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			n_nombre = dlg2.GetValue().title().strip()	
			self.cursor.execute("update miembros set nombre = '{}' where tlf = {}".format(n_nombre,self.it_tlf[1]))
			self.conexion.commit()
		else:
			dlg2.Destroy()
		
	#método para editar observaciones.
	@co
	def editar_obs(self):
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí la nueva observación", "Editando observaciones")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			n_obs = dlg2.GetValue().strip()	
			self.cursor.execute("update miembros set observaciones = '{}' where tlf = {}".format(str(n_obs),self.it_tlf[1]))
			self.conexion.commit()
		else:
			dlg2.Destroy()