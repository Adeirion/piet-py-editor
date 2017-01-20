import sys


#python 2
if sys.version_info.major == 2:
	from Tkinter import Tk, BOTH, Menu, Grid, Canvas, Y, LEFT, TOP, RAISED,  SUNKEN, VERTICAL, HORIZONTAL, RIGHT, SCROLL, UNITS, Text, StringVar, Button
	from ttk import Frame, Label#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry, Scrollbar
	from tkFileDialog import asksaveasfilename, askopenfilename
	#from tkMessageBox import askyesno
	#from tkSimpleDialog import Dialog
#python 3
else:
	from tkinter import Tk, BOTH, Menu, Grid, Canvas, Y, LEFT, TOP, RAISED, SUNKEN, VERTICAL, HORIZONTAL, RIGHT, SCROLL, UNITS, Text, StringVar, Button
	from tkinter.ttk import Frame, Label#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry, Scrollbar
	from tkinter.filedialog  import asksaveasfilename, askopenfilename
	#from tkinter.messagebox  import askyesno
	#from tkinter.simpledialog import Dialog


class PietEditorFrame(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)   

		self.parent = parent

		self.initUI()
		
	def initUI(self):

		self.parent.title("Piet editor")

		self.pack(fill=BOTH, expand=1)

		self.colorselector = Frame(self, relief=RAISED)
		self.colorselector.pack(side=LEFT, fill=Y, expand=False, padx = 5, pady = 5)
		l = Label(self.colorselector, text="colors")
		l.pack(padx = 5, pady = 5)
		
		self.canvas = Canvas(self, width = 300, height = 300, relief=SUNKEN)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1, padx = 5, pady = 5)

		rightPane = Frame(self)
		rightPane.pack(side=LEFT, fill=Y, expand=False)

		self.operations = Frame(self, relief=RAISED)
		self.operations.pack(side=TOP, fill=BOTH, expand=True, in_ = rightPane, padx = 5, pady = 5)
		l2 = Label(self.operations, text="operations")
		l2.pack(padx = 5, pady = 5)

		self.runningFrame = Frame(rightPane, relief=RAISED)
		self.runningFrame.pack(side=TOP, fill=BOTH, expand=True, in_ = rightPane, padx = 5, pady = 5)
		l3 = Label(self.runningFrame, text="running")
		l3.pack(padx = 5, pady = 5)
		

		#Menubar
		menubar = Menu(self)

		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open...", command=self.hello)
		filemenu.add_command(label="Save", command=self.hello)
		filemenu.add_command(label="Save as...", command=self.hello)
		filemenu.add_separator()
		filemenu.add_command(label="Run", command=self.onrun)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.hello)
		menubar.add_cascade(label="File", menu=filemenu)

		# create more pulldown menus
		datamenu = Menu(menubar, tearoff=0)
		datamenu.add_command(label="Cancel", command=self.hello)
		menubar.add_cascade(label="Edit", menu=datamenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.hello)
		menubar.add_cascade(label="Help", menu=helpmenu)

		# display the menu
		self.parent.config(menu=menubar)
		
	def onrun(self, event=None):
		print "run"

	def hello(self):
		print("hello")



	
def main():

	root = Tk()

	root.geometry("1000x500+300+300")
	app = PietEditorFrame(root)
	root.mainloop()  

if __name__ == '__main__':
	main()
