import wx
#creación del popup 
def create_menu(self):
	self.p_menu = wx.Menu()
	self.it_agre = self.p_menu.Append(-1, "Añadir un integrante")
	self.Bind(wx.EVT_MENU, self.añadir_base, self.it_agre)
	self.it_falta = self.p_menu.Append(-1, "Añadir falta")
	self.Bind(wx.EVT_MENU, self.añadir_falta, self.it_falta)
	self.it_el = self.p_menu.Append(-1, "Eliminar integrante")
	
	#ahora el otro popup para el botón 2.
	self.p2_menu = wx.Menu()
	it_c_fal = self.p2_menu.Append(-1, "Consultar faltas")
	self.Bind(wx.EVT_MENU, self.mostrar, it_c_fal)
	it_tm = self.p2_menu.Append(-1, "Mostrar todos los miembros")
	self.Bind(wx.EVT_MENU, self.mostrar_tm, it_tm)
	
#ahora función para el menú de contexto
def context_menu(self):
	self.lista.Bind(wx.EVT_CONTEXT_MENU,self.showPopupMenu)
	self.m_context = wx.Menu()
	it_eli = self.m_context.Append(-1, "Eliminar")
	self.Bind(wx.EVT_MENU,self.elimina, it_eli)