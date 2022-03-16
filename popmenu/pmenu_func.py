import wx
#creación del popup 
def create_menu(self):
	self.p_menu = wx.Menu()
	self.it_agre = self.p_menu.Append(-1, "Añadir un integrante")
	self.Bind(wx.EVT_MENU, self.añadir_base, self.it_agre)
	self.it_falta = self.p_menu.Append(-1, "Añadir falta")
	self.Bind(wx.EVT_MENU, self.añadir_falta, self.it_falta)
	self.it_el = self.p_menu.Append(-1, "Eliminar integrante")
	self.it_fal = self.p_menu.Append(-1, "Número de faltas")