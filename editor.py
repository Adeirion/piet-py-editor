import sys


#python 2
if sys.version_info.major == 2:
	from Tkinter import Tk, BOTH, Menu, Grid, Canvas, Y, LEFT, TOP, RAISED,  SUNKEN, VERTICAL, HORIZONTAL, RIGHT, SCROLL, UNITS, Text, StringVar, Button, Label, Frame
	#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry, Scrollbar
	from tkFileDialog import asksaveasfilename, askopenfilename
	#from tkMessageBox import askyesno
	#from tkSimpleDialog import Dialog
#python 3
else:
	from tkinter import Tk, BOTH, Menu, Grid, Canvas, Y, LEFT, TOP, RAISED, SUNKEN, VERTICAL, HORIZONTAL, RIGHT, SCROLL, UNITS, Text, StringVar, Button, Label
	from tkinter.ttk import Frame#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry, Scrollbar
	from tkinter.filedialog  import asksaveasfilename, askopenfilename
	#from tkinter.messagebox  import askyesno
	#from tkinter.simpledialog import Dialog

colors = {'lred' : 'light coral',
		'red'  : 'red',
		'dred' : 'dark red',
		'lyellow': 'light goldenrod',
		'yellow' : 'gold',
		'dyellow': 'goldenrod',
		'lgreen': 'pale green',
		'green' : 'green2',
		'dgreen': 'dark green',
		'lcyan': 'pale turquoise',
		'cyan' : 'turquoise',
		'dcyan': 'turquoise4',
		'lblue': 'cornflower blue',
		'blue' : 'blue',
		'dblue': 'navy',
		'lmagenta': 'hot pink',
		'magenta' : 'magenta',
		'dmagenta': 'magenta4',
		'white':'white',
		'black':'black'}

color_matrix = [['lred', 'red', 'dred'],
			 ['lyellow', 'yellow', 'dyellow'],
			 ['lgreen', 'green', 'dgreen'],
			 ['lcyan', 'cyan', 'dcyan'],
			 ['lblue', 'blue', 'dblue'],
			 ['lmagenta', 'magenta', 'dmagenta']]

operation_matrix = [['', 'push', 'pop'],
				['add', 'substract', 'multiply'],
				['divide', 'mod', 'not'],
				['greater', 'pointer', 'switch'],
				['duplicate', 'roll', 'in(int)'],
				['in(char)', 'out(int)', 'out(char)']]

class PietEditorFrame(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)   

		self.initUI()
		
	def initUI(self):

		self.master.title("Piet editor")

		self.pack(fill=BOTH, expand=1)

		self.colorselector = ColorFrame(self)
		self.colorselector.pack(side=LEFT, fill=Y, expand=False, padx = 5, pady = 5)
		
		self.canvasframe = CanvasFrame(self)
		self.canvasframe.pack(side=LEFT, fill=BOTH, expand=1, padx = 5, pady = 5)

		self.executionFrame = Frame(self, relief=RAISED, borderwidth=2)
		self.executionFrame.pack(side=LEFT, fill=BOTH, expand=False, padx = 5, pady = 5)
		l3 = Label(self.executionFrame, text="running")
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
		self.master.config(menu=menubar)
		
	def onrun(self, event=None):
		print "run"

	def hello(self):
		print("hello")

class ColorFrame(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent, relief=RAISED, borderwidth=2)

		self.parent=parent

		rowsize=30
		colsize=30

		self.frontcolor="white"
		self.backcolor="black"

		self.labels=[]

		for c in range(6):
			self.columnconfigure(c, minsize=colsize)
		

		for r in range(6):
			self.rowconfigure(2*r, minsize=rowsize)
			for c in range(3):
				color=color_matrix[r][c]
				label = Label(self, background=colors[color], borderwidth=1, relief='solid', text=operation_matrix[r][c], font=("TkDefaultFont",10))
				label.grid(row=2*r, column=2*c, rowspan=2, columnspan=2, sticky='NSEW', padx=1, pady=1)
				label.bind("<Button-1>", lambda event, color=color: self.newfrontcolor(color))
				label.bind("<Button-3>", lambda event, color=color: self.newbackcolor(color))
				self.labels.append(label)
		for i in [1,2,5,8,11,13,14,16,17]:
			self.labels[i].config(foreground = 'black' if c<2 else 'white')
		
		self.rowconfigure(12, minsize=rowsize)
		label = Label(self, background=colors['white'], borderwidth=1, relief='solid')
		label.grid(row=6*2, column=0, rowspan=2, columnspan=3, sticky='NSEW', padx=1, pady=1)
		label.bind("<Button-1>", lambda event, color='white': self.newfrontcolor('white'))
		label.bind("<Button-3>", lambda event, color='white': self.newbackcolor('white'))

		label = Label(self, background=colors['black'], borderwidth=1, relief='solid')
		label.grid(row=6*2, column=3, rowspan=2, columnspan=3, sticky='NSEW', padx=1, pady=1)
		label.bind("<Button-1>", lambda event, color='black': self.newfrontcolor('black'))
		label.bind("<Button-3>", lambda event, color='black': self.newbackcolor('black'))

		self.rowconfigure(14, minsize=rowsize)
		self.rowconfigure(15, minsize=4*rowsize)
		self.rowconfigure(16, minsize=rowsize)
		self.backcolorlabel = Label(self, background=colors['black'], relief='sunken')
		self.backcolorlabel.grid(row=14, column=0, rowspan=2, columnspan=5, sticky='NSEW', padx=10, pady=10)

		self.frontcolorlabel = Label(self, background=colors['white'], relief='raised')
		self.frontcolorlabel.grid(row=15, column=1, rowspan=2, columnspan=5, sticky='NSEW', padx=10, pady=10)

	def newfrontcolor(self, color):
		self.frontcolor=color
		self.frontcolorlabel.config(background=colors[color])
		
		for r in range(6):
			for c in range(3):
				if color_matrix[r][c]==color:
					print color
					for l in range(18):
						self.labels[(l+r*3+c-(3 if l%3>2-c else 0))%18].config(text=operation_matrix[l/3][l%3])
					return

	def newbackcolor(self, color):
		self.backcolor=color
		self.backcolorlabel.config(background=colors[color])

	def getfrontcolor(self):
		return self.frontcolor
	def getbackcolor(self):
		return self.backcolor
		
class CanvasFrame(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent=parent
		
		self.codel_size=10
		self.image_height = 30
		self.image_width = 30
	
		self.canvas = Canvas(self, background='white')
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1, padx = 5, pady = 5)
		
		for i in range(self.image_height):
			self.canvas.create_line(0, i*self.codel_size, self.image_height*self.codel_size, i*self.codel_size)

def main():

	root = Tk()

	root.geometry("1000x500+300+300")
	app = PietEditorFrame(root)
	root.mainloop()  

if __name__ == '__main__':
	main()
