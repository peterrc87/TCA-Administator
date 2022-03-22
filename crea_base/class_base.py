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
		winsound.PlaySound("waves/in.wav", winsound.SND_FILENAME)
	return co_deco
	
#función contar
#@co
def contar_f(self):
	#contará el número de miembros en la base de  datos.
	self.cursor.execute("select * from faltas where n_faltas={}".format(self.text1.GetValue()))
	self.num_faltas=self.cursor.fetchall()
	#self.cursor.execute("select * from faltas where n_faltas={}".format(self.text1.GetValue()))
	#self.mi_falta = self.cursor.fetchone()
	self.cursor.execute("select * from miembros where tlf={}".format(self.text1.GetValue()))
	self.mi = self.cursor.fetchone()
	return self.num_faltas, self.mi

	


#creo la clase.
class Base():
	def  __init__(self, *arg, **kwargs):
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()
		
		self.cursor.execute("create table if not exists miembros (id integer primary key autoincrement, tlf varchar(20) unique not null, nombre varchar(150) not null,  fecha_hora varchar(100))")
		print("se creó la tabla miembros")
		self.cursor.execute("create table if not exists faltas (id integer primary key autoincrement, n_faltas varchar(20) not null, fecha varchar(100), admin varchar(100), foreign key(n_faltas) references miembros(tlf))")		
		print("se acaba de crear la segunda tabla faltas")
		
		self.conexion.close()
	#los métodos de la clase:
		
	@co
	def agregar(self):
		dt = datetime.datetime.now()
		
		#compruebo si solo  son números los introducidos en el campo self.text1
		try:
			eval(self.text1.GetValue())*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into miembros values (null, '{}', '{}', '{}')".format(self.text1.GetValue().strip(), self.text2.GetValue().title(), dt.strftime("%a%d%B%Y %H : %M")))
			self.conexion.commit()

		self.text1.SetLabel("")
		self.text2.SetLabel("")

	@co
	def mostrar(self):
		#muestra de miembros en la base de datos.
		
		contar_f(self)
		print(self.num_faltas)
		#print("hay en la tabla faltas {}".format(len(self.num_faltas)))
		
		for usu in self.num_faltas:
			self.lista.Append("TLF: {} {} {} Fecha: {} Total faltas: {}".format(str(self.mi[1]), str(self.mi[2]), usu[-1], usu[-2], len(self.num_faltas)))
		self.lista.SetFocus()
	
		
	@co
	def faltas(self):
		dt = datetime.datetime.now()

		try:
			eval(self.text1.GetValue())*0
		except:
			dlg = wx.MessageBox("Debe introducir un número válido en el campo teléfono")
		else:
			self.cursor.execute("insert into faltas values (null, '{}', '{}', 'Admin-{}')".format(self.text1.GetValue().strip(),  dt.strftime("%a%d%B%Y %H : %M"), self.it_cho_a))

			self.conexion.commit()

		self.text1.SetLabel("")
		self.text2.SetLabel("")
	@co
	def mostrar_tm(self):
		
		self.cursor.execute("select * from miembros")
		t_mi = self.cursor.fetchall()
		for i in t_mi:
			self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
			u = self.cursor.fetchall()
			self.lista.Append("TLF: {} {} Fecha de ingreso: {} Número de faltas: {}".format(str(i[1]), str(i[2]), str(i[-1]), len(u)))
		self.lista.SetFocus()
	
	#método para eliminar faltas.
	@co
	def eliminar(self):
		self.cursor.execute("delete from faltas where n_faltas={}".format(self.it_tlf[1]))
		self.conexion.commit()
		self.cursor.execute("delete from miembros where tlf={}".format(self.it_tlf[1]))
		self.conexion.commit()
		print("se eliminó a {} TLF {}".format(self.it_tlf[2], self.it_tlf[1]))
