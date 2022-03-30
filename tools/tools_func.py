import wx, os
import sqlite3
import locale, datetime
from crea_base.class_base import co

locale.setlocale(locale.LC_ALL, "es")



#ffunción para guardar el archivo.
def descargar_co(self):
	archivo=""
	wildcard= "Texto (*txt)|*txt"
	dlg=wx.FileDialog(self,"Guardar como",os.getcwd(),'"{}"'.format(archivo),wildcard=wildcard,style=wx.FD_SAVE| wx.FD_OVERWRITE_PROMPT)
	if(dlg.ShowModal()==wx.ID_OK):
		self.ruta=dlg.GetDirectory()
		self.filename=dlg.GetFilename()
		return self.ruta, self.filename2


#método para exportar los miembros.
@co
def exp_miembros(self):
	descargar_co(self)
	self.cursor.execute("select * from miembros")
	t_mi = self.cursor.fetchall()
	for i in t_mi:
		self.cursor.execute("select * from faltas where n_faltas={}".format(i[1]))
		u = self.cursor.fetchall()
		self.lista.Append("TEL: {} {} Fecha de ingreso: {} Número de faltas: {} Observaciones: {}".format(str(i[1]), str(i[2]), str(i[-2]), len(u), str(i[-1])))
