import sys
import numpy as np
from PIL import Image, ImageDraw

code_colors = {0:'white', 1: 'black',
			11:'lred', 12:'red', 13:'dred',
			21:'lyellow', 22:'yellow', 23:'dyellow',
			31:'lgreen', 32:'green', 33:'dgreen',
			41:'lcyan', 42:'cyan', 43:'dcyan',
			51:'lblue', 52:'blue', 53:'dblue',
			61:'lmagenta', 62:'magenta', 63:'dmagenta'}

color_codes = {'white':0, 'black':1,
			'lred':11, 'red':12, 'dred':13,
			'lyellow':21, 'yellow':22, 'dyellow':23,
			'lgreen':31, 'green':32, 'dgreen':33,
			'lcyan':41, 'cyan':42, 'dcyan':43,
			'lblue':51, 'blue':52, 'dblue':53,
			'lmagenta':61, 'magenta':62, 'dmagenta':63}
			
code_ops = {0:'noop', 1:'push', 2:'pop',
				10:'add', 11:'substract', 12:'multiply',
				20:'divide', 21:'mod', 22:'not',
				30:'greater', 31:'pointer', 32:'switch',
				40:'duplicate', 41:'roll', 42:'in(int)',
				50:'in(char)', 51:'out(int)', 52:'out(char)'}

class Program():

	"""
	Piet program

	height : number of rows
	width : number of columns

	"""
	def __init__(self, height, width):
		self.height = height
		self.width = width

		self.program = np.zeros((height, width), dtype='int')

	def set_codel(self, row, column, color):
		self.program[row,column] = color_codes[color]

	def get_codel(self, row, column):
		if row<0 or row>=self.height or column<0 or column>=self.width:
			return 'black'
		return code_colors[self.program[row, column]]

	def get_codel_code(self, row, column):
		if row<0 or row>=self.height or column<0 or column>=self.width:
			return 1
		return self.program[row, column]

	def get_colorblock(self, row, column):
		"""
		Returns a list of tuple with coordinates of the codels of the colorblock.
		"""

		block = [(row,column)]

		expand=True
		index=0
		while(index<len(block)):
			x=block[index][0]
			y=block[index][1]
			#to the top
			if x>0 and self.program[x-1,y]==self.program[row,column] and (x-1,y) not in block:
					block.append((x-1,y))
			#to the bottom
			if x<self.height-1 and self.program[x+1,y]==self.program[row,column] and (x+1,y) not in block:
					block.append((x+1,y))
			#to the left
			if y>0 and self.program[x,y-1]==self.program[row,column] and (x,y-1) not in block:
					block.append((x,y-1))
			#to the right
			if y<self.width-1 and self.program[x,y+1]==self.program[row,column] and (x,y+1) not in block:
					block.append((x,y+1))
			index = index+1
		return block
		
def load(imagefile, codel_size=10):
	
	image = Image.open(imagefile)
	#TODO: detect codel size : for each line and each row, take biggest divisor of min number of contiguous pixels

	image = image.convert("RGB")

	bbox= image.getbbox()
	width = bbox[2]/codel_size
	height = bbox[3]/codel_size
	program = Program(height, width)
	for x in range(0, bbox[2], codel_size):
		for y in range(0, bbox[3], codel_size):
			color=rgb_colors[image.getpixel((x, y))]
			program.set_codel(y/codel_size, x/codel_size,color)
			
	return program
		
class Interpreter():

	def __init__(self, program=None):
		
		self.set_program(program)
		
		self.debug = True
		
	def set_program(self, program):
		self.program = program
		self.reset()
		
	def reset(self):
		self.step=0
		self.row=0
		self.column=0
		self.next_row=0
		self.next_column=0
		self.next_op=""
		self.stack=[]
		self.dp=0
		self.cc=0
		self.it=0
		self.running=False
		
	def start(self):
	
		self.running=True
		self.next_row, self.next_column, self.next_op = self._get_next()
		
	def stop(self):
	
		self.running=False
		self.next_row = -1
		self.next_column = -1
		self.next_op = ""
		
	def _get_next(self):
		
		if self.it == 8:
			return (-1,-1),""
		
		block = self.program.get_colorblock(self.row, self.column)
		
		if self.dp == 0:
			y = np.max([codel[1] for codel in block])
			if self.cc == 0:
				x = np.min([codel[0] for codel in block if codel[1]==y])
			else:
				x = np.max([codel[0] for codel in block if codel[1]==y])
			y = y+1
		elif self.dp == 1:
			x = np.max([codel[0] for codel in block])
			if self.cc == 0:
				y = np.max([codel[1] for codel in block if codel[0]==x])
			else:
				y = np.min([codel[1] for codel in block if codel[0]==x])
			x = x+1
		elif self.dp == 2:
			y = np.min([codel[1] for codel in block])
			if self.cc == 0:
				x = np.max([codel[0] for codel in block if codel[1]==y])
			else:
				x = np.min([codel[0] for codel in block if codel[1]==y])
			y = y-1
		elif self.dp == 3:
			x = np.min([codel[0] for codel in block])
			if self.cc == 0:
				y = np.max([codel[1] for codel in block if codel[0]==x])
			else:
				y = np.min([codel[1] for codel in block if codel[0]==x])
			x = x-1
			
		white=False
		if self.program.get_codel(x,y) == 'white':
			##############WRONG!!!!!!############
			while(self.program.get_codel(x,y) == 'white'):
				if self.dp == 0:
					y=y+1
				elif self.dp == 1:
					x=x+1
				elif self.dp == 2:
					y=y-1
				elif self.dp == 3:
					x=x-1
			white=True
			
		
		color = self.program.get_codel_code(self.row, self.column)
		nextcolor = self.program.get_codel_code(x,y)
			
		if nextcolor == 1: #black
			op = ""
		else:
			if white:
				op = "noop"
			else:
				opcode = ((nextcolor/10-color/10)%6)*10+(nextcolor%10-color%10)%3	
				op = code_ops[opcode]
		
		return x,y,op
		
	def next(self):
	
		if self.running == False:
			return
			
		#1)execute
		
		if self.debug:
			print self.next_op
		
		self.execute(self.next_op)
		
		#2)move
		if self.next_op == "":
			if self.it%2==0:
				self.cc = 1 - self.cc
			else:
				self.dp = (self.dp+1)%4
			self.it = self.it + 1
		else:	
			self.row = self.next_row
			self.column = self.next_column
			self.it = 0
			
			if self.debug:
				print "Go to {}".format((self.row,self.column))
		
		#3)get next
			
		self.next_row, self.next_column, self.next_op = self._get_next()
		
		if self.it == 8:
			self.stop()
		
		if self.debug:
			print "stack: {}".format(self.stack)
			print "next codel: {}".format((self.next_row, self.next_column))
			print "next op: {}".format(self.next_op)
		
		
	def execute(self, operation):
	
	#TODO for pointer and switch, check with negative values
	
		self.step=self.step+1
		
		if operation == "noop":
			pass
		elif operation == "push":
			value = len(self.program.get_colorblock(self.row, self.column))
			self.stack.append(value)
		elif operation == "pop":
			self.stack.pop()
		elif operation == "add":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(v2+v1)
		elif operation == "substract":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(v2-v1)
		elif operation == "multiply":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(v2*v1)
		elif operation == "divide":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(v2/v1)
		elif operation == "mod":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(v2%v1)
		elif operation == "not":
			v1=self.stack.pop()
			self.stack.append(int(not v1))
		elif operation == "greater":
			v1=self.stack.pop()
			v2=self.stack.pop()
			self.stack.append(int(v2>v1))
		elif operation == "pointer":
			v1=self.stack.pop()
			self.dp=(self.dp+v1)%4
		elif operation == "switch":
			v1=self.stack.pop()
			self.cc=(self.cc+v1)%2
		elif operation == "duplicate":
			self.stack.append(self.stack[-1])
		elif operation == "roll":
			v1=self.stack.pop()
			v2=self.stack.pop()
			values = self.stack[-v2:]
			self.stack[-v2:] = values[-(v1%len(values)):] + values[:-(v1%len(values))]
		elif operation == "in(int)":
			value = int(raw_input("Enter a number: "))
			self.stack.append(value)
		elif operation == "in(char)":
			value = ord(raw_input("Enter a character: "))
			self.stack.append(value)
		elif operation == "out(int)":
			v1 = self.stack.pop()
			print v1
		elif operation == "out(char)":
			v1 = self.stack.pop()
			print chr(v1)
	
def main():
	
	pass
	#program_file = sys.argv[1]

	#load program
	#program = load(program_file, codel_size)

	#run 

if __name__ == '__main__':
	main()

	
#debug
p = load("D:\Antoine\Programmation\piet-py-editor\date4.png")
inter = Interpreter(p)