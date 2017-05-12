import sys
import os
import numpy as np
from PIL import Image, ImageDraw

from interpreter import Program
try:
	execfile("D:\Antoine\Programmation\piet-py-editor\interpreter.py")
except Exception:
	pass
	
#python 2
if sys.version_info.major == 2:
	from Tkinter import Tk, BOTH, Menu, Grid, Canvas, X, Y, LEFT, TOP, RAISED,  SUNKEN, VERTICAL, HORIZONTAL, RIGHT, BOTTOM, SCROLL, UNITS, Text, StringVar, Button, Label, Frame, Scrollbar
	#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry
	from tkFileDialog import asksaveasfilename, askopenfilename
	#from tkMessageBox import askyesno
	#from tkSimpleDialog import Dialog
#python 3
else:
	from tkinter import Tk, BOTH, Menu, Grid, Canvas, X, Y, LEFT, TOP, RAISED, SUNKEN, VERTICAL, HORIZONTAL, RIGHT, BOTTOM, SCROLL, UNITS, Text, StringVar, Button, Label, Frame, Scrollbar
	from tkinter.ttk import Frame#, Notebook, Style, Separator, PanedWindow, LabelFrame, Entry, Scrollbar
	from tkinter.filedialog  import asksaveasfilename, askopenfilename
	#from tkinter.messagebox  import askyesno
	#from tkinter.simpledialog import Dialog

color_names = {'lred' : 'light coral',
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
		'lmagenta': 'orchid',
		'magenta' : 'magenta',
		'dmagenta': 'magenta4',
		'white':'white',
		'black':'black'}

#color_rgbs = {'lred' : (240,128,128),
		#'red'  : (255,0,0),
		#'dred' : (139,0,0),
		#'lyellow': (238,221,130),
		#'yellow' : (255,215,0),
		#'dyellow': (218,165,32),
		#'lgreen': (152,251,152),
		#'green' : (0,238,0),
		#'dgreen': (0,100,0),
		#'lcyan': (175,238,238),
		#'cyan' : (0,255,255),
		#'dcyan': (0,134,139),
		#'lblue': (100,149,237),
		#'blue' : (0,0,255),
		#'dblue': (0,0,128),
		#'lmagenta': (218,112,214),
		#'magenta' : (255,0,255),
		#'dmagenta': (139,0,139),
		#'white':(255,255,255),
		#'black':(0,0,0)}

#rgb_colors = {(240,128,128):'lred',
		#(255,0,0) : 'red',
		#(139,0,0) : 'dred',
		#(238,221,130) : 'lyellow',
		#(255,215,0) : 'yellow',
		#(218,165,32) : 'dyellow',
		#(152,251,152) : 'lgreen',
		#(0,238,0) : 'green' ,
		#(0,100,0) : 'dgreen',
		#(175,238,238) : 'lcyan',
		#(0,255,255) : 'cyan',
		#(0,134,139) : 'dcyan',
		#(100,149,237) : 'lblue',
		#(0,0,255) : 'blue',
		#(0,0,128) : 'dblue',
		#(255,105,180) : 'lmagenta',
		#(255,0,255) : 'magenta',
		#(139,0,139) : 'dmagenta',
		#(255,255,255) : 'white',
		#(0,0,0) : 'black'}
		
color_rgbs = {'lred' : (255,192,192),
		'red'  : (255,0,0),
		'dred' : (192,0,0),
		'lyellow': (255,255,192),
		'yellow' : (255,255,0),
		'dyellow': (192,192,0),
		'lgreen': (192,255,192),
		'green' : (0,255,0),
		'dgreen': (0,192,0),
		'lcyan': (192,255,255),
		'cyan' : (0,255,255),
		'dcyan': (0,192,192),
		'lblue': (192,192,255),
		'blue' : (0,0,255),
		'dblue': (0,0,192),
		'lmagenta': (255,192,255),
		'magenta' : (255,0,255),
		'dmagenta': (192,0,192),
		'white':(255,255,255),
		'black':(0,0,0)}

rgb_colors = {(255,192,192):'lred',
		(255,0,0) : 'red',
		(192,0,0) : 'dred',
		(255,255,192) : 'lyellow',
		(255,255,0) : 'yellow',
		(192,192,0) : 'dyellow',
		(192,255,192) : 'lgreen',
		(0,255,0) : 'green' ,
		(0,192,0) : 'dgreen',
		(192,255,255) : 'lcyan',
		(0,255,255) : 'cyan',
		(0,192,192) : 'dcyan',
		(192,192,255) : 'lblue',
		(0,0,255) : 'blue',
		(0,0,192) : 'dblue',
		(255,192,255) : 'lmagenta',
		(255,0,255) : 'magenta',
		(192,0,192) : 'dmagenta',
		(255,255,255) : 'white',
		(0,0,0) : 'black'}

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

		self.frontcolor="white"
		self.backcolor="black"

		self.tool="pen"

		self.initUI()
		
	def initUI(self):

		self.master.title("Piet editor")

		self.pack(fill=BOTH, expand=1)

		self.toolbar = ToolBarFrame(self)
		self.toolbar.pack(side=TOP, fill=X, expand=False)

		self.colorselector = ColorFrame(self)
		self.colorselector.pack(side=LEFT, fill=Y, expand=False, padx = 5, pady = 5)
		
		self.canvasframe = CanvasFrame(self)
		self.canvasframe.pack(side=LEFT, fill=BOTH, expand=1, pady = 5)

		self.executionFrame = Frame(self, relief=RAISED, borderwidth=2)
		self.executionFrame.pack(side=LEFT, fill=BOTH, expand=False, padx = 5, pady = 5)
		l3 = Label(self.executionFrame, text="running")
		l3.pack(padx = 5, pady = 5)
		

		#Menubar
		menubar = Menu(self)

		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="New...", command=self.onnew)
		filemenu.add_command(label="Open...", command=self.canvasframe.open)
		filemenu.add_command(label="Save", command=self.canvasframe.onsave)
		filemenu.add_command(label="Save as...", command=self.canvasframe.onsaveas)
		filemenu.add_separator()
		filemenu.add_command(label="Run", command=self.onrun)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.hello)
		menubar.add_cascade(label="File", menu=filemenu)

		# create more pulldown menus
		datamenu = Menu(menubar, tearoff=0)
		datamenu.add_command(label="Cancel", command=self.canvasframe.cancel)
		datamenu.add_command(label="Repeat", command=self.canvasframe.repeat)
		datamenu.add_separator()
		datamenu.add_command(label="Copy", command=self.canvasframe.copy)
		datamenu.add_command(label="Paste", command=self.canvasframe.paste)
		datamenu.add_separator()
		datamenu.add_command(label="Zoom in", command=self.canvasframe.zoomin)
		datamenu.add_command(label="Zoom out", command=self.canvasframe.zoomout)
		menubar.add_cascade(label="Edit", menu=datamenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.hello)
		menubar.add_cascade(label="Help", menu=helpmenu)

		# display the menu
		self.master.config(menu=menubar)
		
	def onrun(self, event=None):
		print "run"
	
	def onnew(self, event=None):
		#check if saved
		self.canvasframe.new_program(30,30)
	
	def getfrontcolor(self):
		return self.frontcolor

	def getbackcolor(self):
		return self.backcolor

	def hello(self):
		print("hello")

	def settool(self,tool):
		self.tool = tool

class ToolBarFrame(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent, relief=RAISED, borderwidth=1)

		self.parent = parent

		self.penlabel = Label(self, text="pen", relief='sunken' )
		self.penlabel.pack(side=LEFT, fill=None, expand=False)
		self.penlabel.bind("<Button-1>", lambda event: self.select_tool("pen"))
		self.bucketlabel = Label(self, text = "bucket", relief = 'raised')
		self.bucketlabel.pack(side=LEFT, fill=None, expand=False)
		self.bucketlabel.bind("<Button-1>", lambda event: self.select_tool("bucket"))
		self.selectlabel = Label(self, text="select", relief = 'raised')
		self.selectlabel.pack(side=LEFT, fill=None, expand=False)
		self.selectlabel.bind("<Button-1>", lambda event: self.select_tool("select"))

	def select_tool(self, tool):
		#print tool
		if tool != self.parent.tool:
			if tool=="pen":
				self.penlabel.config(relief='sunken')
			elif tool=="bucket":
				self.bucketlabel.config(relief='sunken')
			elif tool=="select":
				self.selectlabel.config(relief='sunken')
			if self.parent.tool=="pen":
				self.penlabel.config(relief='raised')
			elif self.parent.tool=="bucket":
				self.bucketlabel.config(relief='raised')
			elif self.parent.tool=="select":
				self.selectlabel.config(relief='raised')
			self.parent.tool=tool
		
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
				label = Label(self, background=color_names[color], borderwidth=1, relief='solid', text=operation_matrix[r][c], font=("TkDefaultFont",10))
				label.grid(row=2*r, column=2*c, rowspan=2, columnspan=2, sticky='NSEW', padx=1, pady=1)
				label.bind("<Button-1>", lambda event, color=color: self.newfrontcolor(color))
				label.bind("<Button-3>", lambda event, color=color: self.newbackcolor(color))
				self.labels.append(label)
		for i in [1,2,5,8,11,13,14,16,17]:
			self.labels[i].config(foreground = 'black' if c<2 else 'white')
		
		self.rowconfigure(12, minsize=rowsize)
		label = Label(self, background=color_names['white'], borderwidth=1, relief='solid')
		label.grid(row=6*2, column=0, rowspan=2, columnspan=3, sticky='NSEW', padx=1, pady=1)
		label.bind("<Button-1>", lambda event, color='white': self.newfrontcolor('white'))
		label.bind("<Button-3>", lambda event, color='white': self.newbackcolor('white'))

		label = Label(self, background=color_names['black'], borderwidth=1, relief='solid')
		label.grid(row=6*2, column=3, rowspan=2, columnspan=3, sticky='NSEW', padx=1, pady=1)
		label.bind("<Button-1>", lambda event, color='black': self.newfrontcolor('black'))
		label.bind("<Button-3>", lambda event, color='black': self.newbackcolor('black'))

		self.rowconfigure(14, minsize=rowsize)
		self.rowconfigure(15, minsize=4*rowsize)
		self.rowconfigure(16, minsize=rowsize)
		self.backcolorlabel = Label(self, background=color_names['black'], relief='sunken')
		self.backcolorlabel.grid(row=14, column=0, rowspan=2, columnspan=5, sticky='NSEW', padx=10, pady=10)

		self.frontcolorlabel = Label(self, background=color_names['white'], relief='raised')
		self.frontcolorlabel.grid(row=15, column=1, rowspan=2, columnspan=5, sticky='NSEW', padx=10, pady=10)

	def newfrontcolor(self, color):
		self.parent.frontcolor=color
		self.frontcolorlabel.config(background=color_names[color])
		
		for r in range(6):
			for c in range(3):
				if color_matrix[r][c]==color:
					for l in range(18):
						self.labels[(l+r*3+c-(3 if l%3>2-c else 0))%18].config(text=operation_matrix[l/3][l%3])
					return

	def newbackcolor(self, color):
		self.parent.backcolor=color
		self.backcolorlabel.config(background=color_names[color])

		
class CanvasFrame(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent=parent
		
		#in pixels
		self.codel_size=10

		self.canvas = Canvas(self, relief=SUNKEN, borderwidth=1, background="grey")
		
		hbar=Scrollbar(self, orient=HORIZONTAL)
		hbar.pack(side=BOTTOM,fill=X)
		hbar.config(command=self.canvas.xview)
		vbar=Scrollbar(self,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas.yview)
		#self.canvas.config(width=500,height=500)
		self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

		self.new_program(30,30)

		self.canvas.bind("<Control-C>", self.copy)
		
	def new_program(self,height,width):
		
		self.program = Program(height,width)
		self.openfile = ""
		self.cwd=os.getcwd()
		self.modified=True
		self.history=[]
		self.history_index=0
	
		self.canvas.delete('all')
		self.canvas.config(scrollregion=(0,0,width*self.codel_size,height*self.codel_size))
		self.codelgrid = np.empty((height,width), dtype=int)
		self.selection = None
		
		for i in range(self.program.height):
			for j in range(self.program.width):
				self.codelgrid[i,j] = self.canvas.create_rectangle(j*self.codel_size, i*self.codel_size, (j+1)*self.codel_size, (i+1)*self.codel_size, fill='white')

		self.canvas.tag_bind('all', '<Button-1>', self.onclick)
		self.canvas.tag_bind('all', '<Button-3>', self.onclick)
		self.canvas.tag_bind('all', '<B1-Motion>', self.onmove)
		self.canvas.tag_bind('all', '<B3-Motion>', self.onmove)
		self.canvas.tag_bind('all', '<ButtonRelease-1>', self.onrelease)
		self.canvas.tag_bind('all', '<ButtonRelease-3>', self.onrelease)

		
	def onsave(self):
		self.save(self.openfile)

	def onsaveas(self):
		self.save("")

	def save(self, savefile=""):

		if savefile=="":
		
			savefile = asksaveasfilename(defaultextension=".png", filetypes=[("Image Files", ".png")], initialdir=self.cwd, initialfile=self.openfile,parent=self, title="Save as")

			if savefile=="":
				return
		
		image = Image.new("RGB", (self.program.width*self.codel_size, self.program.height*self.codel_size), (255,255,255))
		draw = ImageDraw.Draw(image)
		for i in range(self.program.height):
			for j in range(self.program.width):
				draw.rectangle((j*self.codel_size, i*self.codel_size, (j+1)*self.codel_size, (i+1)*self.codel_size), fill = color_rgbs[self.program.get_codel(i,j)])
		image.save(savefile)
		
		self.cwd = os.path.dirname(savefile)
		self.openfile=savefile
		self.modified=False
		
		
	def open(self, openfile=""):

		if openfile=="":

			openfile = askopenfilename(defaultextension=".png", filetypes=[("Image files", ".png")], initialdir=self.cwd, initialfile="",parent=self, title="Open image")
		
			if openfile=="":
				return

			image = Image.open(openfile)
			#TODO: detect codel size : for each line and each row, take biggest divisor of min number of contiguous pixels

			image = image.convert("RGB")

			bbox= image.getbbox()
			width = bbox[2]/self.codel_size
			height = bbox[3]/self.codel_size
			self.new_program(height, width)
			for x in range(0, bbox[2], self.codel_size):
				for y in range(0, bbox[3], self.codel_size):
					color=rgb_colors[image.getpixel((x, y))]
					self.canvas.itemconfig(self.canvas.find_closest(x,y), fill=color_names[color])
					self.program.set_codel(y/self.codel_size, x/self.codel_size,color)
			
			self.cwd = os.path.dirname(openfile)
			self.openfile = openfile
			self.modified=False
			
	def asksave(self):
		if self.modified == True:
			if askyesno("Save", "Save file?"):
				self.onsave()
				return self.openfile
			else:
				return None
		return self.openfile

	def onclick(self, event):

		x = self.canvas.canvasy(event.x)-3
		y = self.canvas.canvasy(event.y)-3

		if x<0 or y<0:
			return

		#!!!!! y in rows and x in columns
		row = int(y)/self.codel_size
		if row == self.program.height:
			row=row-1
		column = int(x)/self.codel_size
		if column == self.program.width:
			column=column-1

		if event.num==1:
			color = self.parent.getfrontcolor()
		else:
			color = self.parent.getbackcolor()

		self.init_row = row
		self.init_column = column
		self.current_row = row
		self.current_column = column

		if self.parent.tool == "pen":
			self.modified=True
			del self.history[self.history_index:]
			self.history_index = self.history_index+1
			self.history.append(([(row,column)], color, [self.program.get_codel(row,column)]))
			self.paint((row,column),color)
		
		elif self.parent.tool == "bucket":

			block = self.program.get_colorblock(row,column)

			self.modified=True
			del self.history[self.history_index:]
			self.history_index = self.history_index+1
			self.history.append((block, color, [self.program.get_codel(row,column)]))
			self.paint(block, color)

		elif self.parent.tool == "select":
			self.canvas.delete("selection")
			self.selection=[]

			self.canvas.create_rectangle(column*self.codel_size, row*self.codel_size, (column+1)*self.codel_size, (row+1)*self.codel_size, fill = "", outline="red", dash = (4,4), width=2, tags="selection")
			
			

	def onmove(self, event):
		x = self.canvas.canvasy(event.x)-3
		y = self.canvas.canvasy(event.y)-3

		#if x<0 or y<0:
		#	return

		#!!!!! y in rows and x in columns
		row = int(y)/self.codel_size
		if row == self.program.height:
			row=row-1
		column = int(x)/self.codel_size
		if column == self.program.width:
			column=column-1
		
		if row<0 or column<0 or row>self.program.height or column>self.program.width:
			return

		if self.current_row == row and self.current_column == column:
			return

		
		self.current_row = row
		self.current_column = column

		if self.parent.tool == "pen":

			block, newcolor, oldcolors = self.history[self.history_index-1]
			if (row,column) not in block:
				block.append((row,column))
				oldcolors.append(self.program.get_codel(row,column))
				self.paint((row,column), newcolor)
			

		elif self.parent.tool == "select":
		
			row0,row1 = np.sort([row,self.init_row])
			column0,column1 = np.sort([column,self.init_column])

			self.canvas.delete("selection")
			self.canvas.create_rectangle(column0*self.codel_size, row0*self.codel_size, (column1+1)*self.codel_size, (row1+1)*self.codel_size, fill = "", outline="red", dash = (4,4), width=2, tags="selection")


	def onrelease(self, event):
		x = self.canvas.canvasy(event.x)-3
		y = self.canvas.canvasy(event.y)-3

		if x<0 or y<0:
			return

		#!!!!! y in rows and x in columns
		row = int(y)/self.codel_size
		if row == self.program.height:
			row=row-1
		column = int(x)/self.codel_size
		if column == self.program.width:
			column=column-1

		if self.parent.tool == "select":
		
			if len(self.canvas.find_withtag("selection")) > 0:
				coords = self.canvas.coords("selection")
				self.selection = map(lambda i: int(i/self.codel_size), [coords[i] for i in [1,0,3,2]])

		del self.init_row
		del self.init_column

		del self.current_row
		del self.current_column
		

	
	def cancel(self):
		if self.history_index == 0:
			return
		self.history_index = self.history_index-1
		block, new_color, old_color = self.history[self.history_index]
		self.paint(block, old_color)

	def repeat(self):
		if self.history_index == len(self.history):
			return
		block, new_color, old_color = self.history[self.history_index]
		self.history_index = self.history_index+1
		self.paint(block, new_color)

	def paint(self, codels, new_color):
		
		if type(codels[0]) == int:
			codels=[codels]

		if type(new_color) == str:
			new_color = [new_color]
		
		if len(new_color) == 1:
			new_color = new_color*len(codels)

		for (row,column),color in zip(codels, new_color):
			self.canvas.itemconfig(self.codelgrid[row,column], fill=color_names[color])
			self.program.set_codel(row,column,color)

	def zoomin(self):
		if self.codel_size >= 80:
			self.resize(80)
			return
		self.resize(int(self.codel_size*2))

	def zoomout(self):
		if self.codel_size <=5:
			self.resize(5)
			return
		self.resize(int(self.codel_size/2))

	def copy(self):
		if self.selection is not None:
			self.clipboard=[[self.program.get_codel(r,c) for c in range(self.selection[1], self.selection[3])] for r in range(self.selection[0], self.selection[2])]
		print self.clipboard
		
#		self.clipboard = 

	def paste(self):
		print "paste"

	def resize(self, new_codel_size):
		scale = float(new_codel_size)/self.codel_size
		self.canvas.config(scrollregion=(0, 0, self.program.width*new_codel_size,self.program.height*new_codel_size))
		self.canvas.scale('all', 0, 0, scale, scale)
		self.codel_size = new_codel_size


def main():

	root = Tk()

	root.geometry("1000x500+150+150")
	app = PietEditorFrame(root)
	root.mainloop()  

if __name__ == '__main__':
	main()
