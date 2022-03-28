import sqlite3
import winsound, os, wx
import datetime, locale
locale.setlocale(locale.LC_ALL, "es")

#función decoradora para conectarse a la base:
def co(fn):
	def co_deco(self,*args):
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()
		fn(self, *args)
		self.conexion.close()
		#winsound.PlaySound("waves/in.wav", winsound.SND_FILENAME)
	return co_deco
	
#función contar
@co
def contar_f(self):
	#contará el número de faltas de cada miembro en la base de  datos.
	self.cursor.execute("select * from faltas where n_faltas={}".format(self.text1.GetValue()))
	self.num_faltas=self.cursor.fetchall()	
	self.cursor.execute("select * from miembros where tlf={}".format(self.text1.GetValue()))
	self.mi = self.cursor.fetchone()
	
	return self.num_faltas, self.mi

#función para ingresar los eliminados.	
def eliminados(self):
	self.obs = ""
	dt = datetime.datetime.now()
	ob_func(self)
	self.cursor.execute("insert into eliminados values (null, '{}', '{}', '{}', '{}')".format(self.it_tlf[1], self.it_tlf[2], dt.strftime("%a%d%B%Y"), self.obs))
	self.conexion.commit()
	self.che.SetValue(False)
	
#función para observaciones.
def ob_func(self):
	if self.che.IsChecked():
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí  la observación", "ingresar observación")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			self.obs = dlg2.GetValue()
			print("la observación es: ", self.obs)
		else:
			dlg2.Destroy()
	else:
		pass

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
			eval(self.text1.GetValue())*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into miembros values (null, '{}', '{}', '{}', '{}')".format(self.text1.GetValue().strip().replace("-","").replace("+",""), self.text2.GetValue().title(), dt.strftime("%a%d%B%Y"), self.obs))
			self.conexion.commit()
			winsound.PlaySound("waves/in.wav", winsound.SND_FILENAME)
		self.che.SetValue(False)
		self.text1.SetLabel("")
		self.text2.SetLabel("")

	@co
	def mostrar_f(self):
		#muestra de miembros con faltas en la base de datos.
		
		contar_f(self)
		#print(self.num_faltas)
		#print("hay en la tabla faltas {}".format(len(self.num_faltas)))
		
		for usu in self.num_faltas:
			self.lista.Append("TEL: {} {} {} Fecha: {} Total faltas: {} OBservaciones: {}".format(str(self.mi[1]), str(self.mi[2]), usu[-2], usu[-3], len(self.num_faltas), usu[-1]))
		winsound.PlaySound("waves/mos.wav", winsound.SND_FILENAME)
		self.text1.SetLabel("")
		self.lista.SetFocus()
	
		
	@co
	def faltas(self):
		#añadirá una falta a algún miemro.
		self.obs = ""
		dt = datetime.datetime.now()
		ob_func(self)
		try:
			eval(self.text1.GetValue())*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into faltas values (null, '{}', '{}', 'Admin-{}', '{}')".format(self.text1.GetValue().strip().replace("-","").replace("+",""),  dt.strftime("%a%d%B%Y"), self.it_cho_a, self.obs))
			self.conexion.commit()
			winsound.PlaySound("waves/fal.wav", winsound.SND_FILENAME)

		self.che.SetValue(False)
		self.text1.SetLabel("")
		self.text2.SetLabel("")
	@co
	def mostrar_tm(self):
		
		self.cursor.execute("select * from miembros")
		t_mi = self.cursor.fetchall()
		for i in t_mi:
			self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
			u = self.cursor.fetchall()
			self.lista.Append("TEL: {} {} Fecha de ingreso: {} Número de faltas: {} Observaciones: {}".format(str(i[1]), str(i[2]), str(i[-2]), len(u), str(i[-1])))
		winsound.PlaySound("waves/mos.wav", winsound.SND_FILENAME)

		self.lista.SetFocus()
	
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
		print("se eliminó a {} TLF {}".format(self.it_tlf[2], self.it_tlf[1]))

	
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
		winsound.PlaySound("waves/mos.wav", winsound.SND_FILENAME)
		self.lista.SetFocus()

	
	#método para editar número de teléfono.
	@co
	def editar_tlf(self):
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí el nuevo número de teléfono", "Editando teléfono")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			n_tlf = dlg2.GetValue().strip().replace("+", "").replace("-", "")		
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
			print("se cambió el número de teléfono con éxito")