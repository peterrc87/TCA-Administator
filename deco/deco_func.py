import wx
import sqlite3
import winsound
import datetime, locale
locale.setlocale(locale.LC_ALL, "es")

#funciones decoradoras.

#función decoradora para conectarse a la base:
def co(fn):
	def co_deco(self,*args):
		self.conexion = sqlite3.connect("grupos.db")
		self.cursor = self.conexion.cursor()
		fn(self, *args)
		self.conexion.close()
	return co_deco


#función contar
@co
def contar_f(self):
	#contará el número de faltas de cada miembro en la base de  datos.
	self.cursor.execute("select * from faltas where n_faltas={}".format(self.text1.GetValue().strip().replace("+", "").replace("-", "").replace(" ", "")))
	self.num_faltas=self.cursor.fetchall()	
	self.cursor.execute("select * from miembros where tlf={}".format(self.text1.GetValue().strip().replace("+", "").replace("-", "").replace(" ", "")))
	self.mi = self.cursor.fetchone()	
	return self.num_faltas, self.mi

#función para ingresar los eliminados.	
def eliminados(self):
	self.obs = ""
	dt = datetime.datetime.now()
	ob_func(self)
	self.cursor.execute("select nombre from miembros where tlf = {}".format(self.it_tlf[1]))
	nom_u = self.cursor.fetchone()
	for i in nom_u:
		nombre_u = i
	self.cursor.execute("insert into eliminados values (null, '{}', '{}', '{}', '{}')".format(self.it_tlf[1], nombre_u, dt.strftime("%A%d%B%Y"), self.obs))
	self.conexion.commit()
	self.che.SetValue(False)
	
#función para observaciones.
def ob_func(self):
	if self.che.IsChecked():
		dlg2 = wx.TextEntryDialog(self, "Ingresa aquí  la observación", "ingresar observación")
		rp = dlg2.ShowModal()
		if rp == wx.ID_OK:
			self.obs = dlg2.GetValue()
			#print("la observación es: ", self.obs)
		else:
			dlg2.Destroy()
	else:
		pass

#función para enviar el foco y sonar.
def foco_so(self):
	winsound.PlaySound("waves/mos.wav", winsound.SND_FILENAME)
	self.lista.SetFocus()



#función decoradora para limpiar la lista.
def clear_lt(fn):
	def lt_c(self, *args):
		self.lista.Enable()
		self.lista.Clear()
		fn(self, *args)
	return lt_c