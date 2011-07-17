import mc, xbmc

# GET
def _get(id):
	config = mc.GetApp().GetLocalConfig()
	return config.GetValue(id)

# SET
def _set(id, val):
	config = mc.GetApp().GetLocalConfig()
	
	if val == False:
		config.Reset(id)
	else:
		config.SetValue(id, str(val))
	
def LOG(output):
	mc.LogInfo("de.jher.startapplications: "+output)
	
def populate():

	list = mc.GetActiveWindow().GetList(2000)

	items = False
	
	mc.ShowDialogWait()
	items = getItems()
	mc.HideDialogWait()

	if len(items) == 0:
		control = mc.GetActiveWindow().GetControl(8000)
		control.SetFocus()

	list.SetItems(items)
	
import xdg.Menu, xdg.IconTheme
def getItems():
	itemList = mc.ListItems()
	menu = xdg.Menu.parse()
	menuName = _get("menu")
	if len(menuName) > 0:
		menu = menu.getMenu(menuName)
		
	menuDisplay = _get("menu-name")
	if len(menuDisplay) == 0:
		menuDisplay = "Applications"
		
	for entry in menu.getEntries():
		item = mc.ListItem( mc.ListItem.MEDIA_UNKNOWN )
		item.SetProperty("parent-menu", menuDisplay)
		if isinstance(entry, xdg.Menu.MenuEntry):
			item.SetLabel(entry.DesktopEntry.getName().encode("UTF-8"))
			item.SetDescription((entry.DesktopEntry.getComment()).encode("UTF-8"))
			iconPath = xdg.IconTheme.getIconPath(entry.DesktopEntry.getIcon(), theme="gartoon", extensions=["png"])
			item.SetProperty("exec", str(entry.DesktopEntry.getExec()))
		elif isinstance(entry, xdg.Menu.Menu):
			item.SetLabel(entry.getName().encode("UTF-8"))
			item.SetDescription((entry.getComment()).encode("UTF-8"))
			iconPath = xdg.IconTheme.getIconPath(entry.getIcon(), theme="gartoon", extensions=["png"])
			enterMenuName = entry.Name.encode("UTF-8")
			if len(_get("menu")) > 0:
				enterMenuName = _get("menu") + "/" + enterMenuName
			item.SetProperty("menu", enterMenuName)
			item.SetProperty("menu-name", str(entry.getName()))
		item.SetIcon(str(iconPath))
		itemList.append(item)
			
	return itemList


from subprocess import call
def list_click():
	win  = mc.GetActiveWindow()
	list = win.GetList(2000)
	
	item = list.GetItem(list.GetFocusedItem())
	command = item.GetProperty("exec")
	if len(command) > 0:
		mc.ShowDialogWait()
		try: call(command.split(" "))
		except OSError, e: LOG(str(e))
		mc.HideDialogWait()
	else:
		menuName = item.GetProperty("menu")
		menuDisplay = item.GetProperty("menu-name")
		_set("menu", menuName)
		_set("menu-name", menuDisplay)
		mc.GetActiveWindow().PushState()
		populate()

mc.GetApp().ActivateWindow(14000, mc.Parameters())
