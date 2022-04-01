import wx, os
import sqlite3
import winsound
import locale, datetime
from crea_base.class_base import co, contar_f

locale.setlocale(locale.LC_ALL, "es")

#creo la ruta para guardar el archivo txt

#ffunción para guardar el archivo.
def descargar_co(self):
	archivo="info_miembros"
	wildcard= "Texto (*txt)|*txt"
	dlg=wx.FileDialog(self,"Guardar como",os.getcwd(), archivo,wildcard=wildcard,style=wx.FD_SAVE| wx.FD_OVERWRITE_PROMPT)
	if(dlg.ShowModal()==wx.ID_OK):
		self.ruta=dlg.GetDirectory()
		self.filename=dlg.GetFilename()
		self.ruta_f = self.ruta+"\{}.txt".format(self.filename)
	return self.ruta_f, self.filename


#método para exportar los miembros.
@co
def exp_miembros(self):
	dt=datetime.datetime.now()
	descargar_co(self)
	
	self.cursor.execute("select * from miembros")
	t_mi = self.cursor.fetchall()
	
	f = open(self.ruta_f, "a")
	f.write("TCAAdministrator 1.0 Informe de miembros \n Fecha de informe: {}\n Total miembros en la base de datos: {}\n Lista de miembros:".format(dt.strftime("%A %d %B %Y Hora: %H:%M"), len(t_mi)))
	f.close()
	print("se creó el informe")
	for i in t_mi:
		self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
		u = self.cursor.fetchall()
		with open(self.ruta_f, "a") as fichero:
			fichero.write("\n TEL: {} {} Fecha de ingreso: {} Número de faltas: {} Observaciones: {}".format(str(i[1]), str(i[2]), str(i[-2]), len(u), str(i[-1])))
		
	winsound.PlaySound("waves/te.wav", winsound.SND_FILENAME)
	
#método para exportar los miembros con faltas.
@co
def ex_faltas(self):
	dt=datetime.datetime.now()
	descargar_co(self)
	self.cursor.execute("select * from faltas")
	total_f = self.cursor.fetchall()
	
	f = open(self.ruta_f, "a")
	f.write("TCAAdministrator 1.0 Informe de miembros con faltas \n Fecha de informe: {}\n Total miembros con faltas: {}\n Lista de miembros con faltas:".format(dt.strftime("%A %d %B %Y Hora: %H:%M"), len(total_f)))
	f.close()
	print("se creó el informe")
	for i in total_f:
		self.cursor.execute("select * from miembros where tlf={}".format(i[1]))
		u = self.cursor.fetchone()
		self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
		tf = self.cursor.fetchall()

		
		with open(self.ruta_f, "a") as fichero:
			fichero.write("\n TEL: {} {} Fecha de falta: {} falta aplicada por:  {} Faltas acumuladas: {} Observaciones: {}".format(str(i[1]), str(u[2]), str(i[-3]), str(i[-2]), len(tf), i[-1]))
		
	winsound.PlaySound("waves/te.wav", winsound.SND_FILENAME)
