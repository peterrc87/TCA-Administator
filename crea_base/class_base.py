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
#creo la clase.
class Base():
	def  __init__(self, *arg, **kwargs):
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()
		
		self.cursor.execute("create table if not exists miembros (id integer primary key autoincrement  , tele integer unique not null, nombre varchar(150) not null,  fecha_hora varchar(100), admin varchar(200))")
		print("se creó la tabla miembros")
		
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
			self.cursor.execute("insert into miembros values (null, '{}', '{}', '{}','Admin-{}')".format(self.text1.GetValue(), self.text2.GetValue(), dt.strftime("%a%d%B%Y %H : %M"), self.it_cho_a))
			self.conexion.commit()
				
			

		self.text1.SetLabel("")
		self.text2.SetLabel("")

	@co
	def mostrar(self):
		#muestra de miembros en la base de datos.
		
		self.cursor.execute("select * from miembros")
		self.mi = self.cursor.fetchall()
		for i in self.mi:
			self.lista.Append(str(i))
		self.lista.SetFocus()
	
	def contar(self):
		#contará el número de miembros en la base de  datos.
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()
		self.cursor.execute("select * from miembros")
		self.mi = self.cursor.fetchall()

		self.text1.SetLabel("el número de miembros en la base de datos es: {}".format(len(self.mi)))
		self.text1.SetFocus()